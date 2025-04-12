import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from pkgs.webapp.meldna_page import meldna_score_page
from pkgs.webapp.stem_cell_page import stem_cell_page, update_uploaded_files
from pkgs.experiment.stemcellprediction import main
from pkgs.webapp.nl_to_db_query_page import nl_to_db_query_page

app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "ML Toolkit Showcase"

app.layout = html.Div([
    html.Button("☰", id="menu-toggle", style={
        'position': 'fixed',
        'top': '10px',
        'left': '10px',
        'zIndex': 1000,
        'backgroundColor': '#fff',
        'border': '1px solid #ddd',
        'borderRadius': '5px',
        'padding': '10px',
        'cursor': 'pointer',
        'transition': 'left 0.3s ease'
    }),
    html.Nav([
        dcc.Link(html.Span("🔬 Predict MELDNa Score", style={
            'marginLeft': '5px'
        }), href="/meldna-score", style={
            'margin': '10px 0',
            'textDecoration': 'none',
            'color': 'black',
            'fontSize': '14px',
            'fontFamily': 'Arial, sans-serif'
        }),
        dcc.Link(html.Span("🔬 Classify Stem Cell Differentiation", style={
            'marginLeft': '5px'
        }), href="/stem-cell", style={
            'margin': '10px 0',
            'textDecoration': 'none',
            'color': 'black',
            'fontSize': '14px',
            'fontFamily': 'Arial, sans-serif'
        }),
        dcc.Link(html.Span("💻 NL to DB Query", style={
            'marginLeft': '5px'
        }), href="/nl-query", style={
            'margin': '10px 0',
            'textDecoration': 'none',
            'color': 'black',
            'fontSize': '14px',
            'fontFamily': 'Arial, sans-serif'
        }),
    ], id="menu-bar", style={
        'display': 'flex',
        'flexDirection': 'column',
        'alignItems': 'flex-start',
        'backgroundColor': 'white',
        'padding': '50px 10px 10px', 
        'boxShadow': '0 2px 5px rgba(0, 0, 0, 0.1)',
        'border': '1px solid transparent',
        'borderImage': 'linear-gradient(to bottom, #ffffff, #e0e0e0)',
        'borderImageSlice': 1,
        'color': 'black',
        'height': '100vh',
        'position': 'fixed',
        'top': 0,
        'left': 0,
        'width': '200px',
        'transition': 'transform 0.3s ease',
        'transform': 'translateX(0)',
        'fontSize': '10px'
    }),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', style={
        'marginTop': '30px',
        'padding': '20px',
        'border': '1px solid #ddd',
        'borderRadius': '5px',
        'boxShadow': '0 2px 5px rgba(0, 0, 0, 0.1)',
        'maxWidth': '800px',
        'marginLeft': '220px',
        'marginRight': 'auto',
        'fontFamily': 'Arial, sans-serif'
    })
], style={
    'fontFamily': '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
    'lineHeight': '1.5',
    'color': '#333'
})

def drugs_page():
    return html.Div([
        html.H1("Generate 3D Drugs", style={'textAlign': 'center'})
    ])

def nl_query_page():
    return html.Div([
        html.H1("Convert Natural Language Query", style={'textAlign': 'center'})
    ])

@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/stem-cell':
        return stem_cell_page()
    elif pathname == '/3d-drugs':
        return drugs_page()
    elif pathname == '/nl-query':
        return nl_to_db_query_page()
    elif pathname == '/meldna-score':
        return meldna_score_page()
    else:
        return html.Div("Welcome to the ML Toolkit Showcase!", style={'textAlign': 'center'})

@app.callback(
    Output('predict-button', 'n_clicks'),
    [Input('predict-button', 'n_clicks')],
    [State('model-dropdown', 'value')]
)
def call_prediction_script(n_clicks, selected_model):
    if n_clicks:
        main.run_model(selected_model)
    return None

app.callback(
    Output('upload-stem-cell', 'children'),
    [Input('upload-stem-cell', 'contents')],
    [State('upload-stem-cell', 'filename')]
)(update_uploaded_files)

app.clientside_callback(
    "function(pathname) {\n        const links = document.querySelectorAll('nav a');\n        if (!links) return pathname;\n        links.forEach(link => {\n            if (link.getAttribute('href') === pathname) {\n                link.style.border = '2px solid black';\n                link.style.borderRadius = '10px';\n                link.style.padding = '8px';\n                link.style.backgroundColor = '#f0f0f0';\n                link.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';\n            } else {\n                link.style.border = 'none';\n                link.style.padding = '0';\n                link.style.backgroundColor = 'transparent';\n                link.style.boxShadow = 'none';\n            }\n        });\n        return pathname;\n    }",
    Output('url', 'pathname'),
    [Input('url', 'pathname')]
)

app.clientside_callback(
    "function(n_clicks) {\n        const menu = document.getElementById('menu-bar');\n        if (menu) {\n            if (menu.style.transform === 'translateX(-100%)') {\n                menu.style.transform = 'translateX(0)';\n            } else {\n                menu.style.transform = 'translateX(-100%)';\n            }\n        }\n        return null;\n    }",
    Output('menu-toggle', 'n_clicks'),
    [Input('menu-toggle', 'n_clicks')]
)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)