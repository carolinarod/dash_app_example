
# coding: utf-8

# # Final Project
# 
# Create a Dashboard taking data from [Eurostat, GDP and main components (output, expenditure and income)](http://ec.europa.eu/eurostat/web/products-datasets/-/nama_10_gdp). 
# The dashboard will have two graphs: 
# 
# * The first one will be a scatterplot with two DropDown boxes for the different indicators. It will have also a slide for the different years in the data. 
# * The other graph will be a line chart with two DropDown boxes, one for the country and the other for selecting one of the indicators. (hint use Scatter object using mode = 'lines' [(more here)](https://plot.ly/python/line-charts/) 
# 
# 

# # Final Dashboard

# In[ ]:


import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

data = pd.read_csv('nama_10_gdp_1_Data.csv', error_bad_lines = False, engine = 'python', na_values = [':', 'NaN'])

europe_values = [
    'European Union (current composition)',
    'European Union (without United Kingdom)',
    'European Union (15 countries)',
    'Euro area (EA11-2000, EA12-2006, EA13-2007, EA15-2008, EA16-2010, EA17-2013, EA18-2014, EA19)',
    'Euro area (19 countries)',
    'Euro area (12 countries)'
            ]

data_filter = data['GEO'].isin(europe_values)
data = data.loc[~data_filter.values].reset_index(drop = True)

data['INDICATOR'] = data['NA_ITEM'] + ' (' + data['UNIT'] + ')'

available_indicators = data['INDICATOR'].unique()

data['GEO']=data['GEO'].replace(['Germany (until 1990 former territory of the FRG)'], 'Germany')
data['GEO']=data['GEO'].replace(['Kosovo (under United Nations Security Council Resolution 1244/99)'], 'Kosovo')
available_countries = data['GEO'].unique()


app = dash.Dash(__name__)
server = app.server
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

app.layout = html.Div([
    html.Div([
        html.H1(
            children = 'Final Dashbaord',
                style = {'font-family': 'Arial, Helvetica, sans-serif', 'text-align': 'center', 'color': 'SKYBLUE'}
            ),
             
    html.Div([
    ], 
        style = {'margin': '30px 10px 50px 10px', 'background-color': 'SKYBLUE', 'height': '2px'}
    ),
        
        html.H2(
            children = 'Graph 1',
                style = {'font-family': 'Arial, Helvetica, sans-serif', 'text-align': 'center'}
            ),
        html.Div([
            html.P(
                children = 'Select the first indicator:',
                style = {'font-size': 15, 'font-family': 'Arial, Helvetica, sans-serif'}
            ),
            dcc.Dropdown(
                id = 'xaxis-column',
                options = [{'label': i, 'value': i} for i in available_indicators],
                value = available_indicators[0],
            )
        ],
        style = {'width': '48%', 'display': 'inline-block'}),
        
        html.Div([
            html.P(
                children = 'Select the second indicator:',
                style = {'font-size': 15, 'font-family': 'Arial, Helvetica, sans-serif'}
            ),
            dcc.Dropdown(
                id = 'yaxis-column',
                options = [{'label': i, 'value': i} for i in available_indicators],
                value = available_indicators[1],
            )
        ],style = {'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),
   
    dcc.Graph(id = 'indicator-graphic1'),
    
    html.Div([
        dcc.Slider(
            id = 'year--slider',
            min = data['TIME'].min(),
            max = data['TIME'].max(),
            value = data['TIME'].max(),
            step = None,
            marks = {str(year): str(year) for year in data['TIME'].unique()}
        )
    ], 
        style = {'margin' : '10px 40px'}
    ),
     
    html.Div([
    ], 
        style = {'margin': '100px 10px 50px 10px', 'background-color': 'SKYBLUE', 'height': '2px'}
    ),
    
    html.Div([
        html.H2(
            children = 'Graph 2',
            style = {'font-family': 'Arial, Helvetica, sans-serif', 'text-align': 'center'}
        ),
        html.Div([
            html.P(
                children = 'Select the country:',
                style = {'font-size': 15, 'font-family': 'Arial, Helvetica, sans-serif'}
            ),
            dcc.Dropdown(
                id = 'country',
                options = [{'label': i, 'value': i} for i in available_countries],
                value = available_countries[0],
            )
        ],
        style = {'width': '48%', 'display': 'inline-block', 'height': '130px'}),

        html.Div([
            html.P(
                children = 'Select the indicator:',
                style = {'font-size': 15, 'font-family': 'Arial, Helvetica, sans-serif'}
            ),
            dcc.Dropdown(
                id = 'indicator',
                options = [{'label': i, 'value': i} for i in available_indicators],
                value = available_indicators[0],
            )
        ],style = {'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id = 'indicator-graphic2'),

])

@app.callback(
    dash.dependencies.Output('indicator-graphic1', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('year--slider', 'value')])


def update_graph(xaxis_column_name, yaxis_column_name,
                 year_value):
    dff = data[data['TIME'] == year_value]
    
    return {
        'data': [go.Scatter(
            x = dff[dff['INDICATOR'] == xaxis_column_name]['Value'],
            y = dff[dff['INDICATOR'] == yaxis_column_name]['Value'],
            text = dff[dff['INDICATOR'] == yaxis_column_name]['GEO'],
            mode = 'markers',
            marker = {
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis = {
                'title': xaxis_column_name,
            },
            yaxis = {
                'title': yaxis_column_name,
            },
            margin = {'l': 40, 'b': 40, 't': 40, 'r': 40},
            hovermode = 'closest'
        )
    }

@app.callback(
    dash.dependencies.Output('indicator-graphic2', 'figure'),
    [dash.dependencies.Input('country', 'value'),
     dash.dependencies.Input('indicator', 'value')])

def update_graph(selected_country, selected_indicator):    
    
    return {
        'data': [go.Scatter(
            x = data[(data['GEO'] == selected_country) & (data['INDICATOR'] == selected_indicator)]['TIME'].values,
            y = data[(data['GEO'] == selected_country) & (data['INDICATOR'] == selected_indicator)]['Value'].values,
            mode = 'lines'
        )],
        'layout': go.Layout(
            yaxis = {
                'title': selected_indicator,
                'titlefont': {'size': 10},
                'type': 'linear'
            },
            margin = {'l': 40, 'b': 40, 't': 40, 'r': 40},
            hovermode = 'closest'
        )
    }

if __name__ == '__main__':
    app.run_server()

