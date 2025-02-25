from pydantic import BaseModel, ConfigDict
from typing import Callable, Dict, Type, Awaitable, TypeVar, Generic, ClassVar
from starlette.concurrency import run_in_threadpool
from asgiref.sync import async_to_sync
import inspect

RequestT = TypeVar("RequestT", bound=BaseModel)
ResponseT = TypeVar("ResponseT")


class Mediator(BaseModel, Generic[RequestT, ResponseT]):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    _request_handlers: ClassVar[
        Dict[Type[RequestT], Callable[[RequestT], Awaitable[ResponseT]]]
    ] = {}

    @classmethod
    def register_handler(
        cls, request_type: Type[RequestT]
    ) -> Callable[
        [Callable[[RequestT], Awaitable[ResponseT]]],
        Callable[[RequestT], Awaitable[ResponseT]],
    ]:
        def decorator(
            func: Callable[[RequestT], Awaitable[ResponseT]],
        ) -> Callable[[RequestT], Awaitable[ResponseT]]:
            cls._request_handlers[request_type] = func
            return func

        return decorator

    async def send(self, request: RequestT) -> ResponseT:
        handler = self._request_handlers.get(type(request))

        if not handler:
            raise ValueError(f"No request handler found for {type(request)}")

        if inspect.iscoroutinefunction(handler) or inspect.isawaitable(handler):
            return await handler(request)
        else:
            return await run_in_threadpool(handler, request)


mediator: Mediator[RequestT, ResponseT] = Mediator()


def get_mediator() -> Mediator[RequestT, ResponseT]:
    return mediator


class MediatorDTO(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
