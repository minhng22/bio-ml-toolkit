from dash import html

def meldna_score_page():
    return html.Div(
        style={
            'fontFamily': 'Arial, sans-serif',
            'margin': '0 auto',
            'maxWidth': '800px',
            'padding': '20px'
        },
        children=[
            html.H2(
                "A predictive tool to forecast the Model for End-Stage Liver Disease score: the “MELDPredict” tool",
                style={'textAlign': 'center', 'fontWeight': 'normal', 'color': '#34495e'}
            ),
            html.Div(
                style={
                    'display': 'flex',
                    'flexWrap': 'wrap',
                    'gap': '20px',
                    'marginTop': '20px'
                },
                children=[
                    html.Div(
                        style={'flex': '1', 'minWidth': '250px'},
                        children=[
                            html.P(
                                [
                                    html.Strong("Minh Nguyen"),
                                    ", Jiaqi Zhou, Sisi Ma, Gyorgy Simon, Sawyer Olson, Timothy Pruett, Lisiane Pruinelli"
                                ],
                                style={'fontStyle': 'italic', 'color': '#7f8c8d', 'marginBottom': '10px'}
                            ),
                            html.P(
                                "Journal of Medical Artificial Intelligence, 2025",
                                style={'fontWeight': 'bold', 'color': '#2c3e50'}
                            )
                        ]
                    ),
                    html.Div(
                        style={'flex': '1', 'minWidth': '250px'},
                        children=[
                            html.P(
                                "MELDPredict leverages state‑of‑the‑art time-series prediction machine learning models to forecast future MELDNa scores for end‑stage liver disease patients, "
                                "helping clinicians optimize timing for transplant preparation and patient planning.",
                                style={'lineHeight': '1.6', 'color': '#2c3e50'}
                            )
                        ]
                    )
                ]
            ),
            html.Div([
                html.A(
                    "📄 Download full paper (PDF)",
                    href="https://jmai.amegroups.org/article/view/9755/pdf",
                    target="_blank",
                    style={
                        'display': 'inline-block',
                        'padding': '5px 10px',
                        'backgroundColor': 'white',
                        'color': 'black',
                        'border': '2px solid black',
                        'borderRadius': '5px',
                        'textDecoration': 'none',
                        'fontSize': '14px',
                        'marginRight': '10px'
                    }
                ),
                html.A(
                    "🚀 Try the live MELDPredict tool",
                    href="https://ml-meld-prediction.onrender.com",
                    target="_blank",
                    style={
                        'display': 'inline-block',
                        'padding': '5px 10px',
                        'backgroundColor': 'white',
                        'color': 'black',
                        'border': '2px solid black',
                        'borderRadius': '5px',
                        'textDecoration': 'none',
                        'fontSize': '14px',
                        'marginRight': '10px'
                    }
                ),
                html.A(
                    "🔗 View code repo",
                    href="https://github.com/minhng22/uiuc-kidney-failure",
                    target="_blank",
                    style={
                        'display': 'inline-block',
                        'padding': '5px 10px',
                        'backgroundColor': 'white',
                        'color': 'black',
                        'border': '2px solid black',
                        'borderRadius': '5px',
                        'textDecoration': 'none',
                        'fontSize': '14px'
                    }
                )
            ], style={'textAlign': 'center', 'margin': '30px 0'}),
            html.Div(
                [
                    html.H3("How to Cite This Paper", style={'marginTop': '0', 'color': '#2c3e50'}),
                    html.P(
                        "Nguyen M, Zhou J, Ma S, Simon G, Olson S, Pruett T, Pruinelli L. "
                        "A predictive tool to forecast the Model for End‑Stage Liver Disease score: the “MELDPredict” tool. "
                        "J Med Artif Intell. 2025; doi:10.21037/jmai-24-277",
                        style={'fontFamily': 'Courier New, monospace', 'whiteSpace': 'pre-wrap'}
                    )
                ],
                style={
                    'backgroundColor': '#ecf0f1',
                    'padding': '15px',
                    'borderRadius': '5px',
                    'borderLeft': '4px solid #2980b9'
                }
            )
        ]
    )
