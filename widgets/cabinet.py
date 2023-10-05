import random
import asyncio
from typing import Optional, Callable
from dataclasses import dataclass
from functools import partial

from reactpy import html, component
from reactpy.core.hooks import use_state, use_ref, use_effect

from css_utils import grid_position
from .cell import CellWrapper, CellDetails
from consts import STATUSES


@dataclass
class CabinetDetails:
    title: str
    focused_cell: Optional[int]
    hovered_cell: Optional[int]
    on_click: Callable[[int], None]
    on_hover: Callable[[int, bool], None]
    width: int = 3
    height: int = 5

@component
def CabinetHeader(name):
    return html.div(
        {
            'class_name': 'cabinet-header',
            'style': {'display': 'inherit', **grid_position(1, 1, width=3)}
        },
        html.div(
            {'class_name': 'cell-text '},
            name
        )
    )

@component
def Cabinet(details: CabinetDetails):
    cells_data, set_cells_data = use_state([])
    is_first_render = use_ref(True)

    @use_effect(dependencies=[])
    async def effect():
        # Fetch the data in the background
        is_first_render.current = False

        # Simulate fetching delay for some of the cabinets
        should_delay = (details.title in 'GH')
        if should_delay:
            await asyncio.sleep(random.random() * 2 + 1)
        else:
            await asyncio.sleep(random.random() * 0.5)

        cells_data = [random.choice(STATUSES) for _ in range(details.width * details.height)]
        set_cells_data(cells_data)

    cells = []
    if cells_data:
        for y in range(details.height):
            for x in range(details.width):
                cell_number = (1 + details.width * y + x)  # Starting from 1 at the top left
                status = cells_data[cell_number - 1]

                cell_details = CellDetails(
                    cabinet=details.title,
                    number=cell_number,
                    position=(x + 1, y + 2),
                    status=status,
                    delay=(0.05 * (details.height / details.width * x + y)),
                    show_popup=(details.focused_cell == cell_number),
                    show_tooltip=(details.hovered_cell == cell_number),
                    on_click=partial(details.on_click, cell_number),
                    on_hover=partial(details.on_hover, cell_number),
                )

                cells.append(
                    CellWrapper(cell_details)
                )

    return html.div(
        {'class_name': 'cabinet'},
        CabinetHeader(details.title),
        *cells
    )