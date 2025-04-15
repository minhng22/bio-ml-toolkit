from dash import html, dcc

def aging_bio_gpt_page():
    return html.Div([
        html.H1("Query Aging Biology Knowledge", style={
            'textAlign': 'center',
            'fontSize': '24px',
            'marginBottom': '20px'
        }),
        html.Div([
            html.Div(id='response-output', style={
                'marginTop': '20px',
                'padding': '10px',
                'border': '1px solid #ddd',
                'borderRadius': '5px',
                'backgroundColor': '#f9f9f9',
                'fontSize': '16px'
            }),
            dcc.Textarea(
                id='user-input',
                placeholder='Type your question here...',
                style={
                    'width': 'calc(100% - 20px)',
                    'height': '30px',
                    'marginTop': '10px',
                    'marginBottom': '10px',
                    'fontSize': '16px',
                    'padding': '10px',
                    'border': '1px solid #ddd',
                    'borderRadius': '5px'
                }
            ),
            html.Button("Submit", id="submit-button", style={
                'padding': '10px 20px',
                'backgroundColor': 'white',
                'color': 'black',
                'border': '1px solid black',
                'borderRadius': '5px',
                'cursor': 'pointer',
                'fontSize': '16px'
            })
        ], style={
            'maxWidth': '800px',
            'margin': '0 auto'
        })
    ], style={
        'fontFamily': 'Arial, sans-serif',
        'padding': '20px'
    })