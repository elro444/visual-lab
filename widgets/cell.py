from typing import Tuple, Callable
from dataclasses import dataclass

from reactpy import html, component, use_effect, use_ref, Ref, event

from css_utils import grid_position
from .tooltip import Tooltip
from consts import COLORS

STATUS_BAR_DELAY_OFFSET = 0.17  # trust me on this one


@dataclass(frozen=True)
class CellDetails:
    """
    An immutable helper class to hold all the details about a cell.
    Simplifies agument passing all over the place.
    """
    cabinet: str
    number: int
    position: Tuple[int, int]  # Position (x,y) in the cabinet
    status: str
    delay: float
    show_popup: bool
    show_tooltip: bool
    on_click: Callable[[], None]
    on_hover: Callable[[bool], None]


@component
def StatusBar(delay: float, should_animate: bool):
    classes = ['status-bar']
    if should_animate:
        classes.append('status-bar-animation')
    return html.div(
        {
            'class_name': ' '.join(classes),
            'style': f'animation-delay: {delay}s',
        }
    )


@component
def Cell(details: CellDetails):
    should_animate: Ref = use_ref(True)

    @use_effect(dependencies=[])
    async def effect():
        # Disable the animations after the first render
        should_animate.current = False

    if details.position is None:
        position_style = ''
    else:
        position_style = grid_position(*details.position)

    classes = ['cell', f'status-{details.status}']
    if should_animate.current:
        classes.append('cell-animation')

    cell = html.div(
        {
            'class_name': ' '.join(classes),
            'style': f'animation-delay: {details.delay}s; {position_style}',
            'onmouseenter': lambda _: details.on_hover(True),
            'onmouseleave': lambda _: details.on_hover(False),
            'onclick': event(lambda _: details.on_click(), stop_propagation=True),
        },
        html.div(
            {'class_name': 'cell-text'},
            details.number
        ),
        StatusBar(STATUS_BAR_DELAY_OFFSET + details.delay, should_animate.current)
    )

    if details.show_tooltip or details.show_popup:
        return html.div(cell, CellTooltip(details))
    return cell


@component
def CellTooltip(details: CellDetails):
    tooltip = html.div(
        {'style': {'width': '130px'}},
        f"Device at {details.cabinet}-{details.number} has status ",
        html.span(
            {'style': {'color': COLORS[details.status]}},
            details.status,
        )
    )
    return Tooltip(tooltip)
