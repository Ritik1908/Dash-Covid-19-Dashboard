import numpy as np
import pandas as pd
import plotly.graph_objects as go
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

# external CSS stylesheets
external_stylesheets = [
   {
       'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
       'rel': 'stylesheet',
       'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
       'crossorigin': 'anonymous'
   }
]

patients=pd.read_csv('Data/IndividualDetails.csv')
total=patients.shape[0]
active=patients[patients['current_status']=='Hospitalized'].shape[0]
recovered=patients[patients['current_status']=='Recovered'].shape[0]
deaths=patients[patients['current_status']=='Deceased'].shape[0]

options=[
    {'label':'All', 'value':'All'},
    {'label':'Hospitalized', 'value':'Hospitalized'},
    {'label':'Recovered', 'value':'Recovered'},
    {'label':'Deceased', 'value':'Deceased'}
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1("Covid-19"),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Total", className="text-light"),
                    html.H4(total, className="text-light")
                ], className="card-body")
            ], className="card bg-danger")
        ], className="col-md-3"),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Active", className="text-light"),
                    html.H4(active, className="text-light")
                ], className="card-body")
            ], className="card bg-info")
        ], className="col-md-3"),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Recovered", className="text-light"),
                    html.H4(recovered, className="text-light")
                ], className="card-body")
            ], className="card bg-warning")
        ], className="col-md-3"),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Deaths", className="text-light"),
                    html.H4(deaths, className="text-light")
                ], className="card-body")
            ], className="card bg-success")
        ], className="col-md-3")
    ], className="row"),
    html.Div([], className="row"),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id='picker', options=options, value="All"),
                    dcc.Graph(id='bar')
                ], className="card-body")
            ], className="card")
        ], className="col-md-12")
    ], className="row")
], className="container")

@app.callback(Output('bar','figure'), [Input('picker','value')])
def update_graph(type):
    if type=='All':
        pbar = patients['detected_state'].value_counts().reset_index()
        return {'data':[go.Bar(x=pbar['index'], y=pbar['detected_state'])],
           'layout':go.Layout(title='State Total Count')}
    else:
       npat = patients[patients['current_status'] == type]
       pbar = npat['detected_state'].value_counts().reset_index()
       return {'data': [go.Bar(x=pbar['index'], y=pbar['detected_state'])],
            'layout': go.Layout(title='State Total Count')}

if __name__=="__main__":
   app.run_server(debug=True)