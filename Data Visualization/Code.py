import pandas as pd
from collections import Counter
import dash
import dash_core_components as dcc
import dash_html_components as html
import base64


from dash.dependencies import Input, Output
import numpy as np
import plotly.graph_objects as go




#-------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------ Get Data ---------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------#
print(" ")
df_athletes = pd.read_excel('data/athlete_events.xlsx', sheet_name='athlete_events')
print(" ")
df_participants = pd.read_excel('data/athlete_events.xlsx', sheet_name='participants')
print(" ")
df_countries= pd.read_excel('data/tops_countries.xlsx',sheet_name='Countries')

athletes_medals = pd.read_excel('data/tops_athletes.xlsx', sheet_name='Athletes Medals')
print(" ")

#Encode Image
encoded_image = base64.b64encode(open('images/Olympic-logo.png', 'rb').read())

#create years dict
years_select = {str(i): '{}'.format(str(i)) for i in df_participants.Year.unique()}
years_select[str(1892)] = "All"

#create sports dict
sports_select = [dict(label=sport.replace('_', ' '), value=sport) for sport in df_athletes.Sport.unique()]


#calculate numbers
nr_countries = df_athletes.Country.unique()
nr_countries = len(nr_countries)

nr_host_cities = df_participants.City.unique()
nr_host_cities = len(nr_host_cities)

nr_events = df_athletes.Event.unique()
nr_events = len(nr_events)

#--------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------------LAYOUT-----------------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------#

app = dash.Dash(__name__, assets_folder='style')

server = app.server

app.layout = html.Div([

    # Div 1. - Title, Top Winners, Top countries, Filter, Search
    html.Div([

        # Div 1.1. - Title
        html.Div([
            html.P('Olympic Games'),
            html.P('Summer', id='p2'),
            html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), id='logo')
            #html.Img(src=app.get_asset_url( '/images/Olympic-logo.png')),

        ], id='title', className='title leftboxes'
        ),  # end div 1.1.

        # end div 1.2.
        html.Div([
            html.P('Tokyo 2020 Olympic games are approaching fast and 120 years have passed since the first modern era '
                   'Olympic games. It is time to have a look at some games insights since the creation.'),
            html.Br()
        ], id='intro', className='leftboxes'
        ),

        # Div 1.3. - Top Winners
        html.Div([
            html.H2('Top Winners'),
            html.Div([dcc.Graph(id='table_top_a',config={'displayModeBar':False})], className='nice_choro')

            # dcc.Graph(
            #         id='top_contries_fig'
            # )
        ], id='top_winners', className='leftboxes'
        ),  # end div 1.3.

        # Div 1.3. - Top Countries
        html.Div([
            html.H2('Top Countries'),
            html.Div([dcc.Graph(id='table_top_c',config={'displayModeBar':False})], className='nice_choro')

        ], id='top_countries', className='leftboxes'
        ),  # end div 1.3.

        # Div 1.4. - Search, Filter
        html.Div([
            # Div 1.4.1. - Filter
            html.Div([
                html.P('What Type of Sports do you want to see?'),
                dcc.RadioItems(
                    id='sport_type',
                    options=[
                        {'label': 'Team', 'value': 'Team'},
                        {'label': 'Individual', 'value': 'Individual'},
                        {'label': 'Both', 'value': 'both'},

                    ],
                    value='both',
                    labelStyle={'display': 'inline-block', 'font-size': '15px'}
                )
            ], id='filter'
            ),  # end div 1.4.1

            # Div 1.4.2. - Search
            html.Div([
                html.P(),
                html.P("Do you want to select particular sports?"),
                dcc.Dropdown(
                    id='sport_select',
                    options=sports_select,
                    value=[],
                    multi=True,
                    style={'backgroundColor': 'rgb(218,218,218)', 'color': 'black', 'font-size': '13px'}
                )
            ], id='search'
            )  # end div 1.4.2.

        ], id='filters', className='leftboxes'
        ),  # end div 1.4.

        # Div 1.5.Text
        html.Div([
            html.H3('More About'),
            html.P('The first Olympic Games of the modern era opened in Athens in 1896, and the Olympic Movement has not stopped growing ever since. '),
            html.P('Although, the VI, XII and XIII editions of the Olympic Summer Games were cancelled due to the I and II World Wars.'),
            html.Br(), html.Br(), html.Br(), html.Br(), html.Br(), html.Br(),
            html.Br(), html.Br(), html.Br()
        ], id='text', className='leftboxes'
        ),

    ], id='div_1', className='column_1'
    ),  # end div 1.



    # Div 2. - Nr of Editions, HeatMap, Slider, Linecharts (Countries, Events, Athletes)
    html.Div([

        # Div 2.1. - Nr of Editions, Nr Countries, Nr Cities, Nr Events
        html.Div([
            # Div 2.1.1. - Nr of Editions
            html.Div([
                html.H3('Number of Editions'),
                html.P('XXXI')
            ], id='nr_editions', className='miniboxes'
            ),  # end div 2.1.1.

            # Div 2.1.2. - Nr Countries
            html.Div([
                html.H3('Number of Countries '),
                html.Div([str(nr_countries)], className='nr')
            ], id='nr_countries', className='miniboxes'
            ),  # end div 2.1.2.

            # Div 2.1.2. - Nr Cities
            html.Div([
                html.H3('Number of Host Cities '),
                html.Div([str(nr_host_cities)], className='nr'),
            ], id='nr_cities', className='miniboxes'
            ),  # end div 2.1.2.

            # Div 2.1.3. - Nr Events
            html.Div([
                html.H3('Number of Events '),
                html.Div([str(nr_events)], className='nr')
            ], id='nr_events', className='miniboxes'
            ),  # end div 2.1.3.

        ], id='counts', className='row_1'
        ),  # end div 2.1.


        # Div 2.2. - HeatMap
        html.Div([
            html.Div([dcc.Graph(id='map_choroplet',config={'displayModeBar':False})], className='nice_choro'),
            # dcc.Graph(id='heatmap', figure=map)
        ], id='heatmap', className='row_2'
        ),  # end div 2.2.

        # Div 2.3. - Slider
        html.Div([
            dcc.Slider(
                id='year_slider',
                min=1892,
                max=2016,
                step=4,
                #marks=datedict,
                marks=years_select, #.insert(0, 'All')
                #tooltip=str(value),
                value=1892,
                included=False,
                persistence_type='session',
            )
        ], id='slider', className='row_3'
        ),  # end div 2.3.

        # Div 2.4. - Linechart/Barchart/Areachart - Countries, Areachart Men & Women
        html.Div([
            # Div 2.4.1. - Linechart Countries
            html.Div([
                html.P('Olympics getting Popular'),
                html.Div([dcc.Graph(id='c_linechart')], className='nice_line'),
            ], id='countries_linechart', className='boxes'
            ),  # end div 2.4.1.

            # Div 2.4.2. - Areachart Men & Women
            html.Div([
                html.P('Athletes Men & Women'),
                html.Div([dcc.Graph(id='a_linechart')], className='nice_area'),
            ], id='athletes_linechart', className='boxes'
            ),  # end div 2.4.2.

        ], id='linecharts', className='row_4'
        ),  # end div 2.4.

        # Div 2.5. - Barchart
        html.Div([
            # Div 2.5.1. - Barchart Sports
            html.Div([
                html.P('Even Sports need to Qualify?'),
                html.Div([dcc.Graph(id='sports_linechart')], className='nice_bar'),
            ], id='sports_barchart', className='boxes'
            ),  # end div 2.5.1.
        ], id='bar_chart', className='row_5'
        ),  # end div 2.4.2.


    ], id='div_2', className='column_2'
    )  # end div 2.

], id='outer_div',
)


#----------------------------------------Callbacks---------------------------------------------------------------------#

@app.callback(

        [Output("map_choroplet", "figure"),
        Output(component_id='table_top_c', component_property='figure'),
        Output(component_id='table_top_a', component_property='figure'),
        Output(component_id='a_linechart', component_property='figure'),
        Output(component_id='sports_linechart', component_property='figure'),
        Output(component_id='c_linechart', component_property='figure')
        ],

        # Output("choropleth", "figure"),
        # Output("countries_linechart", "figure"),

    [
        Input("sport_type", "value"),
        Input("sport_select", "value"),
        Input("year_slider", "value"),

    ]
    )




#----------------------------------------Callbacks---------------------------------------------------------------------#
def update_graph(team, sport, year):

    # reduces the dataframe to be used to update the graphs, given the inputs
    if (year == 1892) & (len(sport) == 0) & (team == 'both'):
        df = df_countries.copy()
        athletes = athletes_medals
    elif (year != 1892) & (len(sport) == 0) & (team == 'both'):
        df = df_countries.loc[df_countries['Year'] == year, :].copy()
        athletes = athletes_medals.loc[athletes_medals['Year'] == year, :].copy()
    elif (year != 1892) & (len(sport) != 0) & (team == 'both'):
        df = df_countries.loc[(df_countries['Year'] == year) & (df_countries['Sport'].isin(sport)), :].copy()
        athletes = athletes_medals.loc[(athletes_medals['Year'] == year) & (athletes_medals['Sport'].isin(sport)),
                   :].copy()
    elif (year != 1892) & (len(sport) != 0) & (team != 'both'):
        df = df_countries.loc[(df_countries['Year'] == year) & (df_countries['Sport'].isin(sport)) & (
                df_countries['Team Sport'] == team), :].copy()
        athletes = athletes_medals.loc[(athletes_medals['Year'] == year) & (athletes_medals['Sport'].isin(sport)) & (
                athletes_medals['Team Sport'] == team), :].copy()
    elif (year == 1892) & (len(sport) != 0) & (team == 'both'):
        df = df_countries.loc[df_countries['Sport'].isin(sport), :].copy()
        athletes = athletes_medals.loc[athletes_medals['Sport'].isin(sport), :].copy()
    elif (year == 1892) & (len(sport) == 0) & (team != 'both'):
        df = df_countries.loc[df_countries['Team Sport'] == team, :].copy()
        athletes = athletes_medals.loc[athletes_medals['Team Sport'] == team, :].copy()
    elif (year == 1892) & (len(sport) != 0) & (team != 'both'):
        df = df_countries.loc[(df_countries['Sport'].isin(sport)) & (df_countries['Team Sport'] == team), :].copy()
        athletes = athletes_medals.loc[(athletes_medals['Sport'].isin(sport)) & (athletes_medals['Team Sport'] == team),
                   :].copy()
    elif (year != 1892) & (len(sport) == 0) & (team != 'both'):
        df = df_countries.loc[(df_countries['Year'] == year) & (df_countries['Team Sport'] == team), :].copy()
        athletes = athletes_medals.loc[(athletes_medals['Year'] == year) & (athletes_medals['Team Sport'] == team),
                   :].copy()

    df = df.groupby(by=['Country'])['Gold', 'Silver', 'Bronze'].sum()
    df['Country'] = df.index
    df.reset_index(drop=True, inplace=True)

    df = df.merge(df_athletes[['ISO3', 'Country']], on='Country', how='left')
    df.drop_duplicates(inplace=True)

    df = df.merge(df_participants[['City', 'Country', 'Edition']], how='outer', on='Country')
    df.loc[df['City'].isnull(), 'City'] = 'No host'
    df.loc[df['Edition'].isnull(), 'Edition'] = 'No host'
    df['Total'] = df['Gold'] + df['Silver'] + df['Bronze']
    df = df.groupby('Country').agg({'Gold': 'first', 'Silver': 'first', 'Bronze': 'first', 'Total': 'first',
                                    'ISO3': 'first', 'City': ', '.join, 'Edition': ', '.join}).reset_index()

#---------------------------------------------------Top 5 Athletes Filter----------------------------------------------#

    athletes = athletes.groupby(by=['Name'])['Gold', 'Silver', 'Bronze', 'Total'].sum()
    athletes['Name'] = athletes.index
    athletes.reset_index(drop=True, inplace=True)
    athletes.drop_duplicates(inplace=True)

    top5_athletes = athletes

    top5_athletes = top5_athletes.sort_values(by=['Total'], ascending=False)
    top5_athletes = top5_athletes.head()
    top5_athletes = top5_athletes.sort_values(by=['Total'], ascending=True)

    top5_athletes = top5_athletes.drop_duplicates()

    contador = Counter(top5_athletes.Name.tolist())
    repeted = []

    for key, value in contador.items():
        if value > 1:
            repeted.append(key)

    if len(repeted) != 0:
        repeted_frame = top5_athletes[top5_athletes.Name.isin(repeted)].copy()
        top5_athletes = top5_athletes[~top5_athletes.Name.isin(repeted)].copy()
        for i in repeted:
            soma = repeted_frame[repeted_frame.Name == i].sum(axis=0)
            top5_athletes = top5_athletes.append(
                {'Name': i, 'Gold': soma['Gold'], 'Silver': soma['Silver'], 'Bronze': soma['Bronze'],
                 'Total': soma['Total']}, ignore_index=True)

    top5_athletes.Name = [(i.split()[0] + ' ' + i.split()[-1] + "  ") for i in top5_athletes.Name]

    top5_athletes = top5_athletes.reset_index(drop=True)

    dfs = top5_athletes.copy()
    dfs.drop(dfs.index, inplace=True)
    dfs.drop(columns='Total', inplace=True)
    for index, row in top5_athletes.iterrows():
        if row.Bronze >= 1:
            v = 0
            while v < row.Bronze:
                dfs = dfs.append({'Name': row.Name, 'Gold': 0, 'Silver': 0, 'Bronze': row.Bronze - v},
                                 ignore_index=True)
                v += 1
        if row.Bronze == 0 and row.Silver > 0:
            v = 0
            while v < row.Silver:
                dfs = dfs.append({'Name': row.Name, 'Gold': 0, 'Silver': row.Silver - v, 'Bronze': 0},
                                 ignore_index=True)
                v += 1

        if row.Bronze > 0 and row.Silver > 0:
            v = row.Silver
            j = 0
            while v > 0:
                dfs = dfs.append({'Name': row.Name, 'Gold': 0, 'Silver': row.Bronze + row.Silver - j, 'Bronze': 0},
                                 ignore_index=True)
                v -= 1
                j += 1
        if (row.Bronze != 0 or row.Silver != 0) and row.Gold > 0:
            v = row.Gold
            j = 0
            while v > 0:
                dfs = dfs.append(
                    {'Name': row.Name, 'Gold': row.Bronze + row.Silver + row.Gold - j, 'Silver': 0, 'Bronze': 0},
                    ignore_index=True)
                v -= 1
                j += 1

        if row.Gold > 0 and row.Bronze == 0 and row.Silver == 0:
            v = 0
            while v < row.Gold:
                dfs = dfs.append({'Name': row.Name, 'Gold': row.Gold - v, 'Silver': 0, 'Bronze': 0}, ignore_index=True)
                v += 1

    dfs = dfs.replace(0, np.nan)

    #--------------------------------------------------------MAP  CREATION---------------------------------------------#

    trace1 = go.Choropleth(locations=df['ISO3'],
                           locationmode='ISO-3',
                           z=df['Total'],
                           text=np.array(df),
                           name='Total',
                           hovertemplate="<b>%{text[0]}</b><br>" +
                                         "Host City: %{text[6]}<br>" +
                                         "Edition: %{text[7]}<br>" +
                                         "Total Number of Medals: %{text[4]:.0f}<br>" +
                                         "     Gold:  %{text[1]:.0f}" +
                                         "     Silver:  %{text[2]:.0f}" +
                                         "     Bronze:  %{text[3]:.0f}",
                           hoverlabel=dict(bgcolor='rgb(242, 242, 242)',
                                           bordercolor='rgb(242, 242, 242)',
                                           font=dict(size=13,
                                                     color='rgb(0, 0, 0)',
                                                     ),
                                           namelength=0,
                                           ),
                           visible=True,
                           autocolorscale=False,
                           marker=dict(line=dict(width=0)),
                           colorscale='Aggrnyl',
                           colorbar=dict(title=dict(text='Total Number<br>of Medals \n',
                                                    font=dict(color='white', size=14)),
                                         tickfont=dict(color='white', size=13)))
    trace2 = go.Choropleth(locations=df['ISO3'],
                           locationmode='ISO-3',
                           z=df['Gold'],
                           text=np.array(df),
                           name='Gold',
                           hovertemplate="<b>%{text[0]}</b><br>" +
                                         "Host City: %{text[6]}<br>" +
                                         "Edition: %{text[7]}<br>" +
                                         "Total Number of Medals: %{text[4]:.0f}<br>" +
                                         "     Gold:  %{text[1]:.0f}",
                           hoverlabel=dict(bgcolor='rgb(242, 242, 242)',
                                           bordercolor='rgb(242, 242, 242)',
                                           font=dict(size=13,
                                                     color='rgb(0, 0, 0)',
                                                     ),
                                           namelength=0,
                                           ),
                           visible=False,
                           autocolorscale=False,
                           marker=dict(line=dict(width=0)),
                           colorscale='Aggrnyl',
                           colorbar=dict(title=dict(text='Total Number<br>of Golden Medals \n',
                                                    font=dict(color='white', size=14)),
                                         tickfont=dict(color='white', size=13)))
    trace3 = go.Choropleth(locations=df['ISO3'],
                           locationmode='ISO-3',
                           z=df['Silver'],
                           text=np.array(df),
                           name='Silver',
                           hovertemplate="<b>%{text[0]}</b><br>" +
                                         "Host City: %{text[6]}<br>" +
                                         "Edition: %{text[7]}<br>" +
                                         "Total Number of Medals: %{text[4]:.0f}<br>" +
                                         "     Silver:  %{text[2]:.0f}",
                           hoverlabel=dict(bgcolor='rgb(242, 242, 242)',
                                           bordercolor='rgb(242, 242, 242)',
                                           font=dict(size=13,
                                                     color='rgb(0, 0, 0)',
                                                     ),
                                           namelength=0,
                                           ),
                           visible=False,
                           autocolorscale=False,
                           marker=dict(line=dict(width=0)),
                           colorscale='Aggrnyl',
                           colorbar=dict(title=dict(text='Total Number<br>of Silver Medals \n',
                                                    font=dict(color='white', size=14)),
                                         tickfont=dict(color='white', size=13)))
    trace4 = go.Choropleth(locations=df['ISO3'],
                           locationmode='ISO-3',
                           z=df['Bronze'],
                           text=np.array(df),
                           name='Bronze',
                           hovertemplate="<b>%{text[0]}</b><br>" +
                                         "Host City: %{text[6]}<br>" +
                                         "Edition: %{text[7]}<br>" +
                                         "Total Number of Medals: %{text[4]:.0f}<br>" +
                                         "     Bronze:  %{text[3]:.0f}",
                           hoverlabel=dict(bgcolor='rgb(242, 242, 242)',
                                           bordercolor='rgb(242, 242, 242)',
                                           font=dict(size=13,
                                                     color='rgb(0, 0, 0)',
                                                     ),
                                           namelength=0,
                                           ),
                           visible=False,
                           autocolorscale=False,
                           marker=dict(line=dict(width=0)),
                           colorscale='Aggrnyl',
                           colorbar=dict(title=dict(text='Total Number<br>of Bronze Medals \n',
                                                    font=dict(color='white', size=14)),
                                         tickfont=dict(color='white', size=13)))
    layout = dict(geo=dict(landcolor='rgb(43, 43, 43)',
                           showcountries=False,
                           showframe=False,
                           #framewidth=0,
                           #framecolor='rgb(30, 30, 30)',
                           coastlinecolor='rgb(43, 43, 43)',
                           showcoastlines=True,
                           showland=True,
                           showocean=True,
                           oceancolor='rgb(30, 30, 30)',
                           showlakes=True,
                           lakecolor='rgb(30, 30, 30)',
                           projection={'type': 'equirectangular'}),
                  dragmode=False,
                  margin=dict(autoexpand=False,
                              l=10, r=150, t=10, b=40
                              ),
                  paper_bgcolor='rgb(30, 30, 30)',
                  plot_bgcolor='rgb(30, 30, 30)',
                  updatemenus=[
                      go.layout.Updatemenu(
                          visible=True,
                          type='buttons',
                          direction="right",
                          active=0,
                          buttons=list([
                              dict(args=[{"visible": [True, False, False, False]}],
                                   label="Total", method="update"),
                              dict(args=[{"visible": [False, True, False, False]}],
                                   label="Gold", method="update"),
                              dict(args=[{"visible": [False, False, True, False]}],
                                   label="Silver", method="update"),
                              dict(args=[{"visible": [False, False, False, True]}],
                                   label="Bronze", method="update"),
                          ]),
                          showactive=True,
                          x=0.90,
                          xanchor="right",
                          y=0.10,
                          yanchor="top",
                          bgcolor='rgb(30, 30, 30)',
                          font=dict(color='rgb(14, 135, 127)', size=14)
                      )
                  ]
                  )
    map = go.Figure(data=[trace1, trace2, trace3, trace4], layout=layout)

    # --------------------------------------------------- TOP COUNTRIES TABLE------------------------------------------#

    top_5_countries = df.copy()
    top_5_countries = top_5_countries.sort_values(by='Total', ascending=False)
    top_5_countries = top_5_countries.head()

    table_countries = go.Table(
        header=dict(
            values=["Country", "Gold", "Silver", "Bronze"],
            line_color=['rgb(128,128,128)', 'rgb(255, 206, 51)', 'rgb(192,192,192)', 'rgb(205, 127, 50)'],
            fill_color=['rgb(128,128,128)', 'rgb(255, 206, 51)', 'rgb(192,192,192)', 'rgb(205, 127, 50)'],
            align='center',
            font=dict(color=['black'], size=15),
        ),
        cells=dict(
            values=[top_5_countries.Country, top_5_countries.Gold, top_5_countries.Silver, top_5_countries.Bronze],
            line_color='black', fill_color='rgb(43, 43, 43)',
            align=['center','center'], font=dict(color='white', size=14),
            height=30
        )
    )
    layout_table = dict(
        showlegend=False,
        plot_bgcolor='black',
        paper_bgcolor='black',
        autosize=False,
        width=400,
        height=340,
        margin=dict(autoexpand=False, l=10, r=10, t=10, b=5),
    )

    table = go.Figure(data=table_countries, layout=layout_table)

    table.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })

    # ---------------------------------------------------  Top 5 Athlethes Pictogram-----------------------------------#

    fig_tp5a = go.Figure()

    fig_tp5a.add_trace(go.Scatter(x=dfs.Bronze.tolist(), y=dfs.Name.tolist(), mode='markers',
                             hoverinfo='skip',
                             marker={'symbol': 'circle', 'size': 7, 'color': 'rgb(205, 127, 50)'}, name='Bronze'))

    fig_tp5a.add_trace(go.Scatter(x=dfs.Silver.tolist(), y=dfs.Name.tolist(), mode='markers',
                             hoverinfo='skip',
                             marker={'symbol': 'circle', 'size': 7, 'color': 'rgb(192,192,192)'}, name='Silver'))

    fig_tp5a.add_trace(go.Scatter(x=dfs.Gold.tolist(), y=dfs.Name.tolist(), mode='markers',
                             hoverinfo='skip',
                             marker={'symbol': 'circle', 'size': 7, 'color': 'rgb(255, 206, 51)'}, name='Gold'))

    fig_tp5a.update_layout(dragmode=False,
                              xaxis=dict(title=dict(text="Medals Won",
                                                    font=dict(family='Arial',
                                                              size=14,
                                                              color='white',
                                                              ),
                                                    ),
                                         range=[0, (top5_athletes.Total.max() + 1)],
                                         showgrid=False,
                                         tick0=0,
                                         tickfont=dict(family='Arial',
                                                       size=13,
                                                       color='white',
                                                       ),
                                         showline=False,
                                         showticklabels=True,
                                         dtick=5),  # which ticks to show - one by one
                              yaxis=dict(showgrid=False,
                                         showline=False,
                                         tickfont=dict(family='Arial',
                                                       size=13,
                                                       color='white',
                                                        ),
                                         #standoff=2,
                                         ),
                              showlegend=False,
                              plot_bgcolor='black',
                              paper_bgcolor='black',
                              autosize=False,
                              width=400,
                              height=220,
                              margin=dict(autoexpand=False, l=140, r=10, t=10, b=30),
                            )

    fig_tp5a.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })

    # -------------------------------------------------------------------------------------------------------------------
    # AREA CHART
    # -----------------------------------------------------------------------------------------------------------------

    trace1 = go.Scatter(x=df_participants['Year'],
                        y=df_participants['Men'],
                        name='Men',
                        mode="lines+markers",
                        fill="tonexty",  # "none" | "tozeroy" | "tozerox" | "tonexty" | "tonextx" | "toself" | "tonext"
                        fillcolor='rgb(188, 246, 237)',
                        stackgroup='one',
                        text=df_participants['Participants'],
                        hovertemplate="<b>%{x}</b><br>Total: %{text:.0f}<br>Men: %{y:.0f}",
                        hoverlabel=dict(bgcolor='rgb(242, 242, 242)',
                                        bordercolor='rgb(242, 242, 242)',
                                        font=dict(size=12,
                                                  color='rgb(0, 0, 0)',
                                                  ),
                                        namelength=0,
                                        ),
                        line=dict(color='rgb(21, 148, 128)',
                                  width=3,
                                  dash='solid',
                                  shape="linear"),  # "linear" | "spline"
                        marker=dict(symbol='x-dot',
                                    size=5, color='rgb(31, 46, 46)'),
                        showlegend=True,
                        )

    trace2 = go.Scatter(x=df_participants['Year'],
                        y=df_participants['Women'],
                        name='Women',
                        mode="lines+markers",
                        fill="tonexty",  # "tozeroy" |"tonexty" | "tonextx" | "toself" | "tonext"
                        fillcolor='rgb(247, 248, 185)',
                        stackgroup='one',
                        text=df_participants['Participants'],
                        hovertemplate="<b>%{x}</b><br>Total: %{text:.0f}<br>Women: %{y:.0f}",
                        hoverlabel=dict(bgcolor='rgb(242, 242, 242)',
                                        bordercolor='rgb(242, 242, 242)',
                                        font=dict(size=12,
                                                  color='rgb(0, 0, 0)',
                                                  ),
                                        namelength=0,
                                        ),
                        line=dict(color='rgb(237, 239, 93)',
                                  width=3,
                                  dash='solid',
                                  shape="linear"),  # "linear" | "spline"
                        marker=dict(symbol='x-dot',
                                    size=5, color='rgb(31, 46, 46)'),
                        showlegend=True,
                        )

    layout_area = dict(xaxis=dict(title=dict(text="Year",
                                             font=dict(family='Arial',
                                                       size=14,
                                                       color='white',
                                                       ),
                                             ),
                                  showline=True,
                                  showgrid=False,
                                  showticklabels=True,
                                  linecolor='rgb(0, 0, 0)',
                                  linewidth=2,
                                  ticks='outside',
                                  tickcolor='white',
                                  tickfont=dict(
                                      family='Arial',
                                      size=13,
                                      color='white',
                                  ),
                                  tickvals=[1896, 1904, 1912, 1920, 1928, 1936, 1948, 1956, 1964,
                                            1972, 1980, 1988, 1996, 2004, 2012],
                                  dtick=4,
                                  tickangle=45,
                                  showspikes=True,
                                  spikecolor='rgb(0, 0, 0)',
                                  spikethickness=2,
                                  ),
                       yaxis=dict(title=dict(text="Number of Athletes",
                                             font=dict(family='Arial',
                                                       size=14,
                                                       color='white',
                                                       ),
                                             ),
                                  showgrid=False,
                                  showline=False,
                                  showticklabels=True,
                                  linecolor='white',
                                  linewidth=2,
                                  ticks='outside',
                                  tickcolor='white',
                                  tickfont=dict(family='Arial',
                                                size=13,
                                                color='white',
                                                ),
                                  tick0=0,
                                  range=[0, 12000],
                                  side='right',
                                  ),
                       autosize=False,
                       width=510,
                       height=400,
                       margin=dict(autoexpand=False,
                                   l=10, r=50, t=10, b=70
                                   ),
                       showlegend=True,
                       legend=dict(x=0, y=1, font=dict(color='white')),
                       paper_bgcolor='rgba(0, 0, 0)',
                       plot_bgcolor='rgba(0, 0, 0)'
                       )

    area = go.Figure(data=[trace1, trace2], layout=layout_area)

    area.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })

    area.add_annotation(
        go.layout.Annotation(
            x=1932,
            y=1332,
            xref="x",
            yref="y",
            text="Worldwide Great<br>Depression",
            showarrow=True,
            font=dict(
                family="Arial",
                size=13,
                color="#ffffff"
            ),
            align="left",
            arrowhead=1,
            arrowsize=1,
            arrowwidth=1,
            arrowcolor="#636363",
            ax=-50,
            ay=-130,
            bordercolor="#619292",
            borderwidth=1,
            borderpad=4,
            bgcolor="#619292",
            opacity=0.8
        )
    )

    area.add_annotation(
        go.layout.Annotation(
            x=1956,
            y=3314,
            xref="x",
            yref="y",
            text="Protest due to the IOC's<br>rejection to suspend the USSR<br>after their invasion of Hungary.",
            showarrow=True,
            font=dict(
                family="Arial",
                size=13,
                color="#ffffff"
            ),
            align="left",
            arrowhead=1,
            arrowsize=1,
            arrowwidth=1,
            arrowcolor="#636363",
            ax=-75,
            ay=-150,
            bordercolor="#619292",
            borderwidth=1,
            borderpad=4,
            bgcolor="#619292",
            opacity=0.8
        )
    )

    if year != 1892:
        area.update_layout(
            shapes=[
                go.layout.Shape(
                    type="rect",
                    # x-reference is assigned to the x-values
                    xref="x",
                    # y-reference is assigned to the y-values
                    yref="y",
                    x0=year - 1.7,
                    y0=0,
                    x1=year + 1.7,
                    y1=int(df_participants[df_participants.Year == year]['Participants']),
                    fillcolor="#FF8C00",#ff9966
                    opacity=0.6,
                    line_width=0,
                )])

    # ------------------------------------------------------------------------------------------------------------------
    #  STACKED BAR FOR SPORTS
    # ------------------------------------------------------------------------------------------------------------------
    years = df_participants['Year']

    df_participants['New Sports'] = ""
    df_participants['Returning Sports'] = ""
    df_participants['Maintained Sports'] = ""
    df_participants['Lost Sports'] = ""

    all_sports = []
    previous_list = []
    for idx, x in enumerate(years):
        if (idx != 0):
            previous_list.extend(df_participants.at[idx - 1, 'New Sports'])
            previous_list.extend(df_participants.at[idx - 1, 'Returning Sports'])
            previous_list.extend(df_participants.at[idx - 1, 'Maintained Sports'])

        if (idx == 0):
            df_participants.at[idx, 'New Sports'] = df_athletes[df_athletes['Year'] == years[0]].Sport.unique().tolist()
            df_participants.at[idx, 'Returning Sports'] = []
            df_participants.at[idx, 'Maintained Sports'] = []
        elif (idx == 1):
            df_participants.at[idx, 'New Sports'] = [a for a in
                                                     df_athletes[df_athletes['Year'] == x].Sport.unique().tolist() if
                                                     a not in df_participants['New Sports'][idx - 1]]
            df_participants.at[idx, 'Returning Sports'] = []
            df_participants.at[idx, 'Lost Sports'] = [a for a in previous_list if a not in df_athletes[
                df_athletes['Year'] == x].Sport.unique().tolist()]
            df_participants.at[idx, 'Maintained Sports'] = [a for a in df_athletes[
                df_athletes['Year'] == x].Sport.unique().tolist() if a in df_participants['New Sports'][idx - 1]]
        else:
            df_participants.at[idx, 'New Sports'] = [a for a in
                                                     df_athletes[df_athletes['Year'] == x].Sport.unique().tolist() if
                                                     a not in all_sports]
            df_participants.at[idx, 'Returning Sports'] = [a for a in
                                                           df_athletes[df_athletes['Year'] == x].Sport.unique().tolist()
                                                           if a not in df_participants['New Sports'][
                                                               idx - 1] and a in all_sports and
                                                           a not in df_participants['Maintained Sports'][
                                                               idx - 1] and a not in
                                                           df_participants['Returning Sports'][idx - 1]]
            df_participants.at[idx, 'Maintained Sports'] = [a for a in df_athletes[
                df_athletes['Year'] == x].Sport.unique().tolist()
                                                            if a in df_participants['New Sports'][idx - 1]
                                                            or a in df_participants['Returning Sports'][idx - 1]
                                                            or a in df_participants['Maintained Sports'][idx - 1]]
            df_participants.at[idx, 'Lost Sports'] = [a for a in previous_list if a not in df_athletes[
                df_athletes['Year'] == x].Sport.unique().tolist()]

        previous_list = []
        all_sports.extend(df_participants.at[idx, 'New Sports'])

    df_participants['New Sports_Count'] = ""
    df_participants['Returning Sports_Count'] = ""
    df_participants['Maintained Sports_Count'] = ""

    for idx, x in enumerate(years):
        df_participants.at[idx, 'New Sports_Count'] = len(df_participants.at[idx, 'New Sports'])
        df_participants.at[idx, 'Returning Sports_Count'] = len(df_participants.at[idx, 'Returning Sports'])
        df_participants.at[idx, 'Maintained Sports_Count'] = len(df_participants.at[idx, 'Maintained Sports'])

    for idx, x in enumerate(years):
        df_participants.at[idx, 'New Sports'] = [' {0}'.format(elem) if index != 0 else '{0}'.format(elem) for
                                                 index, elem in enumerate(df_participants.at[idx, 'New Sports'])]
        df_participants.at[idx, 'Returning Sports'] = [' {0}'.format(elem) if index != 0 else '{0}'.format(elem) for
                                                       index, elem in
                                                       enumerate(df_participants.at[idx, 'Returning Sports'])]
        df_participants.at[idx, 'Maintained Sports'] = [' {0}'.format(elem) if index != 0 else '{0}'.format(elem) for
                                                        index, elem in
                                                        enumerate(df_participants.at[idx, 'Maintained Sports'])]
        # df_participants.at[idx, 'Lost Sports'] = [' {0}'.format(elem) if index != 0 else '{0}'.format(elem) for
        #                                           index, elem in enumerate(df_participants.at[idx, 'Lost Sports'])]

    for idx, x in enumerate(years):
        if df_participants.at[idx, 'Lost Sports'] == []:
            df_participants.at[idx, 'Lost Sports'] = 0

    layout = dict(xaxis=dict(title=dict(text="Year",
                                        font=dict(family='Arial',
                                                  size=14,
                                                  color='white',
                                                  ),
                                        ),
                             showline=True,
                             showgrid=False,
                             showticklabels=True,
                             linecolor='white',
                             linewidth=2,
                             ticks='outside',
                             tickcolor='white',
                             range=[1894, 2018],
                             tickfont=dict(
                                 family='Arial',
                                 size=13,
                                 color='white',
                             ),
                             # tickvals=[1896, 1904, 1912, 1920, 1928, 1936, 1948, 1956, 1964,
                             #           1972, 1980, 1988, 1996, 2004, 2012],
                             dtick=4,
                             tickangle=45
                             ),
                  yaxis=dict(title=dict(text="Number of Sports",
                                        font=dict(family='Arial',
                                                  size=14,
                                                  color='white',
                                                  ),
                                        ),
                             showgrid=False,
                             showline=True,
                             showticklabels=True,
                             linecolor='white',
                             linewidth=2,
                             ticks='outside',
                             tickcolor='white',
                             tickfont=dict(family='Arial',
                                           size=13,
                                           color='white',
                                           ),
                             tick0=0
                             ),
                  showlegend=True,
                  margin=dict(autoexpand=False, l=50, r=170, t=10, b=70),
                  legend=dict(font=dict(color='white'), uirevision=False),
                  paper_bgcolor='rgba(0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0)'
                  )

    bar = go.Figure(data=[
                go.Bar(name='Maintained Sports', x=df_participants['Year'], y=df_participants['Maintained Sports_Count'],
                       text=df_participants['Lost Sports'], marker=dict(color='rgb(237, 239, 93)'),
                       hovertemplate="<b>Maintained Sports:</b> %{y:.0f}<br><b>Lost Sports:</b> %{text}",
                       hoverlabel=dict(bgcolor='rgb(242, 242, 242)',
                                       bordercolor='rgb(242, 242, 242)',
                                       font=dict(size=13,
                                                 color='rgb(0, 0, 0)',
                                                 ),
                                       namelength=0,
                                       )),

                go.Bar(x=df_participants['Year'], y=df_participants['Returning Sports_Count'], name='Returning Sports',
                       text=df_participants['Returning Sports'], marker=dict(color='rgb(35, 87, 105)'),
                       hovertemplate="<b>Returning Sports:</b> %{y:.0f}<br>%{text}",  # Total Sports: %{text}<br>
                       hoverlabel=dict(bgcolor='rgb(242, 242, 242)',
                                       bordercolor='rgb(242, 242, 242)',
                                       font=dict(size=13,
                                                 color='rgb(0, 0, 0)',
                                                 ),
                                       namelength=0,
                                       )),
                go.Bar(name='New Sports', x=df_participants['Year'], y=df_participants['New Sports_Count'],
                       text=df_participants['New Sports'], marker=dict(color='rgb(230, 230, 230)'),
                       hovertemplate="<b>New Sports:</b> %{y:.0f}<br>%{text}",  # Total Sports: %{text}<br>
                       hoverlabel=dict(bgcolor='rgb(242, 242, 242)',
                                       bordercolor='rgb(242, 242, 242)',
                                       font=dict(size=13,
                                                 color='rgb(0, 0, 0)',
                                                 ),
                                       namelength=0,
                                       ))],
                layout=layout)

    # Change the bar mode
    bar.update_layout(barmode='stack')

    # Add totals at the top of the bars
    bar.add_trace(go.Scatter(
        x=df_participants['Year'],
        y=df_participants['Sports'],
        mode="text",
        # name="Lines, Markers and Text",
        text=df_participants['Sports'],
        textfont=dict(color="white", size=11),
        textposition="top center",
        showlegend=False,
        hoverinfo='skip',

    ))

    bar.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })

    if year != 1892:
        bar.update_layout(
            shapes=[
                go.layout.Shape(
                    type="rect",
                    # x-reference is assigned to the x-values
                    xref="x",
                    # y-reference is assigned to the y-values
                    yref="y",
                    x0=year - 2,
                    y0=0,
                    x1=year + 2,
                    y1=df_participants[df_participants.Year == year][
                        ['Returning Sports_Count','Maintained Sports_Count', 'New Sports_Count']].sum().sum(),
                    fillcolor="#FF8C00",
                    opacity=0.7,
                    line_width=0
                )])

    # --------------------------------------------------- Line Chart ----------------------------------------------------#
    line = go.Figure(data=go.Scatter(x=df_participants['Year'],
                                     y=df_participants['Countries'],
                                     mode="lines+markers",
                                     text=df_participants['Edition'],
                                     hovertemplate="<b>%{y:,.0f}</b> countries participated<br>in the %{text} Summer Olympics <b>(%{x})",
                                     hoverlabel=dict(bgcolor='rgb(242, 242, 242)',
                                                     bordercolor='rgb(242, 242, 242)',
                                                     font=dict(size=12,
                                                               color='black',
                                                               ),
                                                     namelength=0,
                                                     ),
                                     line=dict(color='rgb(237, 237, 93)',
                                               width=3,
                                               dash='solid'),
                                     marker=dict(symbol="circle-dot",
                                                 size=8, color='rgb(35, 88, 105)'),
                                     showlegend=False
                                     ),
                     layout=dict(xaxis=dict(title=dict(text="Year",
                                                       font=dict(family='Arial',
                                                                 size=14,
                                                                 color='white',
                                                                 ),
                                                       ),
                                            showline=True,
                                            showgrid=False,
                                            showticklabels=True,
                                            linecolor='white',
                                            linewidth=1.5,
                                            ticks='outside',
                                            tickcolor='white',
                                            tickfont=dict(
                                                family='Arial',
                                                size=13,
                                                color='white',
                                            ),

                                            tickvals=[1896, 1904, 1912, 1920, 1928, 1936, 1948, 1956, 1964,
                                                      1972, 1980, 1988, 1996, 2004, 2012],
                                            dtick=4,
                                            tickangle=45,
                                            showspikes=True,
                                            spikecolor='rgb(179, 203, 203)'
                                            ),
                                 yaxis=dict(title=dict(text="Number of Countries",
                                                       font=dict(family='Arial',
                                                                 size=14,
                                                                 color='white',
                                                                 ),
                                                       ),
                                            showgrid=False,
                                            showline=True,
                                            showticklabels=True,
                                            linecolor='white',
                                            linewidth=1.5,
                                            ticks='outside',
                                            tickcolor='white',
                                            tickfont=dict(family='Arial',
                                                          size=13,
                                                          color='white',
                                                          ),
                                            # tick0 = 0,
                                            dtick=50,
                                            range=[0, 250],
                                            ),
                                 autosize=False,
                                 width=512,
                                 height=400,
                                 margin=dict(autoexpand=False, l=50, r=5, t=10, b=70),
                                 showlegend=False,
                                 paper_bgcolor='rgba(0,0,0,0)',
                                 plot_bgcolor='rgba(0,0,0,0)'
                                 )
                     )

    line.add_annotation(
        go.layout.Annotation(
            x=1976,
            y=92,
            xref="x",
            yref="y",
            text="After New Zealand's rugby team broke the<br>international sports embargo on Apartheid<br>in South Afr"
                 "ica, 28 African countries boycotted<br>the summer games in Montreal.",
            showarrow=True,
            font=dict(
                family="Arial",
                size=13,
                color="#ffffff"
            ),
            align="left",
            arrowhead=1,
            arrowsize=1,
            arrowwidth=1,
            arrowcolor="#636363",
            ax=-100,
            ay=-120,
            bordercolor="#619292",
            borderwidth=1,
            borderpad=4,
            bgcolor="#619292",
            opacity=0.8
        )
    )

    line.add_annotation(
        go.layout.Annotation(
            x=1980,
            y=80,
            xref="x",
            yref="y",
            text="Led by the United States, 66 countries<br>boycotted the games because<br>of the Soviet–Afghan War.",
            showarrow=True,
            font=dict(
                family="Arial",
                size=13,
                color="#ffffff"
            ),
            align="left",
            arrowhead=1,
            arrowsize=1,
            arrowwidth=1,
            arrowcolor="#636363",
            ax=50,
            ay=40,
            bordercolor="#619292",
            borderwidth=1,
            borderpad=4,
            bgcolor="#619292",
            opacity=0.8
        )
    )

    if year != 1892:
        line.update_layout(
            shapes=[
                go.layout.Shape(
                    type="rect",
                    # x-reference is assigned to the x-values
                    xref="x",
                    # y-reference is assigned to the y-values
                    yref="y",
                    x0=year - 0.15,
                    x1=year + 0.15,
                    y0=0,
                    y1=int(df_participants[df_participants.Year == year]['Countries']),
                    fillcolor="#FF8C00",
                    line=dict(
                        color="#FF8C00"),
                    line_width=2,
                    opacity=0.7
                )])

    return map, table, fig_tp5a, area, bar, line









# Run application
if __name__ == '__main__':
    app.run_server(debug=True)