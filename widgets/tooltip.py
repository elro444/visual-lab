from reactpy import html, component, use_state, use_ref, use_effect
from reactpy.types import Component


@component
def Tooltip(tooltip_content: Component, hoverables):
    if not hoverables:
        return html.span()

    # The actual state that controls if the tooltip is visible
    is_visible, set_visibility = use_state(False)

    container_attrs = {
        'style': {
            'position': 'relative',
            'display': 'inline-block',
        },
        'onmouseenter': lambda *_: set_visibility(True),
        'onmouseleave': lambda *_: set_visibility(False),
    }

    children = list(hoverables)
    if is_visible:
        tooltip = html.div(
            {'class_name': 'vl-tooltip'},
            tooltip_content
        )
        children.append(tooltip)

    return html.div(
        container_attrs,
        *children
    )
