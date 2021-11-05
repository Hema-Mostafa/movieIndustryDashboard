import math
from dash.html.Legend import Legend
import numpy as np
import matplotlib.pyplot as plt
from plotly.express import data
import seaborn as sns
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
from dash.html.H1 import H1
from numpy.lib.arraysetops import isin
import plotly.express as px
import pandas as pd
import plotly.offline as pyo
import math
# bootstrab setup
import dash_bootstrap_components as dbc
import pycountry_convert as pc

from utils import *


# Build Layout with Bootstrap framework
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP] ,suppress_callback_exceptions=True)


movie_df = pd.read_csv('movies.csv/movies.csv')

# remove nan rows
movie_df.dropna(inplace=True)
movie_df.drop_duplicates(inplace=True)

# edit Datatype of budget,groos  Column
movie_df['budget'] = movie_df['budget'].astype('int64')
movie_df['gross'] = movie_df['gross'].astype('int64')

# add profit column to dataset
movie_df['profit'] = movie_df['gross'] - movie_df['budget']

# add Continent Column to dataset
movie_df['continent'] = movie_df['country'].apply(add_continent)
movie_df = movie_df[movie_df['continent'] != '0']


# the main 3 number to appear in dashboard
total_movies = movie_df['name'].count()

total_budget = movie_df['budget'].sum() / 10000000000
total_budget = round(total_budget , 2)

total_revneu =  movie_df['gross'].sum() / 10000000000
total_revneu = round(total_revneu , 2)


# # # create bar plot of gross vs budget lineplot
# gross_vs_budget_line = px.line(movie_df.groupby('year').agg(
#     {'gross': 'mean', 'budget': 'mean'}) , width=450, height=400)

# gross_vs_budget_line.update_layout(legend=dict(
#     yanchor="top",
#     y=0.99,
#     xanchor="left",
#     x=0.01
# ) , legend_title_text='Trend')


# # create bar plot of gross vs budget Barplot
# gross_vs_budget_bar = px.bar(movie_df.groupby('year')['budget', 'gross'].mean(), height=300,
#                              title="Gross vs Budget" ,  template='plotly_white')


# filter_movies = filter_with_genre(movie_df)
# grouped_filtered_movies = filter_movies.groupby(['genre','year'] , as_index=False).sum()

# # #create line plot of most 6 films kind
# grouped_filtered_movies_plot = px.line(grouped_filtered_movies , x = 'year' , y = 'profit' , height=300 , 
# color='genre' , title='Most Six Films Kind' , template='plotly_white')


app.layout =html.Div([
    html.Div(
        html.H2("Movie Industry Dashboard (1980 - 2020)", className='text-left')
        , className="container-fluid"),
    html.Div([
       
        html.Div([
            html.Div([
                html.H5('Total Movies', className='text-center'),
                html.Span("{0}".format(total_movies), className='text-center'),
        ], className='card posotion-card-1'),
        html.Div([
            html.H5('Total Budget', className='text-center'),
            html.Span("{0}B $".format(total_budget), className='text-center'),
        ], className='card posotion-card-2'),

        html.Div([
            html.H5('Total Revenue', className='text-center'),
            html.Span("{0}B $".format(total_revneu), className='text-center'),
        ], className='card posotion-card-3'),
    ], className='d-flex justify-content-between'),

    html.Div([
        html.Div([
             dcc.RangeSlider(
                    id='my-range-slider',
                    min=movie_df['year'].min(),
                    max=movie_df['year'].max(),
                    step=None,
                    marks=create_slider_year_range(movie_df['year'].unique()),
                    value=[movie_df['year'].min(), movie_df['year'].max()]
                )]
            ,className='col-md-5 slider-div'),
        html.Div([
              dcc.Dropdown(
                    id='continent-drop',
                    options=[{'label': i, 'value': i} for i in movie_df['continent'].unique()],
                    value=None,
                    multi=True),
            ],className='col-md-3 slider-div'),
        html.Div([
            html.Span("From " ,className="from-text" ),
            html.Span("1980 " ,className="from-date" , id="from-date-id"),
            html.Span("To " ,className="to-text"),
            html.Span("2020 " ,className="to-date" , id='to-date-id'),
        ],className='col-md-4 slider-div'),
    ],className='row'),
    # Div of Tabs
    html.Div([
       dcc.Tabs(id="tabs-example-graph", value='tab-1-example-graph', children=[
            dcc.Tab(label='Money', value='tab-1-example-graph' , className='nav-item custome-nav-item'),
            dcc.Tab(label='Stakeholders', value='tab-2-example-graph' , className='nav-item custome-nav-item'),
    ] , className='nav nav-pills'),
    html.Div(id='tabs-content-example-graph'),

    ]),
   
], className='container')
])


@app.callback(Output('tabs-content-example-graph', 'children'),
              Input('tabs-example-graph', 'value'))

def render_content(tab):
    if tab == 'tab-1-example-graph':
        
        return html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.H5('Budget', className='text-center h5-custome'),
                        html.Span("", className='text-center span-custome' , id='budget-span'),
                    ],className='custome-col')
                ],className='col-md-4 '),
                html.Div([
                    html.Div([
                        html.H5('Revenue', className='text-center h5-custome'),
                        html.Span("", className='text-center span-custome' , id='revenue-span'),
                    ],className='custome-col')
                ],className='col-md-4 '),
                html.Div([
                    html.Div([
                        html.H5('Profits', className='text-center h5-custome'),
                        html.Span("", className='text-center span-custome',id='profits-span' ),
                    ],className='custome-col')
                ],className='col-md-4 '),

            ],className= 'row custom-row'),
            html.Div([
                html.Div([
                    dcc.Graph(
                        # figure= gross_vs_budget_line,
                        id='gross_vs_budget_plot-id',
                        className='center-graph'),
        
                ],className='col-md-5 mg-r'),
                html.Div([],className='col-md-1'),
                    html.Div([
                        dcc.Graph(
                            # figure=grouped_filtered_movies_plot,
                            id='genre-plot-id',
                            className='center-graph',   
                    )],className='col-md-5 mg-l'),
            ],className='row row-custome'),
            html.Div([
                html.Div([
                    dcc.Graph(
                            id='map-id',
                            className='center-graph',
                )],className="col-md-7"),
               
                html.Div([
                    dcc.Graph(
                        id= 'genre-pie-id'
                    )
                ],className="col-md-5")
            ],className = 'row row-custome'),
          
        ])
    elif tab == 'tab-2-example-graph':
        return html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(
                        figure = create_genre_barplot(movie_df),
                        id='genre-count-barplot-id',
                        className='center-graphs',
                )],className = 'col-md-6'),
                html.Div([

                    dcc.Graph(
                        figure = create_genre_score_barplot(movie_df),
                        id='genre-idscore-id',
                        className='center-graphs',
                )
                ],className = 'col-md-6')
            ],className='row row-custome'),

            html.Div([
                html.Div([
                    dcc.Graph(
                        figure = create_company_realesed_barplot(movie_df),
                        id='company-realesed-id',
                        className='center-graphs')
                ],className='col-md-6'),
                html.Div([
                    dcc.Graph(
                        figure = create_country_realesed_barplot(movie_df),
                        id='country-realesed-id',
                        className='center-graphs')
                ],className='col-md-6'),
            ],className = "row row-custome")

        ])


@app.callback(

    Output(component_id='budget-span'  , component_property='children'),
    Output(component_id='revenue-span'  , component_property='children'),
    Output(component_id='profits-span'  , component_property='children'),
    
    Output(component_id='gross_vs_budget_plot-id'  , component_property='figure'),
    Output(component_id='genre-plot-id'  , component_property='figure'),
    Output(component_id='map-id'  , component_property='figure'),
    Output(component_id='genre-pie-id'  , component_property='figure'),
    Output(component_id='from-date-id'  , component_property='children'),
    Output(component_id='to-date-id'  , component_property='children'),

    Input(component_id='my-range-slider', component_property='value'),
    Input(component_id='continent-drop', component_property='value'),
    # Input(component_id='genre-count-barplot-id', component_property='figure'),

)

def update_view(range_value , continentList):

    if not continentList:
        new_movies = movie_df[(movie_df['year'] >= range_value[0]) &
                        (movie_df['year'] <= range_value[1])]

    else:
        new_movies = movie_df[(movie_df['year'] >= range_value[0]) &
                        (movie_df['year'] <= range_value[1]) & movie_df['continent'].isin(continentList)]


    total_budget = new_movies['budget'].sum() / 10000000000
    total_budget = str(round(total_budget , 2)) + "B $"

    total_revneu =  new_movies['gross'].sum() / 10000000000
    total_revneu = str(round(total_revneu , 2)) + "B $"

    total_profit = new_movies['profit'].sum() / 10000000000
    total_profit = str(round(total_profit , 2)) + "B $"

    # create line plot of gross vs budget 
    gross_vs_budget_line_fig = px.line(new_movies.groupby('year').agg(
        {'gross': 'mean', 'budget': 'mean'}) , width=500, height=400 ,labels={
            "year":"Year",
            "value":"Money (million)"
        } , template='plotly_white' , title="Budget and Gross over Years")

    gross_vs_budget_line_fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ) , legend_title_text='Budget vs Gross')

    #filter movies based on genre (movie kind)
    movies_after_genre_filter = filter_with_genre(new_movies)

    #create line plot of most 6 films kind
    movies_after_genre_filter_fig = px.line( movies_after_genre_filter.groupby(['genre','year'] , as_index=False).sum(),
     width=500, height=400,color='genre' ,  
     x ='year' , y = 'profit', template='plotly_white' , title = "Most 6 kind of Films with profit")

    # get map_fig
    map_fig = get_map_fig(new_movies)

    # get piechart fig of genre by profits
    genre_piechart_fig = create_genre_piechart(new_movies)

    # get barplot of genre  films counts

    to_span = range_value[1]
    from_span = range_value[0]

    print('Hello')
    any_fig = create_genre_barplot(new_movies)
    print('Hello')


    return total_budget , total_revneu , total_profit ,gross_vs_budget_line_fig, \
     movies_after_genre_filter_fig  , map_fig, genre_piechart_fig ,  from_span,to_span



if __name__ == "__main__":
    app.run_server()
