import random
from typing import Tuple

from reactpy import html, component

from css_utils import grid_position
from .tooltip import Tooltip

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