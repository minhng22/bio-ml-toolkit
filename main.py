import dash
from dash import dcc, html
from dash.dependencies import Input, Output

app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "ML Toolkit Showcase"

app.layout = html.Div([
    html.Button("☰", id="menu-toggle", style={
        'position': 'fixed',
        'top': '10px',
        'left': '10px',  # Moved the button back to its original position
        'zIndex': 1000,
        'backgroundColor': '#fff',
        'border': '1px solid #ddd',
        'borderRadius': '5px',
        'padding': '10px',
        'cursor': 'pointer',
        'transition': 'left 0.3s ease'  # Smooth transition for button position
    }),
    html.Nav([
        dcc.Link("Predict Stem Cell Differentiation", href="/stem-cell", style={
            'margin': '10px 0',
            'textDecoration': 'none',
            'color': 'black',
            'fontSize': '18px',
            'fontFamily': 'Arial, sans-serif'
        }),
        dcc.Link("Generate 3D Drugs", href="/3d-drugs", style={
            'margin': '10px 0',
            'textDecoration': 'none',
            'color': 'black',
            'fontSize': '18px',
            'fontFamily': 'Arial, sans-serif'
        }),
        dcc.Link("Convert Natural Language Query", href="/nl-query", style={
            'margin': '10px 0',
            'textDecoration': 'none',
            'color': 'black',
            'fontSize': '18px',
            'fontFamily': 'Arial, sans-serif'
        })
    ], id="menu-bar", style={
        'display': 'flex',
        'flexDirection': 'column',
        'alignItems': 'flex-start',
        'backgroundColor': 'white',
        'padding': '50px 10px 10px',  # Added top padding to move menu options down
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
        'transform': 'translateX(0)'
    }),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', style={
        'marginTop': '30px',
        'padding': '20px',
        'border': '1px solid #ddd',
        'borderRadius': '5px',
        'boxShadow': '0 2px 5px rgba(0, 0, 0, 0.1)',
        'maxWidth': '800px',
        'marginLeft': '220px',  # Adjusted to account for the menu bar width
        'marginRight': 'auto',
        'fontFamily': 'Arial, sans-serif'
    })
], style={
    'fontFamily': '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
    'fontSize': '16px',
    'lineHeight': '1.5',
    'color': '#333'
})

# Define the layout for each tool page
def stem_cell_page():
    return html.Div([
        html.H1("Predict Stem Cell Differentiation", style={'textAlign': 'center'})
    ])

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
        return nl_query_page()
    else:
        return html.Div("Welcome to the ML Toolkit Showcase!", style={'textAlign': 'center'})

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

# Run the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)