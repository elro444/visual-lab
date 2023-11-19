from typing import Callable
from reactpy import html, component
from reactpy.types import Component

TOOLTIP = 'vl-tooltip'
POPUP = 'vl-popup'

@component
def Tooltip(tooltip_content: Component, class_name=TOOLTIP):
    return html.div(
        {
            'style': {
                'position': 'relative',
            }
        },
        html.div(
            {
                'class_name': class_name
            },
            tooltip_content
        )
    )


@component
def PopupButton(text: str, onclick: Callable, override_style=None):
    style = {}
    if override_style:
        style.update(override_style)
    return html.span(
        {
            'class_name': 'vl-popup-button',
            'onclick': onclick,
            'style': style,
        },
        f' {text} '
    )
