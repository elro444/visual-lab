from typing import Tuple, Callable
from dataclasses import dataclass

from reactpy import html, component, use_state, use_effect, use_ref, Ref

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
def Cell(details: CellDetails, should_animate: Ref, set_is_hovered):
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
            'onmouseenter': lambda *_: set_is_hovered(True),
            'onmouseleave': lambda *_: set_is_hovered(False),
        },
        html.div(
            {'class_name': 'cell-text'},
            details.number
        ),
        StatusBar(STATUS_BAR_DELAY_OFFSET + details.delay, should_animate.current)
    )
    return cell


@component
def CellTooltip(details: CellDetails, hoverables):
    tooltip = html.div(
        {'style': {'width': '130px'}},
        f"Device at {details.cabinet}-{details.number} has status ",
        html.span(
            {'style': {'color': COLORS[details.status]}},
            details.status,
        )
    )
    return Tooltip(tooltip, hoverables)


@component
def CellWrapper(cell_details: CellDetails):
    """
    We need this wrapper because if the state is created inside the Cell
    component, each change to it will trigger a render for the cell
    itself, which will trigger the css animations again..
    This way, reactpy knows the change is only in the CellWrapper and Tooltip,
    and not in the Cell itself, so it is not re-rendered :)
    """
    is_hovered, set_is_hovered = use_state(False)

    should_animate: Ref = use_ref(True)
    @use_effect(dependencies=[])
    async def effect():
        # Disable the animations after the first render
        should_animate.current = False

    cell = Cell(cell_details, should_animate, set_is_hovered)

    if not is_hovered:
        return cell
    return CellTooltip(cell_details, hoverables=[cell])
