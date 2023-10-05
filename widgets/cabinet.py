import random
import asyncio

from reactpy import html, component
from reactpy.core.hooks import use_state, use_ref, use_effect

from css_utils import grid_position
from .cell import CellWrapper
from consts import STATUSES

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
def Cabinet(title, width=3, height=5):
    cells, set_cells = use_state([])
    is_first_render = use_ref(True)

    @use_effect(dependencies=[])
    async def effect():
        # Fetch the data in the background
        is_first_render.current = False

        # Simulate fetching delay for some of the cabinets
        should_delay = (title in 'GH')
        if should_delay:
            await asyncio.sleep(random.random() * 2 + 1)
        else:
            await asyncio.sleep(random.random() * 0.5)

        cells = []
        for y in range(height):
            for x in range(width):
                text = str(1 + width * y + x)
                delay = 0.05 * (height/width * x + y)
                position = (x + 1, y + 2)
                status = random.choice(STATUSES)
                cells.append(
                    CellWrapper(title, text, status, delay, position)
                )
        set_cells(cells)

    return html.div(
        {'class_name': 'cabinet'},
        CabinetHeader(title),
        *cells
    )