from dash import html
from dash import dcc

def nl_to_db_query_page():
    return html.Div([
        html.H1("Natural Language to Database Query", style={'textAlign': 'center', 'fontSize': '28px', 'marginBottom': '20px'}),
        html.Div([
            html.Div([
                html.P("QueryGen provides a powerful tool to convert natural language search queries into database queries. Select a large language model, input your search query and database schema, and generate precise database queries.", style={'textAlign': 'left', 'fontSize': '16px', 'marginLeft': '10px'})
            ], style={'flex': '0.5', 'padding': '10px'}),
            html.Div([
                html.Div([
                    html.Label("Choose a Model:", style={'fontSize': '16px'}),
                    dcc.Dropdown(
                        id='llm-model-dropdown',
                        options=[
                            {'label': 'GPT-4', 'value': 'gpt4'},
                            {'label': 'Claude', 'value': 'claude'},
                            {'label': 'LLaMA', 'value': 'llama'},
                            {'label': 'PaLM', 'value': 'palm'}
                        ],
                        placeholder="Select a model",
                        style={
                            'width': '100%',
                            'marginBottom': '10px',
                            'fontSize': '16px'
                        }
                    )
                ], style={'marginBottom': '20px'}),
                html.Label("Enter your natural language query:", style={'fontSize': '16px'}),
                dcc.Textarea(
                    id='nl-query-input',
                    placeholder='Type your search query here...',
                    style={
                        'width': '100%',
                        'height': '80px',
                        'marginBottom': '10px',
                        'fontSize': '16px'
                    }
                ),
                html.Label("Enter your database schema:", style={'fontSize': '16px'}),
                dcc.Textarea(
                    id='db-schema-input',
                    placeholder='Describe your database schema here...',
                    style={
                        'width': '100%',
                        'height': '80px',
                        'marginBottom': '10px',
                        'fontSize': '16px'
                    }
                ),
                html.Button("Generate Query", id="generate-query-button", style={
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