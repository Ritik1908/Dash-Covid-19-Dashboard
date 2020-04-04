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

# For Death and Recovered Plot
eachDayRecovered = recovered.iloc[:,4:].sum().tolist()
eachDayDeath = deaths.iloc[:,4:].sum().tolist()

# To Remove Duplicate Values
def unique(x):
  return list(dict.fromkeys(x))
country = total["Country/Region"].tolist()
country = unique(country)

options2 = []
for i in country:
    options2.append({'label':i, 'value':i})


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

            # Graph showing rise in death and recovery
            html.Div([
                dcc.Graph(figure={
                    'data' : [
                        go.Scatter(
                            x=dates,
                            y=eachDayRecovered,
                            mode='lines+markers',
                            marker={'color': 'green'},
                            name='Recovered'
                        ),
                        go.Scatter(
                            x=dates,
                            y=eachDayDeath,
                            mode='lines+markers',
                            marker={'color': 'red'},
                            name='Death'
                        )
                    ],
                    'layout': go.Layout({
                        'title': 'Death vs Recovery'
                    })
                })
            ], className="col-md-6 padding-align")

        ], className="row")
    ], className="container"),

    html.Hr(),

    html.H2("Country/Region Wise Graphical Analysis"),

    # For Country Wise Analysis
    html.Div([

        # Drop Down To Control All Type Of Graph
        html.Div([
            html.Div([
                dcc.Dropdown(id="country", options=options2, value="All")
            ], className="col-12")
        ], className="row"),

        # For Total Number Of Active Cases
        html.Div([

            # Bar
            html.Div([
                dcc.Graph(id='displayBarTotal')
            ], className="col-6 padding-align"),

            # Linear
            html.Div([
                dcc.Graph(id='displayLinearTotal')
            ], className="col-6 padding-align")

        ], className="row"),

        # For Total Number Of Recovered Cases
        html.Div([

            # Bar
            html.Div([
                dcc.Graph(id='displayBarRecovered')
            ], className="col-6 padding-align"),

            # Linear
            html.Div([
                dcc.Graph(id='displayLinearRecovered')
            ], className="col-6 padding-align")

        ], className="row"),

        # For Total Number Of Death Cases
        html.Div([

            # Bar
            html.Div([
                dcc.Graph(id='displayBarDeath')
            ], className="col-6 padding-align"),

            # Linear
            html.Div([
                dcc.Graph(id='displayLinearDeath')
            ], className="col-6 padding-align")

        ], className="row")

    ], className="container")
])

# Graph Selector For Total Number Of Cases
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

# Bar Graph For Total Cases
@app.callback(Output('displayBarTotal', 'figure'), [Input('country', 'value')])
def displayBarTotal(type) :
    if(type == "All"):
        return {
            'data': [go.Bar(
                x=dates,
                y=forBarGraphEachDayRecords
            )],
            'layout': go.Layout({
                'title': 'Daily New Cases'
            })
        }
    else:
        xD = total[total["Country/Region"] == type]
        eachDay = xD.iloc[:, 4:].sum().tolist()
        forBarGraph = np.ediff1d(eachDay, to_begin=eachDay[0])
        return {

            'data': [go.Bar(
                x=dates,
                y=forBarGraph
            )],
            'layout': go.Layout({
                'title': 'Daily New Cases'
            })
        }

# Linear Graph For Total Cases
@app.callback(Output('displayLinearTotal', 'figure'), [Input('country', 'value')])
def dispLinearTotal(type) :
    if(type == "All"):
        return {
            'data': [go.Scatter(
                x=dates,
                y=eachDayRecords,
                mode='lines+markers',
            )],
            'layout': go.Layout({
                'title': 'New Cases Trend'
            })
        }
    else:
        xD = total[total["Country/Region"] == type]
        eachDay = xD.iloc[:, 4:].sum().tolist()
        return {

            'data': [go.Scatter(
                x=dates,
                y=eachDay,
                mode='lines+markers',
            )],
            'layout': go.Layout({
                'title': 'Daily New Cases Trend'
            })
        }

# Bar Graph For Recovery Rate
@app.callback(Output('displayBarRecovered', 'figure'), [Input('country', 'value')])
def displayBarRecovered(type) :
    if(type == "All"):
        return {
            'data': [go.Bar(
                x=dates,
                y=np.ediff1d(eachDayRecovered, to_begin=eachDayRecovered[0]),
                marker={'color':'green'}
            )],
            'layout': go.Layout({
                'title': 'Daily Recovery'
            })
        }
    else:
        xD = recovered[recovered["Country/Region"] == type]
        eachDay = xD.iloc[:, 4:].sum().tolist()
        forBarGraph = np.ediff1d(eachDay, to_begin=eachDay[0])
        return {

            'data': [go.Bar(
                x=dates,
                y=forBarGraph,
                marker={'color': 'green'}
            )],
            'layout': go.Layout({
                'title': 'Daily Recovery'
            })
        }

# Linear Graph For Recovery Rate
@app.callback(Output('displayLinearRecovered', 'figure'), [Input('country', 'value')])
def dispLinearRecovered(type) :
    if(type == "All"):
        return {
            'data': [go.Scatter(
                x=dates,
                y=eachDayRecovered,
                mode='lines+markers',
                marker={'color': 'green'}
            )],
            'layout': go.Layout({
                'title': 'Recovery Trend'
            })
        }
    else:
        xD = recovered[recovered["Country/Region"] == type]
        eachDay = xD.iloc[:, 4:].sum().tolist()
        return {

            'data': [go.Scatter(
                x=dates,
                y=eachDay,
                mode='lines+markers',
                marker={'color': 'green'}
            )],
            'layout': go.Layout({
                'title': 'Recovery Trend'
            })
        }

# Bar Graph For Death Rate
@app.callback(Output('displayBarDeath', 'figure'), [Input('country', 'value')])
def displayBarDeath(type) :
    if(type == "All"):
        return {
            'data': [go.Bar(
                x=dates,
                y=np.ediff1d(eachDayDeath, to_begin=eachDayDeath[0]),
                marker={'color':'red'}
            )],
            'layout': go.Layout({
                'title': 'Daily Death'
            })
        }
    else:
        xD = deaths[deaths["Country/Region"] == type]
        eachDay = xD.iloc[:, 4:].sum().tolist()
        forBarGraph = np.ediff1d(eachDay, to_begin=eachDay[0])
        return {

            'data': [go.Bar(
                x=dates,
                y=forBarGraph,
                marker={'color': 'red'}
            )],
            'layout': go.Layout({
                'title': 'Daily Death'
            })
        }

# Linear Graph For Death Rate
@app.callback(Output('displayLinearDeath', 'figure'), [Input('country', 'value')])
def dispLinearDeath(type) :
    if(type == "All"):
        return {
            'data': [go.Scatter(
                x=dates,
                y=eachDayDeath,
                mode='lines+markers',
                marker={'color': 'red'}
            )],
            'layout': go.Layout({
                'title': 'Death Trend'
            })
        }
    else:
        xD = deaths[deaths["Country/Region"] == type]
        eachDay = xD.iloc[:, 4:].sum().tolist()
        return {

            'data': [go.Scatter(
                x=dates,
                y=eachDay,
                mode='lines+markers',
                marker={'color': 'green'}
            )],
            'layout': go.Layout({
                'title': 'Death Trend'
            })
        }

if __name__=="__main__":
   app.run_server(debug=True)