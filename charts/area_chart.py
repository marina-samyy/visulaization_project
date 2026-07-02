import plotly.graph_objects as go
import pandas as pd

def create_chart(df, chart_type):
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Month'] = df['Order Date'].dt.to_period('M').astype(str)
    data = df.groupby(['Month', 'Region'])['Sales'].sum().reset_index()

    colors = {
        'Central': 'rgba(46, 134, 193, 0.5)',
        'East':    'rgba(39, 174, 96, 0.5)',
        'South':   'rgba(231, 76, 60, 0.5)',
        'West':    'rgba(243, 156, 18, 0.5)'
    }

    fig = go.Figure()

    for region in data['Region'].unique():
        region_data = data[data['Region'] == region]
        fig.add_trace(go.Scatter(
            x=region_data['Month'],
            y=region_data['Sales'],
            name=region,
            mode='lines',
            fill='tozeroy',
            line=dict(width=2),
            fillcolor=colors.get(region, 'rgba(100,100,100,0.5)')
        ))

    fig.update_layout(
        title=dict(
            text="<b>Monthly Sales by Region</b>",
            x=0.5,
            font=dict(size=20, color='black', family='Arial')
        ),
        xaxis_title='<b>Month</b>',
        yaxis_title='<b>Sales (USD)</b>',
        plot_bgcolor='white',
        paper_bgcolor='white',

        showlegend=True,
        legend=dict(
            title=dict(text='<b>Region</b>'),
            bordercolor='black',
            borderwidth=1,
            yanchor='top', y=0.98,
            xanchor='right', x=0.98
        ),

        xaxis=dict(
            showline=True, linewidth=2,
            linecolor='black', mirror=True,
            showgrid=False,
            tickangle=45
        ),
        yaxis=dict(
            showline=True, linewidth=2,
            linecolor='black', mirror=True,
            rangemode='tozero',
            gridcolor='#D3D3D3', griddash='dot', showgrid=True,
            zeroline=True, zerolinecolor='black', zerolinewidth=1
        ),
        margin=dict(l=60, r=40, t=80, b=80)
    )

    return fig