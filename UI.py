# ---------------------Imports---------------------#
import dash_bootstrap_components as dbc
from dash import dcc, html
# ---------------------------NAVBAR------------------------------------------#
navbar = dbc.NavbarSimple(
    children=[
        dbc.DropdownMenu(
            children=[
            dcc.ConfirmDialog(
                id='credits',
                message='Dash application created by Levi S Eichelberg',
            ),
            dbc.DropdownMenuItem("Credits", id='credits-input', n_clicks=0)
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="Dish - KPI Report Tool",
    brand_href="#",
    color="primary",
    dark=True,
)


# -----------------------How to-------------------------------#
help_info = html.Div(className='container-fluid', children=[
    html.H1("How to use.", className='mt-4'),
    html.P("1.  Open MO.drm and TPut.drm Log in X-Cap Tool"),
    html.P("2.  Export .xlsx data from each log using the .fav KPI."),
    html.P("3.  Drag and drop both .xlsx files on the left."),
    html.P("4.  Set report, name, date & hit generate."),
    html.P(""),
    html.P("Note: Please wait up to 2 minutes for report to generate depending on data size.")
])



