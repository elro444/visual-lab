import random
from threading import Thread

from reactpy import html, component
from reactpy.core.hooks import use_state, use_ref

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


def make_cells(cabinet_title, width, height, set_cells, should_delay):
    from time import sleep
    if should_delay:
        sleep(random.random() * 2 + 1)
    else:
        sleep(random.random() * 0.5)

    cells = []
    for y in range(height):
        for x in range(width):
            text = str(1 + width * y + x)
            delay = 0.05 * (height/width * x + y)
            position = (x + 1, y + 2)
            status = random.choice(STATUSES)
            cells.append(
                CellWrapper(cabinet_title, text, status, delay, position)
            )
    set_cells(cells)


@component
def Cabinet(title, width=3, height=5):
    cells, set_cells = use_state([])

    is_first = use_ref(True)

    if is_first.current:
        is_first.current = False

        worker = Thread(
            target=make_cells,
            args=(title, width, height, set_cells, title in 'GH')
        )
        worker.start()

    return html.div(
        {'class_name': 'cabinet'},
        CabinetHeader(title),
        *cells
    )