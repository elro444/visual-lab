from typing import Tuple
from threading import Thread

from reactpy import component, html, use_state, use_ref
import random
from dnd import DraggableItem, ExampleTarget, CustomDndProvider

from css_utils import grid_position

from fixer import Button, Tooltip

STATUSES = \
    ['good'] * 20 + \
    ['down'] * 2 + \
    ['unknown-device'] * 5 + \
    ['broken', 'misconfigured']

STATUS_BAR_DELAY_OFFSET = 0.17  # trust me on this one


# (item, monitor) => {
#       const dropResult = monitor.getDropResult()
#       if (item && dropResult) {
#         alert(`You dropped ${item.name} into ${dropResult.name}!`)
#       }
#     }

def drop_end(item, monitor):
    print("Dropped!", item, monitor)

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
        CustomDndProvider({}, 
            ExampleTarget(),
            DraggableItem(
                {'drop_end': drop_end,
                'name': "HI"}
            ),
        ),
    )


@component
def Cell(text: str = '', delay: int = 0, position: Tuple[int, int] = None):
    status = random.choice(STATUSES)
    position_style = {} if position is None else grid_position(*position)
    status_bar_delay = STATUS_BAR_DELAY_OFFSET + delay

    return Tooltip({
            "title": "Connected is ID 9999",
            "arrow": True
        }, html.div(
        {
        'class_name': f'cell status-{status}',
         'style': {'animation-delay': f'{delay}s', **position_style}
         },
        html.div(
            {'class_name': 'cell-text '},
            text
        ),
        # This is a status bar
        # Somewhy components don't work inside a Tooltip,
        # So I had to place here only <div>s
        html.div(
            {'class_name': 'status-bar',
             'style': {'animation-delay': f'{status_bar_delay}s'}
             }
        )
    ))


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
