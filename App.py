# Dash app for food_prices data
# ZUNGU KWAZI

# Packages
from dash import Dash, html, dcc, Input, Output, callback, dash_table
import pandas as pd
import plotly.express as px

# Dataframes
df_prices = pd.read_csv("food_prices.csv")
df_minMax = pd.read_csv("MaxMinPrices_view.csv")
df_Qcount = pd.read_csv("QualityCount_view.csv")
df_units = pd.read_csv("UnitsUsed_view.csv")

# initialise app
stylesheet = ["styles.css"]
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
countries = ["South Africa", "Japan", "Sweden", "Canada", "Australia"]
prices_stats = ["Lowest Price", "Average Price", "Highest Price"]

# Layout
app.layout = html.Div([
    html.H1(className="row", id="mainTitle",
            children="Price Trends For Milk, Eggs, Bread & Potatoes In Five Selected Countries",
            style={'textAlign': 'center', 'color': 'blue', 'fontSize': 50, 'fontWeight': 700}),
    dcc.Dropdown(id="dropdown-country", options=countries, value="Australia"),
    dcc.Graph(id="trend-Graph"),
    html.Div(className="minMax", children=[html.Div(className="minMaxRadio", children=[dcc.RadioItems(id="radio-prices", options=prices_stats, value="Average Price")],
                                                    style={'padding-right': '20px'}),
                                           html.Div(className="minMaxGraph", children=[dcc.Graph(id="minMax")],
                                                    style={'width': '80%'})],
             style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
    html.Div(className="tables", children=[html.Div(className="units", children=[dash_table.DataTable(data=df_units.to_dict('records'),
                                                                                                      style_cell={
                                                                                                          'textAlign': 'center', 'background-color': 'grey', 'color': 'white'},
                                                                                                      style_header={'backgroundColor': 'black', 'fontWeight': '800'})],
                                                    style={'width': '40%'}),
                                           html.Div(className="qCount", children=[dash_table.DataTable(data=df_Qcount.to_dict('records'),
                                                                                                       style_header={
                                                                                                           'backgroundColor': 'black', 'fontWeight': '800', 'color': 'white'},
                                                                                                       style_cell={'textAlign': 'center', 'background-color': 'lightblue', 'border': 'solid 1px'})],
                                                    style={'width': '40%'})],
             style={'display': 'flex', 'align-items': 'center', 'justify-content': 'space-between'})
],
    style={'margin': '25px'}
)

# update trend-graph


@callback(
    Output("trend-Graph", "figure"),
    Input("dropdown-country", "value")
)
def update_graph1(selected):
    condition = df_prices["Country"] == selected
    filtered_df_prices = df_prices[condition]
    fig1 = px.line(filtered_df_prices, x="Date", y="PriceinUSD", color="FoodItem", color_discrete_sequence=px.colors.qualitative.Plotly,
                   title=f"<b>Prices trends in {selected}</b>")

    # custom layout
    fig1.update_layout(
        yaxis=dict(showgrid=False), xaxis=dict(showticklabels=False),
        yaxis_title="<b>Price in USD</b>",
        xaxis_title="",
        legend_title="<b>Item</b>",
        plot_bgcolor="RGB(232,236,236)",
        title_x=0.5
    )

    return fig1


# update for Min vs Max vs avg graph
@callback(
    Output("minMax", "figure"),
    Input("radio-prices", "value")
)
def update_graph2(selected):
    fig2 = px.bar(df_minMax, x="Country", y=selected,
                  color="FoodItem", barmode="group",
                  title=f"<b>{selected} For Each Item In Each Country</b>")

    # Customize labels for the y-axis and bar labels
    fig2.update_layout(yaxis_title='<b>Price</b>', xaxis_title="", legend_title='<b>Item</b>', title_x=0.5,
                       bargap=0.4, yaxis=dict(showgrid=False, showticklabels=False),
                       plot_bgcolor="rgb(128,128,128)")

    return fig2


# Run app
if __name__ == "__main__":
    app.run_server(debug=False)
