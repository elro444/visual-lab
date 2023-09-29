import asyncio

from reactpy import html, component, use_state, use_ref, use_effect
from reactpy.types import Component


HIDE_DELAY = 0.2
IS_ON_COOLDOWN = False

async def _delayed_tooltip_hide(is_hovered, set_visibility, delay):
    """
    Give the user time to re-hover the tooltip before disappearing
    """
    global IS_ON_COOLDOWN
    await asyncio.sleep(delay)
    if is_hovered():
        # The user started hovering again before the timeout ran out
        return
    set_visibility(False)
    IS_ON_COOLDOWN = False


def _tooltip_hover_effect(is_hovered, set_visibility, _set_is_hovered):
    global IS_ON_COOLDOWN
    if is_hovered():
        if not IS_ON_COOLDOWN:
            IS_ON_COOLDOWN = True
            set_visibility(True)
        else:
            # We need to cleanup, otherwise the next time we won't trigger a render :(
            # We should find a better way to do this..
            _set_is_hovered(False)
    else:
        # Run in background
        task = _delayed_tooltip_hide(is_hovered, set_visibility, HIDE_DELAY)
        asyncio.get_event_loop().create_task(task)


@component
def Tooltip(tooltip_content: Component, hoverables):
    if not hoverables:
        return html.span()

    # The actual state that controls if the tooltip is visible
    is_visible, set_visibility = use_state(False)

    # We need a ref so that our background task will get the 'realtime' value
    is_hovered_ref = use_ref(False)
    # We also need a state because refs do not trigger effects :(
    is_hovered, _set_is_hovered = use_state(False)

    # We use an effect to delay the hiding and give
    # the user an option to re-hover before we hide
    use_effect(
        lambda: _tooltip_hover_effect(
            is_hovered=lambda: is_hovered_ref.current,
            set_visibility=set_visibility,
            _set_is_hovered=_set_is_hovered,
        ),
        [is_hovered]
    )

    def set_is_hovered(value):
        # We really want to update both (to trigger the effect above)
        if value != is_visible:
            is_hovered_ref.current = value
            _set_is_hovered(value)

    container_attrs = {
        'style': {
            'position': 'relative',
            'display': 'inline-block',
        },
        'onmouseenter': lambda *_: set_is_hovered(True),
        'onmouseleave': lambda *_: set_is_hovered(False),
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
