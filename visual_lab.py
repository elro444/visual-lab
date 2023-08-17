from typing import Tuple
from threading import Thread

from reactpy import component, html, use_state, use_ref, web
import random

from css_utils import grid_position

STATUSES = \
    ['good'] * 20 + \
    ['down'] * 2 + \
    ['unknown-device'] * 5 + \
    ['broken', 'misconfigured']

STATUS_BAR_DELAY_OFFSET = 0.17  # trust me on this one

mui = web.module_from_template(
    "react@18.2.0",
    "material-ui-core@5.0.1",
    fallback="⌛",
    cdn='http://localhost:9999/npm',
)

Tooltip = web.export(mui, "Tooltip")

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
            Tooltip(
                {'title': 'what?'},
                html.div('Hi there!')
            ),
            # html.div({'data-toggle': 'tooltip', 'data-placement': 'left', 'title': 'Woohoo!'}, 'Hi there!')
            # *[Cabinet(x) for x in 'ABCDEFGH']
        ),
    )


@component
def StatusBar(delay=0):
    return html.div(
        {'class_name': 'status-bar',
         'style': f'animation-delay: {delay}s'}
    )


@component
def Cell(text: str = '', delay: int = 0, position: Tuple[int, int] = None):
    status = random.choice(STATUSES)
    position_style = '' if position is None else grid_position(*position)
    return html.div(
        {'class_name': f'cell status-{status}',
         'style': f'animation-delay: {delay}s; {position_style}'},
        html.div(
            {'class_name': 'cell-text '},
            text
        ),
        StatusBar(STATUS_BAR_DELAY_OFFSET + delay)
    )


@component
def CabinetHeader(name):
    return html.div(
        {
            'class_name': 'cabinet-header',
            'style': f'display: inherit; {grid_position(1, 1, width=3)}'
        },
        html.div(
            {'class_name': 'cell-text '},
            name
        )
    )


def make_cells(width, height, set_cells, should_delay):
    from time import sleep
    if should_delay:
        sleep(random.random() * 2 + 1)
    else:
        sleep(random.random() * 0.5)

    cells = []
    for y in range(height):
        for x in range(width):
            text = str(1 + 3 * y + x)
            delay = 0.05 * (5/3 * x + y)
            position = (x + 1, y + 2)
            cells.append(
                Cell(text, delay, position)
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
            args=(width, height, set_cells, title in 'GH')
        )
        worker.start()

    return html.div(
        {'class_name': 'cabinet'},
        CabinetHeader(title),
        *cells
    )
