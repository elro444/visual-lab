from reactpy import component, html
import random

STATUSES = ['good', 'down', 'unknown-device', 'broken', 'misconfigured']

STATUS_BAR_DELAY_OFFSET = 0.17 # trust me on this one

@component
def Base():
    return html.div(
        html.h1('Visual Lab!'),
        Cabinet(3, 5)
    )

@component
def StatusBar(delay=0):
    return html.div(
        {'class_name': 'status-bar',
         'style': f'animation-delay: {delay}s'}
    )

@component
def Cell(text: str = '', delay=0):
    status = random.choice(STATUSES)
    return html.div(
        {'class_name': f'cell status-{status}',
         'style': f'animation-delay: {delay}s;'},
        html.div(
            {'class_name': 'cell-text '},
            text
        ),
        StatusBar(STATUS_BAR_DELAY_OFFSET + delay)
    )


@component
def Line(items):
    return html.div({'class_name': 'cabinet-row'}, *items)


@component
def Cabinet(width, height):
    return html.div(
        {'class_name': 'cabinet'},
        *(
            Line([Cell(str(1 + y * 3 + x), 0.05 * (x + y)) for x in range(width)]) for y in range(height)
        )
    )
