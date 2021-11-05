from numpy.core.fromnumeric import size
import pycountry_convert as pc
import plotly.express as px

# Add new Columns of Continent that Countries belongs
def add_continent(country):
    
    try:
        country_code = pc.country_name_to_country_alpha2(country, cn_name_format="default")
        continent_name = pc.country_alpha2_to_continent_code(country_code)   

    except:
        continent_name = '0' # To hande case of not found continent

    return continent_name

# create range of year as dictionary to spider
def create_slider_year_range(years):
    
    range_dict = {}

    for i in range(0, len(years), 5):
        range_dict[str(years[i])] = str(years[i])

    return range_dict


def filter_with_genre(dataset, top_num=6):
   
    genre_grouped= dataset.groupby(['genre', 'year'], as_index=False).sum()
    filterList = genre_grouped.groupby('genre').sum().sort_values(
        by='profit', ascending=False).iloc[0:top_num].index

    fillter_dataset = dataset[dataset['genre'].isin(filterList)]
    
    return fillter_dataset
    



import pycountry
import plotly.graph_objects as go

def get_map_fig(movie_df):
    countries = {}
    for country in pycountry.countries:
        countries[country.name] = country.alpha_3

    codes = [countries.get(country, 'Unknown code') for country in movie_df['country']]

    movie_df['code'] = codes

    map_df = movie_df.groupby(['code','country'], as_index=False).agg({"profit":"sum"})

    map_fig = go.Figure(data=go.Choropleth(
        locations = map_df['code'],
        z =  map_df['profit'],
        text = map_df['country'],
        colorscale = 'Blues',
        autocolorscale=False,
        reversescale=False,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_tickprefix = '$',
        colorbar_title = 'Profit in Billion $',
        
       
    ))
    map_fig.update_layout(
         title_text = "Total Profit over countries"
    )

    return map_fig


def create_genre_piechart(movies):

    fig = px.pie(movies.groupby('genre' , as_index=False).agg({"profit":"sum"}) , values='profit',
     names='genre', title="Kind OF Films Occurrence")
    fig.update_traces(textposition='inside', textinfo='percent+label')

    return fig


def create_genre_barplot(movies):


    movies= movies.groupby('genre' , as_index=False).agg({"released":"count"} )\
    .sort_values(by = 'released' , ascending = False)

    fig = px.bar( movies, width=500, x = 'genre', y = 'released' ,
        labels={
            "released": "Films Count"
        }, color = 'released',  color_continuous_scale=["#2e3948" , "#0077BB"],
     height=400 , template='plotly_white' , title="Movies Categories")

    fig.update_layout(
        xaxis = go.layout.XAxis(
            tickangle = 45)
            )

    return fig


def create_genre_score_barplot(movies):

    movies= movies.groupby('genre' , as_index=False).agg({"score":"sum"} )\
    .sort_values(by = 'score' , ascending = False)
   
    fig = px.bar( movies, width=500, x = 'genre', y = 'score' ,
            labels={
                "score": "Total Score"
            }, color = 'score',  color_continuous_scale=["#2e3948" , "#cb3701"],
        height=400 , template='plotly_white' , title="Total Score of Movies")

    fig.update_layout(
        xaxis = go.layout.XAxis(
            tickangle = 45)
            )

    return fig


def create_company_realesed_barplot(movies):

#create lineplot of 10 company with high profit in year

    fig= px.bar(movies.groupby('company', as_index=False).agg({"released":"count"}).sort_values(by='released',ascending = True)[-10:] , 
    x = 'released' , y = 'company' ,title="Top 10-Producer Compnaies in Movies Industry", width=500 , height=400,
     labels={
                "released": "Num Films",
                "company": "Company Name",

            },
    template='plotly_white'  , color="released" , color_continuous_scale=["#2e3948" , "#cb3701"])

    return fig


def create_country_realesed_barplot(movies):

#create lineplot of 10 company with high profit in year

    fig= px.bar(movies.groupby('country', as_index=False).agg({"released":"count"}).sort_values(by='released',ascending = True)[-10:] , 
    x = 'released' , y = 'country'  ,title="Top 10-Country in Movies Industry ", width=500 , height=400,
     labels={
                "released": "Num Films",
                "country": "Star Name",
            },
    template='plotly_white'  , color="released" , color_continuous_scale=["#2e3948" , "#0077BB"])

    return fig    