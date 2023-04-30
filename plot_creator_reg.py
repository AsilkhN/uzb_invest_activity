import pandas as pd
# import plotly.express as px
import plotly.graph_objects as go

# Read in data from Excel file
df = pd.read_excel('invest_reg.xlsx', engine='openpyxl')

def gdp_graph(region):
    # create a trace for the line graph
    column_names = df['Регионы'].tolist()
    line_trace = go.Scatter(x=df['Годы'], y=df[column_names[int(region)]], mode='lines', name='line')

    # create a layout for the line graph
    layout = go.Layout(xaxis_title='Годы', yaxis_title='ВРП, млрд.сум.')

    # create a figure and add the trace and layout to it
    fig = go.Figure(data=[line_trace], layout=layout)

    # Convert plot to JSON format
    graphJSON_GDP = fig.to_json()

    return graphJSON_GDP

# Define the color for the bar you want to highlight
def population_bar(region):
    colors = ['#8c91c5'] * len(df)
    colors[int(region)] = '#709845'

    # Create the Plotly bar chart
    trace = go.Bar(
        x=df['Численность постоянного населения (тысяч чел)'],
        y=df['Регионы'],
        orientation='h',
        text=df['Численность постоянного населения (тысяч чел)'],
        textposition='auto',
        marker=dict(color=colors),
    )

    layout = go.Layout(
        title='Численность постоянного населения по регионам',
        xaxis=dict(title='Численность постоянного населения (тысяч чел)'),
        yaxis=dict(title='Регионы')
    )
    fig = go.Figure(data=[trace], layout=layout)

    # Convert plot to JSON format
    graphJSON = fig.to_json()

    return graphJSON

 # # Pass JSON to HTML template
# return render_template('plot.html', graphJSON=graphJSON)
