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
