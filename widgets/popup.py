from reactpy import component, html
from reactpy.types import Component
from typing import TypeVar, Callable, cast
from . import cell
from css_utils import colorize

POPUP_WIDTH = '200px'

PopupMaker = TypeVar(
    'PopupMaker',
    bound=Callable[['cell.CellDetails'], Component]
)
_POPUPS: dict[str, PopupMaker] = {}


@component
def default_handler(details: 'cell.CellDetails'):
    return html.div(
        {
            'style': {
                'width': POPUP_WIDTH,
            }
        },
        colorize('Error', '#f12323'),
        f': popup for status {details.status} has not been implemented yet!'
    )


def get_handler(status: str) -> PopupMaker:
    return _POPUPS.get(status, default_handler)


def generate_popup(details: 'cell.CellDetails'):
    handler = get_handler(details.status)
    return handler(details)


def popup_maker(status: str) -> Callable[[PopupMaker], PopupMaker]:
    def wrapper(func: PopupMaker) -> PopupMaker:
        _POPUPS[status] = func
        return func
    return wrapper
