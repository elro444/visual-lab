import random
from typing import Tuple
from threading import Thread

from reactpy import component, html, use_state, use_ref

from tooltip import Tooltip
from css_utils import grid_position

STATUSES = \
    ['good'] * 20 + \
    ['down'] * 2 + \
    ['unknown-device'] * 5 + \
    ['broken', 'misconfigured']

COLORS = {
    'good': '#72fa93',
    'down': '#e45f2b',
    'unknown-device': '#f6c445',
    'broken': '#e39af0',
    'misconfigured': '#9ac1f0',
}

STATUS_BAR_DELAY_OFFSET = 0.17  # trust me on this one


@component
def Base():
    return html.div(
        html.h1(
            {'style': 'text-align: center; margin: 50px'},
            'Visual Lab!'
        ),
        html.div(
            {'style': 'display: flex; flex-direction: row;'
                      'justify-content: center'},
            *[Cabinet(x) for x in 'ABCDEFGH']
        ),
    )


@component
def StatusBar(delay=0):
    return html.div(
        {'class_name': 'status-bar',
         'style': f'animation-delay: {delay}s'}
    )


@component
def Cell(cabinet: str, text: str = '', delay: int = 0, position: Tuple[int, int] = None):
    status = random.choice(STATUSES)
    position_style = '' if position is None else grid_position(*position)

    tooltip = html.div(
        {'style': {'width': '130px'}},
        f"Device at {cabinet}-{text} has status ",
        html.span(
            {'style': {'color': COLORS[status]}},
            status
        )
    )
    cell = html.div(
        {'class_name': f'cell status-{status}',
         'style': f'animation-delay: {delay}s; {position_style}'},
        html.div(
            {'class_name': 'cell-text'},
            text
        ),
        StatusBar(STATUS_BAR_DELAY_OFFSET + delay)
    )
    return Tooltip(tooltip, hoverables=[cell])


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
            cells.append(
                Cell(cabinet_title, text, delay, position)
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
