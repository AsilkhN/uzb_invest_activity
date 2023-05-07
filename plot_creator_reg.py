import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Read in data from Excel file
df = pd.read_excel('invest_reg.xlsx', engine='openpyxl')
df_ia = pd.read_excel('invest_reg.xlsx', sheet_name = 'Показатели', engine='openpyxl')

def gdp_graph(region):
    # create a trace for the line graph
    column_names = df['Регионы'].tolist()
    line_trace = go.Scatter(x=df['Годы'], y=df[column_names[int(region)]],
                            mode='lines', name='line')

    # create a layout for the line graph
    layout = go.Layout(xaxis_title='Годы', yaxis_title='ВРП, млрд.сум.')

    # create a figure and add the trace and layout to it
    fig = go.Figure(data=[line_trace], layout=layout)

    # Convert plot to JSON format
    graphJSON_GDP = fig.to_json()

    return graphJSON_GDP



def population_bar(region):
    # Define the color for the bar you want to highlight
    colors = ['#8c91c5'] * len(df)
    colors[int(region)] = '#709845'

    # Create the Plotly bar chart
    trace = go.Bar(x=df['Численность постоянного населения (тысяч чел)'],
                   y=df['Регионы'], orientation='h',
                   text=df['Численность постоянного населения (тысяч чел)'],
                   textposition='auto', marker=dict(color=colors))

    layout = go.Layout(
                       xaxis=dict(title='Численность постоянного населения (тысяч чел)'),
                       yaxis=dict(title='Регионы'))
    fig = go.Figure(data=[trace], layout=layout)

    # Convert plot to JSON format
    graphJSON = fig.to_json()

    return graphJSON



def growth_temp(region):
    colors = ['#8c91c5'] * len(df_ia)
    colors[int(region)] = '#709845'

    rounded = [round(num, 2) for num in df_ia['Темпы роста инвестиций в основной капитал']]

    # Create the Plotly bar chart
    trace = go.Bar(x=df_ia['Регионы'],
                   y=rounded, orientation='v',
                   text=df_ia['Темпы роста инвестиций в основной капитал'].round(4),
                   textposition='auto', marker=dict(color=colors))

    layout = go.Layout(
                       xaxis=dict(title='Регионы'),
                       yaxis=dict(title='Темпы роста инвестиций в основной капитал', tickformat='.1f'))
    fig = go.Figure(data=[trace], layout=layout)

    # Convert plot to JSON format
    graphJSON = fig.to_json()

    return graphJSON

def inv_share():
    regions = df_ia['Регионы']

    invest_share = df_ia['Доля инвестиций в ВРП']

    foreign_share = df_ia['Доля иностранных инвестиций в ВРП']

    size = [i+j for i,j in zip(invest_share, foreign_share)]

    fig = go.Figure(data=go.Scatter(
        x=foreign_share,
        y=invest_share,
        mode='markers',
        marker=dict(
            size=size,
            sizemode='diameter',
            sizeref=0.7,
            color=invest_share,
            colorscale='viridis',
            showscale=True
        ),
        text=regions
    ))

    fig.update_layout(
        xaxis_title='Доля иностранных инвестиций в ВРП',
        yaxis_title='Доля инвестиций в ВРП',
        yaxis=dict(range=[min(invest_share)-0.05, max(invest_share)+0.05]),
    )

    graphJSON = fig.to_json()
    return graphJSON


def inv_dev(region):
    values = df_ia['Доля региона по освоеннию инвестиций в республике']
    labels = df_ia['Регионы']
    pull = [0.3 if i == int(region) else 0 for i in range(14)] # Make the selected region's slice protrude
    print(pull)
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, pull=pull)])
    fig.update_layout(title=f"Доля региона {labels[int(region)]} по освоеннию инвестиций в республике",
                      margin=dict(t=50, l=0, r=0, b=0))

    graphJSON = fig.to_json()
    return graphJSON

def inv_per_capita(region):
    values = df_ia['Инвестиции на душу населения (млн.сум)']
    labels = df_ia['Регионы']
    colors = ['rgb(173, 255, 47)', 'rgb(154, 205, 50)', 'rgb(50, 205, 50)', 'rgb(32, 178, 170)', 'rgb(0, 191, 255)', 'rgb(30, 144, 255)', 'rgb(0, 0, 205)', 'rgb(0, 0, 139)', 'rgb(0, 0, 128)', 'rgb(25, 25, 112)', 'rgb(0, 0, 128)', 'rgb(0, 0, 139)', 'rgb(0, 0, 205)', 'rgb(30, 144, 255)']


    fig = go.Figure()

    for i in range(len(values)):
        opacity = 0.3
        if i == int(region):
            opacity = 1.0
        fig.add_trace(go.Bar( 
            x=[labels[i]],
            y=[values[i]],
            marker=dict(
                color=colors[i],
                opacity=opacity
            ),
            name=labels[i]
        ))

    fig.update_layout(
        xaxis_title="Регионы",
        yaxis_title="Инвестиции на душу населения (млн.сум)",
        showlegend=False
    )

    graphJSON = fig.to_json()
    return graphJSON

