from reactpy import html, component
from reactpy.types import Component


@component
def Tooltip(tooltip_content: Component):
    return html.div(
        {
            'style': {
                'position': 'relative',
            }
        },
        html.div(
            {
                'class_name': 'vl-tooltip'
            },
            tooltip_content
        )
    )
