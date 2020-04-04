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

options1 = [
    {'label': 'Daily New Cases', 'value': 'Daily New Cases'},
    {'label': 'Total Cases', 'value': 'Total Cases'},
    {'label': 'Total Cases (Logarithm)', 'value': 'Total Cases (Logarithm)'},
]

total = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
deaths = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")
recovered = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv")

totalCasesWorldWide = total.iloc[:,-1].sum()
totalDeathsWorldWide = deaths.iloc[:,-1].sum()
totalRecoveredWorldWide = recovered.iloc[:,-1].sum()
totalActiveWorldWide = totalCasesWorldWide - totalDeathsWorldWide - totalRecoveredWorldWide

# Number of Days
dates = total.columns[4:].tolist()

# Cumulative Records
eachDayRecords = total.iloc[:,4:].sum().tolist()

# For Bar Graph
forBarGraphEachDayRecords = np.ediff1d(eachDayRecords, to_begin=eachDayRecords[0])

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([

    # Heading Element
    html.H1("Covid-19 World Dashboard"),

    # Div For Overview of Total, Death, etc
    html.Div([
        html.Div([
            # For Total Cases World Wide
            html.Div([
                html.Div([
                    html.Div([
                        html.H5("Total"),
                        html.H6(totalCasesWorldWide)
                    ], className="card-body bg-info txt-light")
                ], className="card")
            ], className="col-md-3"),

            # For Total Active Cases World Wide
            html.Div([
                html.Div([
                    html.Div([
                        html.H5("Active"),
                        html.H6(totalActiveWorldWide)
                    ], className="card-body bg-warning txt-light")
                ], className="card")
            ], className="col-md-3"),

            # For Total Recovered Cases World Wide
            html.Div([
                html.Div([
                    html.Div([
                        html.H5("Recovered"),
                        html.H6(totalRecoveredWorldWide)
                    ], className="card-body bg-success txt-light")
                ], className="card")
            ], className="col-md-3"),

            # For Total Death Cases World Wide
            html.Div([
                html.Div([
                    html.Div([
                        html.H5("Deaths"),
                        html.H6(totalDeathsWorldWide)
                    ], className="card-body bg-danger txt-light")
                ], className="card")
            ], className="col-md-3")
        ], className="row")
    ], className="container"),

    html.Hr(),

    # For Graphs briefing World Wide Records
    html.Div([
        html.Div([

            # Graphs Related To Total Number Of Cases
            html.Div([
                dcc.Dropdown(id='totalCaseGraphType', options=options1, value="All"),
                dcc.Graph(id='totalCaseGraph')
            ], className="col-md-6 padding-align"),

            html.Div([], className="col-md-6 padding-align")

        ], className="row")
    ], className="container")

])

@app.callback(Output('totalCaseGraph', 'figure'), [Input('totalCaseGraphType', 'value')])
def totalcasegraphplot(type) :
    if(type == "Total Cases (Logarithm)"):
        return {
            'data': [go.Scatter(
                x=dates,
                y=eachDayRecords,
                mode='lines+markers',
            )],
            'layout': go.Layout({
                'yaxis':dict(
                    type='log',
                    autorange=True
                ),
                'title': 'Total Cases (Logarithm)'
            })
        }
    elif(type=="Total Cases"):
        return {
            'data': [go.Scatter (
                x=dates,
                y=eachDayRecords,
                mode='lines+markers')],
            'layout': go.Layout({
                'title': 'Total Cases'
            })
        }
    else:
        return {
            'data': [go.Bar(
                x=dates,
                y=forBarGraphEachDayRecords
            )],
            'layout': go.Layout({
                'title': 'Daily New Cases'
            })
        }

if __name__=="__main__":
   app.run_server(debug=True)