import pandas as pd
# import plotly.express as px
import plotly.graph_objects as go

# Read in data from Excel file
df = pd.read_excel('invest_reg.xlsx', sheet_name='ВВП_страны', engine='openpyxl')

def gdp_graph():
    # create a trace for the line graph
    line_trace = go.Scatter(x=df['Годы'], y=df['ВВП, млрд.сум.'], mode='lines', name='line')

    # create a layout for the line graph
    layout = go.Layout(xaxis_title='Годы', yaxis_title='ВВП, млрд.сум.')

    # create a figure and add the trace and layout to it
    fig = go.Figure(data=[line_trace], layout=layout)

    # Convert plot to JSON format
    graphJSON = fig.to_json()

    return graphJSON

