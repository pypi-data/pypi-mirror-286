from typing import Type, cast

from rodi import Container, Services
from whistle import IAsyncEventDispatcher

from harp import __revision__, __version__, get_logger
from harp.asgi import ASGIKernel
from harp.asgi.events import EVENT_CONTROLLER_VIEW, EVENT_CORE_REQUEST, RequestEvent
from harp.config import Config
from harp.config.events import (
    EVENT_FACTORY_BIND,
    EVENT_FACTORY_BOUND,
    EVENT_FACTORY_BUILD,
    EVENT_FACTORY_DISPOSE,
    FactoryBindEvent,
    FactoryBoundEvent,
    FactoryBuildEvent,
    FactoryDisposeEvent,
)
from harp.controllers import ProxyControllerResolver
from harp.event_dispatcher import LoggingAsyncEventDispatcher
from harp.http import HttpResponse
from harp.typing import GlobalSettings
from harp.utils.network import Bind
from harp.views.json import on_json_response

logger = get_logger(__name__)


async def ok_controller():
    return HttpResponse("Ok.", status=200)


async def on_health_request(event: RequestEvent):
    if event.request.path == "/healthz":
        event.set_controller(ok_controller)
        event.stop_propagation()


class KernelFactory:
    AsyncEventDispatcherType: Type[IAsyncEventDispatcher] = LoggingAsyncEventDispatcher
    ContainerType: Type[Container] = Container
    KernelType: Type[ASGIKernel] = ASGIKernel

    # references for external treatments
    container: Container
    provider: Services
    dispatcher: IAsyncEventDispatcher
    resolver: ProxyControllerResolver

    def __init__(self, configuration: Config):
        self.configuration = configuration
        self.hostname = "[::]"

    async def build(self) -> tuple[ASGIKernel, list[Bind]]:
        logger.info(f"🎙  HARP v.{__version__} ({__revision__})")
        # we only work on validated configuration
        self.configuration.validate()

        logger.info(f"📦 Apps: {', '.join(map(lambda name: name.split('.')[-1], self.configuration.applications))}")

        self.dispatcher = self.build_event_dispatcher()
        self.container = self.build_container(self.dispatcher)
        self.resolver = ProxyControllerResolver()

        # dispatch "bind" event: this is the last chance to add services to the container
        try:
            await self.dispatcher.adispatch(
                EVENT_FACTORY_BIND,
                FactoryBindEvent(
                    self.container,
                    self.configuration.settings,
                ),
            )
        except Exception as exc:
            logger.fatal("Fatal while dispatching «factory bind» event: %s", exc)
            raise

        # this can fail if configuration is not valid, but we let the container raise exception which is more explicit
        # that what we can show here.
        self.provider = self.container.build_provider()

        # dispatch "bound" event: you get a resolved container, do your thing
        try:
            await self.dispatcher.adispatch(
                EVENT_FACTORY_BOUND,
                FactoryBoundEvent(
                    self.provider,
                    self.resolver,
                ),
            )
        except Exception as exc:
            logger.fatal("Fatal while dispatching «factory bound» event: %s", exc)
            raise

        self.kernel = self.KernelType(dispatcher=self.dispatcher, resolver=self.resolver)
        binds = [Bind(host=self.hostname, port=port) for port in self.resolver.ports]
        event = FactoryBuildEvent(self.kernel, binds)
        await self.dispatcher.adispatch(EVENT_FACTORY_BUILD, event)

        return event.kernel, event.binds

    async def dispose(self):
        if self.kernel:
            event = FactoryDisposeEvent(self.kernel, self.provider)
            await self.dispatcher.adispatch(EVENT_FACTORY_DISPOSE, event)

    def build_container(self, dispatcher: IAsyncEventDispatcher) -> Container:
        """Factory method responsible for the service injection container creation, registering initial services."""
        container = cast(Container, self.ContainerType())
        container.add_instance(self.configuration.settings, GlobalSettings)
        container.add_instance(dispatcher, IAsyncEventDispatcher)

        self.configuration.register_services(container)

        return container

    def build_event_dispatcher(self) -> IAsyncEventDispatcher:
        """Factory method responsible for the event dispatcher creation, binding initial/generic listeners."""
        dispatcher = cast(IAsyncEventDispatcher, self.AsyncEventDispatcherType())

        dispatcher.add_listener(EVENT_CORE_REQUEST, on_health_request, priority=-100)

        # todo move into core or extension, this is not proxy related
        dispatcher.add_listener(EVENT_CONTROLLER_VIEW, on_json_response)

        self.configuration.register_events(dispatcher)

        return dispatcher
