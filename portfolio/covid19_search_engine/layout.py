import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

layout = html.Div([
    html.Br(),
    html.Br(),
    html.H1('Accelerate Your Research', style = {'text-align': 'center', 'font-family':'sans-serif'}),
    html.Br(),
    html.H5("Search the COVID-19 research database or enter the text from a paper you're interested in. The algorithm will read the paper and provide recommendations for further reading based on your interests.",
            style = {'text-align': 'center', 'font-family':'sans-serif'}),
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Search Database', value='tab-1'),
        dcc.Tab(label='Enter Your Own Paper', value='tab-2'),
    ], style = {'width':'50%', 'margin':'auto'}),
    html.Br(),
    html.Div(id='tab-output'),
    html.Div(html.P(["Data: COVID-19 Open Research Dataset (CORD-19). 2020."], style= {'text-align': 'center','font-size': '10px', 'verticleAlign': 'text-bottom'})),
    html.Div(html.P(["Created by: Brian VandenAkker"], style= {'text-align': 'center','font-size': '10px', 'verticleAlign': 'text-bottom'})),
])
