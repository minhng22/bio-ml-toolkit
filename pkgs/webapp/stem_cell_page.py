from dash import html, dcc, Input, Output, State, Dash
import base64
import os
from io import BytesIO
from PIL import Image
from pkgs.stemcellprediction.experiment.main import run_model
from pkgs.stemcellprediction.experiment.types import SupportedModel

app = Dash(__name__, suppress_callback_exceptions=True)

uploaded_images = []

def handle_file_upload(contents, filename):
    _, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    image = Image.open(BytesIO(decoded))

    save_path = os.path.join("/tmp", filename)
    image.save(save_path)
    uploaded_images.append(save_path)

def stem_cell_page():
    return html.Div([
        html.H1("Predict Stem Cell Differentiation", style={'textAlign': 'center', 'fontSize': '24px'}),
        html.Div([
            html.Div([
                html.P("StemCellNet provides a simplistic user interface to predict stem cell differentiation. Upload images of stem cells and leverage state-of-the-art machine learning models to classify their differentiation states with precision.", style={'textAlign': 'left', 'fontSize': '16px', 'marginLeft': '10px'})
            ], style={'flex': '0.5', 'padding': '10px'}),
            html.Div([
                html.Div([
                    html.Label("Choose a Model:", style={'fontSize': '16px'}),
                    dcc.Dropdown(
                        id='model-dropdown',
                        options=[
                            {'label': 'ResNet50 (pre-trained)', 'value': SupportedModel.PT_RESNET50.value},
                            {'label': 'InceptionV3 (pre-trained)', 'value': SupportedModel.PT_INCEPTIONV3.value},
                            {'label': 'EfficientNet (pre-trained)', 'value': SupportedModel.PT_EFFICIENTNET.value},
                            {'label': 'VGG16 (pre-trained)', 'value': SupportedModel.PT_VGG16.value}
                        ],
                        placeholder="Select a model",
                        style={
                            'width': '100%',
                            'marginBottom': '10px',
                            'fontSize': '16px'
                        }
                    )
                ], style={'marginBottom': '20px'}),
                html.Label("Upload Stem Cell Pictures:", style={'fontSize': '16px'}),
                dcc.Upload(
                    id='upload-stem-cell',
                    children=html.Div([
                        html.P("Drag and Drop or Select Files")
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
                }),
                html.Div(id='prediction-output', style={'marginTop': '20px'})
            ], style={'flex': '1', 'textAlign': 'center', 'padding': '10px'})
        ], style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'flex-start'})
    ], style={'fontFamily': 'Arial, sans-serif', 'fontSize': '16px'})

@app.callback(
    Output('upload-stem-cell', 'children'),
    [Input('upload-stem-cell', 'contents')],
    [State('upload-stem-cell', 'filename')]
)
def update_uploaded_files(list_of_contents, list_of_names):
    if list_of_contents is not None:
        for contents, name in zip(list_of_contents, list_of_names):
            handle_file_upload(contents, name)
        return html.Div([html.P(f"Uploaded: {', '.join(list_of_names)}")])
    return html.Div([html.P("Drag and Drop or Select Files")])

@app.callback(
    Output('prediction-output', 'children'),
    [Input('predict-button', 'n_clicks')],
    [State('upload-stem-cell', 'contents'), State('model-dropdown', 'value')]
)
def update_prediction_output(n_clicks, contents, selected_model):
    if n_clicks is not None and n_clicks > 0 and contents is not None:
        print(f'Predicting for model: {selected_model} with {len(uploaded_images)} images.')
        results = run_model(selected_model, uploaded_images)
        print(f"Results: {results}")
        result_divs = []
        for result in results:
            result_divs.append(html.Div([
                html.P(f"Image: {result['image_path']}", style={'fontWeight': 'bold'}),
                html.P(f"Prediction: {result['prediction']}"),
                html.P(f"Probabilities: {result['probabilities']}")
            ]))
        return html.Div(result_divs)
    return html.Div("Upload images and click Predict.")