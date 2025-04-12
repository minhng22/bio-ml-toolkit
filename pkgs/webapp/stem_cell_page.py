from dash import html, dcc

def stem_cell_page():
    return html.Div([
        html.H1("Predict Stem Cell Differentiation", style={'textAlign': 'center', 'fontSize': '24px'}),
        html.Div([
            html.Div([
                html.P("This page allows you to predict stem cells differentiation.", style={'textAlign': 'left', 'marginLeft': '10px', 'fontSize': '16px'})
            ], style={'flex': '0.5', 'padding': '10px'}),
            html.Div([
                html.Label("Upload Stem Cell Pictures:", style={'fontSize': '16px'}),
                dcc.Upload(
                    id='upload-stem-cell',
                    children=html.Div([
                        'Drag and Drop or ',
                        html.A('Select Files', style={'fontSize': '16px'})
                    ]),
                    style={
                        'width': '100%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '10px 0',
                        'fontSize': '16px'
                    },
                    multiple=True
                ),
                html.Button("🚀 Predict", id="predict-button", style={
                    'marginTop': '10px',
                    'padding': '10px 20px',
                    'backgroundColor': 'white',
                    'color': 'black',
                    'border': '1px solid black',
                    'borderRadius': '5px',
                    'cursor': 'pointer',
                    'fontSize': '16px'
                })
            ], style={'flex': '1', 'textAlign': 'center', 'padding': '10px'})
        ], style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'flex-start'})
    ], style={'fontFamily': 'Arial, sans-serif', 'fontSize': '16px'})