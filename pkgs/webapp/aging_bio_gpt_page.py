from dash import html, dcc, callback, Input, Output, State
from pkgs.aginggpt.service import process_query, get_loading_message
import time

def aging_bio_gpt_page():
    return html.Div([
        html.H1("Query Aging Biology Knowledge", style={
            'textAlign': 'center',
            'fontSize': '24px',
            'marginBottom': '20px'
        }),
        html.Div([
            html.Div([
                html.P("AgingGPT combines LLM with Retrieval-Augmented Generation (RAG) to provide accurate information about aging biology research.", style={
                    'fontSize': '16px',
                    'marginBottom': '20px',
                    'color': '#555'
                }),
                html.Div(id='loading-message', style={
                    'fontSize': '16px',
                    'color': '#888',
                    'fontStyle': 'italic',
                    'marginBottom': '10px',
                    'minHeight': '20px',
                    'textAlign': 'center'
                }),
                html.Div(id='loading-container', children=[
                    dcc.Loading(
                        id="loading-indicator",
                        type="default",
                        children=html.Div(id='response-output', style={
                            'marginTop': '20px',
                            'padding': '20px',
                            'border': '1px solid #ddd',
                            'borderRadius': '5px',
                            'backgroundColor': '#f9f9f9',
                            'fontSize': '16px',
                            'minHeight': '150px'
                        })
                    )
                ]),
                dcc.Textarea(
                    id='user-input',
                    placeholder='Ask a question about aging biology...',
                    style={
                        'width': 'calc(100% - 20px)',
                        'height': '60px',
                        'marginTop': '20px',
                        'marginBottom': '10px',
                        'fontSize': '16px',
                        'padding': '10px',
                        'border': '1px solid #ddd',
                        'borderRadius': '5px',
                        'resize': 'vertical'
                    }
                ),
                html.Div([
                    html.Button("Submit", id="submit-button", n_clicks=0, style={
                        'padding': '10px 20px',
                        'backgroundColor': '#4a86e8',
                        'color': 'white',
                        'border': 'none',
                        'borderRadius': '5px',
                        'cursor': 'pointer',
                        'fontSize': '16px',
                        'fontWeight': 'bold',
                        'marginRight': '10px'
                    }),
                    html.Button("Clear", id="clear-button", n_clicks=0, style={
                        'padding': '10px 20px',
                        'backgroundColor': 'white',
                        'color': '#555',
                        'border': '1px solid #ddd',
                        'borderRadius': '5px',
                        'cursor': 'pointer',
                        'fontSize': '16px'
                    })
                ], style={'display': 'flex', 'flexDirection': 'row'})
            ], style={
                'width': '100%',
                'padding': '20px',
                'boxSizing': 'border-box'
            })
        ], style={
            'maxWidth': '800px',
            'margin': '0 auto',
            'backgroundColor': 'white',
            'borderRadius': '8px',
            'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
            'overflow': 'hidden'
        })
    ], style={
        'fontFamily': 'Arial, sans-serif',
        'padding': '20px'
    })


@callback(
    Output('loading-message', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('user-input', 'value')],
    prevent_initial_call=True
)
def show_loading_message(n_clicks, query):
    if not query or query.strip() == "":
        return ""
    
    # Show a funny loading message
    loading_msg = get_loading_message()
    return loading_msg

@callback(
    [Output('response-output', 'children'),
     Output('loading-message', 'children', allow_duplicate=True)],
    [Input('submit-button', 'n_clicks')],
    [State('user-input', 'value')],
    prevent_initial_call=True
)
def update_response(n_clicks, query):
    if not query or query.strip() == "":
        return "Please ask a question about aging biology.", ""
    
    result = process_query(query)
    
    if result["status"] == "success":
        response = result["response"]
        
        response_content = [
            html.P("Query: ", style={'fontWeight': 'bold'}) if query else "",
            html.P(query, style={'fontStyle': 'italic'}) if query else "",
            html.Hr() if query else "",
            html.Div([
                html.P(part) for part in response.split("\n\n")
            ])
        ]
        return response_content, ""  # Clear loading message when done
    else:
        return html.P(result["response"], style={'color': 'red'}), ""

@callback(
    [Output('user-input', 'value'),
     Output('response-output', 'children', allow_duplicate=True),
     Output('loading-message', 'children', allow_duplicate=True)],
    [Input('clear-button', 'n_clicks')],
    prevent_initial_call=True
)
def clear_input(n_clicks):
    return "", html.Div("Ask a question about aging biology research to get started."), ""