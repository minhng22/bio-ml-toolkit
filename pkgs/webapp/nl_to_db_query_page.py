from dash import html
from dash import dcc

def nl_to_db_query_page():
    return html.Div([
        html.H1("Natural Language to Database Query", style={'textAlign': 'center', 'fontSize': '28px', 'marginBottom': '20px'}),
        html.Div([
            html.Div([
                html.P("This page allows you to convert natural language queries into database queries.", style={'textAlign': 'left', 'fontSize': '16px', 'marginLeft': '10px'})
            ], style={'flex': '0.5', 'padding': '10px'}),
            html.Div([
                html.Div([
                    html.Label("Enter your natural language query:", style={'fontSize': '16px'}),
                    dcc.Textarea(
                        id='nl-query-input',
                        placeholder='Type your query here...',
                        style={
                            'width': '100%',
                            'height': '100px',
                            'marginBottom': '10px',
                            'fontSize': '16px'
                        }
                    ),
                    html.Button("Convert", id="convert-button", style={
                        'marginTop': '10px',
                        'padding': '10px 20px',
                        'backgroundColor': 'white',
                        'color': 'black',
                        'border': '1px solid black',
                        'borderRadius': '5px',
                        'cursor': 'pointer',
                        'fontSize': '16px'
                    })
                ], style={'textAlign': 'center', 'marginTop': '20px'})
            ], style={'flex': '1', 'padding': '10px'})
        ], style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'flex-start'})
    ])