def grid_position(x, y, width=1, height=1):
    width_str = height_str = ''
    if width != 1:
        width_str = f'/ span {width}'
    if height != 1:
        height_str = f'/ span {height}'
    return {
        'grid-row': f'{y} {height_str}',
        'grid-column': f'{x} {width_str}',
    }
