from reactpy import html, component
from reactpy.types import Component


@component
def Tooltip(tooltip_content: Component, hoverables):
    if not hoverables:
        return html.span()

    tooltip = html.div(
        {'class_name': 'vl-tooltip'},
        tooltip_content
    )

    return html.div(
        {
            'style': {
                'position': 'relative',
            }
        },
        *hoverables,
        tooltip
    )
