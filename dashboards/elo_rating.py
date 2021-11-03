from threading import main_thread
from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px

app = Dash(__name__)

matches = pd.read_pickle('../data/aflmatches_elo.pypickle')

fig = px.line(matches, x=matches.date, y="home_team_current_rating", color = "home_team", hover_data=['round'])
fig.update_layout(title = 'AFL Elo Ratings',
                  xaxis_title = 'Year',
                  yaxis_title = "ELO Rating",
                  legend = {"title": "Team"})

app.layout = html.Div(children=[
    html.H1(children='AFL Elo Ratings'),

    html.Div(children='''
        Select your favourite team or compare different teams by selecting them.
    '''),
    
    # Dropdown to select which teams are displayed in the plot
    dcc.Dropdown(
                id='home-team-select',
                options=[{'label': i, 'value': i} for i in matches.home_team.unique()],
                value='Essendon',
                multi=True
            ),

    dcc.Graph(
        id='afl-elo-rating'
    )
])

@app.callback(Output('afl-elo-rating', 'figure'), 
              Input('home-team-select', 'value'))
def update_graph(team_name):
    """Creates a line plot showing a teams change in Elo Rating over time

    Args:
        team_name (Input): The teams names chosen in the Dash dropdown

    Returns:
        Figure: A Plotly plot
    """
    # Check if more than one team is being compared
    if isinstance(team_name, str):
        matches_filtered = matches[matches.home_team == team_name]
        fig = px.line(matches_filtered, x=matches_filtered.date, y="home_team_current_rating", hover_data=['round'])        
        fig.update_layout(title = f'{team_name} Elo Rating',
                        xaxis_title = 'Year',
                        yaxis_title = "ELO Rating",
                        legend = {"title": "Team"})
        return fig
    else:
        matches_filtered = matches[matches.home_team.isin(team_name)]
        fig = px.line(matches_filtered, x=matches_filtered.date, y="home_team_current_rating", 
                      hover_data=['round'], color='home_team')        
        fig.update_layout(title = f'Elo Rating',
                        xaxis_title = 'Year',
                        yaxis_title = "ELO Rating",
                        legend = {"title": "Team"})
        return fig

if __name__ == '__main__':
    app.run_server(debug=True)