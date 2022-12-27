import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import dash
from dash import dcc, html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

df = pd.read_csv("BeeData.csv")
df = df.groupby(['State', 'ANSI', 'Affected by', 'Year', 'state_code'])[['Pct of Colonies Impacted']].mean()
df.reset_index(inplace=True)
# print(df[:5])

# App layout

app.layout = html.Div([

    html.H1("Web Application built with Dash", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_year",
                 options=[
                     {"label": "Disease", "value": "Disease"},
                     {"label": "Other", "value": "Other"},
                     {"label": "Pesticides", "value": "Pesticides"},
                     {"label": "Pests_excl_Varroa", "value": "Pests_excl_Varroa"},
                     {"label": "Unknown", "value": "Unknown"},
                     {"label": "Varroa_mites", "value": "Varroa_mites"},
                 ],
                 multi=False,
                 value="Varroa_mites",
                 style={'width': "40%"}),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_bee_map', figure={})
])

# Callback Function

@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_bee_map', component_property='figure')],
    [Input(component_id='slct_year', component_property='value')]
)

def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The year chosen by the user was: {}".format(option_slctd)

    dff = df.copy()
    dff = dff[dff["Affected by"] == option_slctd]

    # Plotly Express


    fig = px.line(
        dff,
        x="Year",
        y="Pct of Colonies Impacted",
        color='state_code'
    )


    # Graph Opjects

    return container, fig


if __name__ == '__main__':
    app.run_server(debug=True)
