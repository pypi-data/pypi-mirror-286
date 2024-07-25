# ruff: noqa: D100, D101, D102, D103, D104, D105, D107
from __future__ import annotations

import logging
from types import ModuleType
from typing import TYPE_CHECKING, Any, Self, cast

if TYPE_CHECKING:
    from collections.abc import Generator, Iterator

logger = logging.getLogger('fake')
logger.setLevel(logging.INFO)


class Fake(ModuleType):
    def __init__(
        self: Fake,
        *args: object,
        __props: dict[str, object] | None = None,
        __items: dict[str, object] | None = None,
        __list: list[object] | None = None,
        __return_value: object | None = None,
        __await_value: object | None = None,
        __length: int | None = None,
        __iter: Iterator | None = None,
        **kwargs: object,
    ) -> None:
        self.__debug = kwargs.pop('_Fake__debug', False)
        logger.log(
            logging.INFO if self.__debug else logging.DEBUG,
            'Initializing `Fake`',
            extra={
                'args_': args,
                'kwargs': kwargs,
                '__return_value': __return_value,
                '__await_value': __await_value,
                '__props': __props,
            },
        )
        self.__props = __props
        self.__items = __items
        self.__list = __list
        self.__return_value = __return_value
        self.__await_value = __await_value
        self.__iteration_counter = 0
        self.__length = (len(__list) if __list else 1) if __length is None else __length
        self.__iter = __iter
        super().__init__('')

    def __init_subclass__(cls: type[Fake], **kwargs: dict[str, Any]) -> None:
        logger.log(
            logging.INFO if kwargs.get('__debug', False) else logging.DEBUG,
            'Subclassing `Fake`',
            extra={'cls': cls, 'kwargs': kwargs},
        )

    def __getattr__(self: Fake, attr: str) -> Fake:
        if attr.startswith('_Fake__'):
            return self.__getattribute__(attr[5:])
        logger.log(
            logging.INFO if self.__debug else logging.DEBUG,
            'Accessing fake attribute of a `Fake` instance',
            extra={'attr': attr, 'props': self.__props},
        )
        if self.__props and attr in self.__props:
            return cast(Fake, self.__props[attr])
        if attr == '__file__':
            return cast(Fake, 'fake')
        return self

    def __setattr__(self: Fake, attr: str, value: object) -> None:
        if attr != '_Fake__debug':
            logger.log(
                logging.INFO if self.__debug else logging.DEBUG,
                'Accessing fake attribute of a `Fake` instance',
                extra={'attr': attr},
            )
        super().__setattr__(attr, value)

    def __getitem__(self: Fake, key: object) -> object:
        logger.log(
            logging.INFO if self.__debug else logging.DEBUG,
            'Accessing fake item of a `Fake` instance',
            extra={'key': key},
        )
        if self.__items and key in self.__items:
            return self.__items[key]
        if isinstance(key, int) and self.__list:
            return self.__list[key]
        return self

    def __setitem__(self: Fake, key: object, value: object) -> None:
        logger.log(
            logging.INFO if self.__debug else logging.DEBUG,
            'Setting fake item of a `Fake` instance',
            extra={'key': key, 'value': value},
        )

    def __call__(self: Fake, *args: object, **kwargs: dict[str, Any]) -> Fake:
        logger.log(
            logging.INFO if self.__debug else logging.DEBUG,
            'Calling a `Fake` instance',
            extra={
                'args_': args,
                'kwargs': kwargs,
                '__return_value': self.__return_value,
            },
        )
        return cast(
            Fake,
            self.__return_value if self.__return_value is not None else self,
        )

    def __await__(self: Fake) -> Generator[Any, Any, object]:
        logger.log(
            logging.INFO if self.__debug else logging.DEBUG,
            'Awaiting a `Fake` instance',
            extra={'__await_value': self.__await_value},
        )
        yield
        return self.__await_value or Fake()

    def __next__(self: Fake) -> Fake:
        logger.log(
            logging.INFO if self.__debug else logging.DEBUG,
            'Getting next of a `Fake` instance',
            extra={'length': self.__length},
        )
        if self.__iteration_counter >= self.__length:
            raise StopIteration
        self.__iteration_counter += 1
        return self

    def __anext__(self: Fake) -> Fake:
        logger.log(
            logging.INFO if self.__debug else logging.DEBUG,
            'Getting async next of a `Fake` instance',
            extra={'length': self.__length},
        )
        if self.__iteration_counter >= self.__length:
            raise StopAsyncIteration
        self.__iteration_counter += 1
        return self

    def __iter__(self: Fake) -> Iterator[Fake]:
        logger.log(
            logging.INFO if self.__debug else logging.DEBUG,
            'Getting iterator of a `Fake` instance',
            extra={'iter': self.__iter},
        )
        if self.__iter is not None:
            return self.__iter
        return self

    def __aiter__(self: Fake) -> Iterator[Fake]:
        logger.log(
            logging.INFO if self.__debug else logging.DEBUG,
            'Getting async iterator of a `Fake` instance',
            extra={'iter': self.__iter},
        )
        if self.__iter is not None:
            return self.__iter
        return self

    def __enter__(self: Fake) -> Fake:  # noqa: PYI034
        return self

    def __exit__(self: Fake, *_: object) -> None:
        pass

    async def __aenter__(self: Self) -> Self:
        return self

    async def __aexit__(self: Fake, *_: object) -> None:
        pass

    def __mro_entries__(self: Fake, bases: tuple[type[Fake]]) -> tuple[type[Fake]]:
        logger.log(
            logging.INFO if self.__debug else logging.DEBUG,
            'Getting MRO entries of a `Fake` instance',
            extra={'bases': bases},
        )
        return (cast(type, self),)

    def __len__(self: Fake) -> int:
        return self.__length

    def __index__(self: Fake) -> int:
        return self.__length

    def __contains__(self: Fake, _: object) -> bool:
        return True

    def __eq__(self: Fake, _: object) -> bool:
        return True

    def __ne__(self: Fake, _: object) -> bool:
        return False

    def __str__(self: Fake) -> str:
        return 'Fake'

    def __repr__(self: Fake) -> str:
        return 'Fake'

    def __add__(self: Fake, _: object) -> Fake:
        return self

    def __sub__(self: Fake, _: object) -> Fake:
        return self

    def __mul__(self: Fake, _: object) -> Fake:
        return self

    def __truediv__(self: Fake, _: object) -> Fake:
        return self

    def __floordiv__(self: Fake, _: object) -> Fake:
        return self

    def __mod__(self: Fake, _: object) -> Fake:
        return self

    def __pow__(self: Fake, _: object) -> Fake:
        return self

    def __lshift__(self: Fake, _: object) -> Fake:
        return self

    def __rshift__(self: Fake, _: object) -> Fake:
        return self

    def __and__(self: Fake, _: object) -> Fake:
        return self

    def __xor__(self: Fake, _: object) -> Fake:
        return self

    def __or__(self: Fake, _: object) -> Fake:
        return self

    def __neg__(self: Fake) -> Fake:
        return self

    def __pos__(self: Fake) -> Fake:
        return self

    def __abs__(self: Fake) -> Fake:
        return self

    def __invert__(self: Fake) -> Fake:
        return self

    def __round__(self: Fake) -> Fake:
        return self

    def __floor__(self: Fake) -> Fake:
        return self

    def __ceil__(self: Fake) -> Fake:
        return self

    def __trunc__(self: Fake) -> Fake:
        return self

    def __hash__(self: Fake) -> int:
        return hash('Fake')

    def __bool__(self: Fake) -> bool:
        return True

    def __int__(self: Fake) -> int:
        return 0

    def __float__(self: Fake) -> float:
        return 0.0

    def __complex__(self: Fake) -> complex:
        return 0j

    def __bytes__(self: Fake) -> bytes:
        return b'Fake'

    def __format__(self: Fake, _: str) -> str:
        return 'Fake'

    def __dir__(self: Fake) -> list[str]:
        return list(self.__props.keys()) if self.__props else []

    def __sizeof__(self: Fake) -> int:
        return 1
