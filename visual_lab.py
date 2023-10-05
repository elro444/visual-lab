from reactpy import component, html

from widgets.cabinet import Cabinet


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
    )
