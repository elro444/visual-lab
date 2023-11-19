from reactpy import component, html
from reactpy.types import Component
from typing import TypeVar, Callable, cast
from . import cell
from .tooltip import PopupButton
from consts import Status, COLORS
from css_utils import colorize

POPUP_WIDTH = '250px'

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


@popup_maker(Status.DOWN)
@component
def _popup_down(details: 'cell.CellDetails'):
    return html.div(
        {
            'style': {
                'width': POPUP_WIDTH,
            },
        },
        f'The interface in cell {details.cell_id} is ',
        colorize('DOWN', COLORS[Status.DOWN]),
        '. Please make sure the cable is connected!',
    )

@popup_maker(Status.MISCONFIGURED)
@component
def _popup_misconfigured(details: 'cell.CellDetails'):
    # TODO: Improve the styling on the button in this component
    def quick_fix(_):
        # TODO: Reconfigure the DB
        ...

    return html.div(
        {
            'style': {
                'width': POPUP_WIDTH,
            },
        },
        # TODO: Fix this message
        f'Device #100 is in this cell, but is configured to cell A-1.\n',
        f'Click the button below to move it to {details.cell_id}\n',
        PopupButton('Quick Fix', quick_fix),
    )
