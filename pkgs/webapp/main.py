import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from pkgs.webapp.meldna_page import meldna_score_page
from pkgs.webapp.stem_cell_page import stem_cell_page, update_uploaded_files, update_prediction_output
from pkgs.webapp.aging_bio_gpt_page import aging_bio_gpt_page

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
        dcc.Link(html.Span("🔬 Query Aging Biology Knowledge", style={
            'marginLeft': '5px'
        }), href="/aging-bio-gpt", style={
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
    dcc.Store(id='current-pathname'),
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

@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/stem-cell':
        return stem_cell_page()
    elif pathname == '/meldna-score':
        return meldna_score_page()
    elif pathname == '/aging-bio-gpt':
        return aging_bio_gpt_page()
    else:
        return html.Div(
            "🌟 Explore advanced machine learning tools for predictive modeling and data analysis. 🌟",
            style={'textAlign': 'center'}
        )

app.callback(
    Output('upload-stem-cell', 'children'),
    [Input('upload-stem-cell', 'contents')],
    [State('upload-stem-cell', 'filename')]
)(update_uploaded_files)

app.callback(
    Output('prediction-output', 'children'),
    [Input('predict-button', 'n_clicks')],
    [State('upload-stem-cell', 'contents'), State('model-dropdown', 'value')]
)(update_prediction_output)

app.clientside_callback(
    """
    function(pathname) {
        const links = document.querySelectorAll('nav a');
        links.forEach(link => {
            if (link.getAttribute('href') === pathname) {
                link.style.border = '2px solid black';
                link.style.borderRadius = '10px';
                link.style.padding = '8px';
                link.style.backgroundColor = '#f0f0f0';
                link.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';
            } else {
                link.style.border = 'none';
                link.style.padding = '0';
                link.style.backgroundColor = 'transparent';
                link.style.boxShadow = 'none';
            }
        });
        return pathname;
    }
    """,
    Output('current-pathname', 'data'),
    [Input('url', 'pathname')]
)

app.clientside_callback(
    """
    function(n_clicks) {
        const menu = document.getElementById('menu-bar');
        if (menu) {
            if (menu.style.transform === 'translateX(-100%)') {
                menu.style.transform = 'translateX(0)';
            } else {
                menu.style.transform = 'translateX(-100%)';
            }
        }
        return null;
    }
    """,
    Output('menu-toggle', 'n_clicks'),
    [Input('menu-toggle', 'n_clicks')]
)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
