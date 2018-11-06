import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from flask import Flask
import pandas as pd

server = Flask(__name__)
app = dash.Dash(__name__, server=server)

crimedata = pd.read_csv('crimedata.csv')
features = crimedata.columns
crimetypes = features[:-1] #don't want the year column

#add markdown text
markdown_text = """
Data used for this dashboard was taken from the US Department of Justice website which can be accessed [here.](https://ucr.fbi.gov/crime-in-the-u.s/2016/crime-in-the-u.s.-2016/topic-pages/tables/table-1)
"""

app.layout = html.Div([
	html.Div([
    #Here is the interactive component
		html.Div([
			dcc.Dropdown(
				id='yaxis',
				options=[{'label':i,'value':i} for i in crimetypes],
				value='crime-type'
			)
		], style={'width': '40%'})
	]),
	html.Div([dcc.Graph(
		id='crime-graphic',
		figure={
			'data': [go.Scatter(
				x=crimedata['Year'],
				y=[0,0],
				mode='markers'
			)],
			'layout': go.Layout(
				title = 'Use the dropdown to display the chart ...',
				xaxis={'tickformat': 'd'}
			)
		}
		)
	], style={'width':'50%', 'display':'inline-block'}),
	html.Div([dcc.Graph(
		id='crime-stacked',
		figure={
			'data': [go.Bar(
				x=crimedata['Year'],
				y=crimedata['Assault'],
				name='Assault'
				),
				go.Bar(
                                x=crimedata['Year'],
                                y=crimedata['Burglary'],
                                name='Burglary'
                                ),
				go.Bar(
                                x=crimedata['Year'],
                                y=crimedata['Larceny'],
                                name='Larceny'
                                ),
				go.Bar(
                                x=crimedata['Year'],
                                y=crimedata['Murder'],
                                name='Murder'
                                ),
				go.Bar(
                                x=crimedata['Year'],
                                y=crimedata['Property_Crime'],
                                name='Property Crime'
                                ),
				go.Bar(
                                x=crimedata['Year'],
                                y=crimedata['Rape'],
                                name='Rape'
                                ),
				go.Bar(
                                x=crimedata['Year'],
                                y=crimedata['Robbery'],
                                name='Robbery'
                                ),
				go.Bar(
                                x=crimedata['Year'],
                                y=crimedata['Vehicle_Theft'],
                                name='Vehicle Theft'
                                ),
				go.Bar(
                                x=crimedata['Year'],
                                y=crimedata['Violent_Crime'],
                                name='Violent Crime'
                                ) 
			],
			'layout': go.Layout(
				title ='Crime in the United States by Volume, 1997–2016',
				barmode='stack'
			)
		}
		)
	], style={'width':'50%', 'display':'inline-block'}),
	html.Div([dcc.Graph(
		id='crime-boxplot',
		figure={
			'data': [go.Box(
			y=crimedata['Assault'],
			name='Assault'
			),
			go.Box(
                        y=crimedata['Burglary'],
                        name='Burglary'
                        ),
			go.Box(
                        y=crimedata['Larceny'],
                        name='Larceny'
                        ),
			go.Box(
                        y=crimedata['Murder'],
                        name='Murder'
                        ),
			go.Box(
                        y=crimedata['Property_Crime'],
                        name='Property Crime'
                        ),
			go.Box(
                        y=crimedata['Rape'],
                        name='Rape'
                        ),
			go.Box(
                        y=crimedata['Robbery'],
                        name='Robbery'
                        ),
			go.Box(
                        y=crimedata['Vehicle_Theft'],
                        name='Vehicle Theft'
                        ),
			go.Box(
                        y=crimedata['Violent_Crime'],
                        name='Violent Crime'
                        ),
			],
			'layout': go.Layout(
			title='Crime in the United States by Volume, 1997–2016'
			)
		}
	)
	], style={'width':'50%', 'display':'inline-block'}),
	html.Div([
		dcc.Markdown(children=markdown_text)
	])
], style={'padding':10})

#Here is the callback
@app.callback(
	Output('crime-graphic', 'figure'),
	[Input ('yaxis', 'value')])
def update_graphic(yaxis_crime):
	return {
		'data': [go.Scatter(
			x=crimedata['Year'],
			y=crimedata[yaxis_crime],
			mode='lines+markers',
			marker={
				'size': 15,
				'opacity': 0.5,
				'line': {'width':0.5, 'color':'white'}
			}
		)],
		'layout': go.Layout(
			title='{} in the US by Volume, 1997-2016'.format(yaxis_crime),
			xaxis={'title': 'Year'},
			yaxis={'title': yaxis_crime},
			hovermode='closest'
		)
	}


if __name__ == '__main__':
	app.run_server(debug=True)
