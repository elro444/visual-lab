from dataclasses import dataclass
from typing import Optional, Callable, Tuple
from functools import partial
import traceback

from reactpy import component, html, use_state, event

from widgets import cabinet


@dataclass
class LabState:
    focused_cell: Optional[str]
    set_focused_cell: Callable[[Optional[str]], None]
    hovered_cell: Optional[str]
    set_hovered_cell: Callable[[Optional[str]], None]


def get_titles():
    return [x for x in 'ABCDEFGH']


def parse_cell_id(cell_id: Optional[str]) -> Tuple[Optional[str], Optional[int]]:
    if cell_id is None:
        cabinet, number = None, None
    else:
        cabinet, number = cell_id.split('-')
        number = int(number)
    return cabinet, number


@component
def VisualLab():
    # "Focused" is when we click on the cell and it shows the popup
    focused_cell, set_focused_cell = use_state(None)
    focused_cell_cabinet, focused_cell_number = parse_cell_id(focused_cell)

    # "Hovered" is when we hover on the cell and it shows the tooltip (unless it is focused)
    hovered_cell, set_hovered_cell = use_state(None)
    hovered_cell_cabinet, hovered_cell_number = parse_cell_id(hovered_cell)

    def on_hover(title: str, cell_number: int, is_hovered: bool):
        if is_hovered:
            set_hovered_cell(f'{title}-{cell_number}')
        else:
            set_hovered_cell(None)
    def on_click(title: str, cell_number: int):
        set_focused_cell(f'{title}-{cell_number}')

    cabinets = []
    for title in get_titles():
        passed_focused_cell = None
        if focused_cell_cabinet == title:
            passed_focused_cell = focused_cell_number

        passed_hovered_cell = None
        if hovered_cell_cabinet == title:
            passed_hovered_cell = hovered_cell_number

        details = cabinet.CabinetDetails(
            title=title,
            focused_cell=passed_focused_cell,
            hovered_cell=passed_hovered_cell,
            on_click=partial(on_click, title),
            on_hover=partial(on_hover, title),
        )
        cabinets.append(cabinet.Cabinet(details))

    def clear_focused_cell(_):
        set_focused_cell(None)

    return html.div(
        {
            'class_name': 'visual-lab',
            'onclick': clear_focused_cell,
        },
        html.div(
            html.h1(
                {'style': 'text-align: center; padding: 50px'},
                'Visual Lab!'
            ),
            html.div(
                {'style': 'display: flex; flex-direction: row;'
                        'justify-content: center'},
                *cabinets,
            ),
        )
    )
