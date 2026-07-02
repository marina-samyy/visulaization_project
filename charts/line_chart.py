import plotly.graph_objects as go
import pandas as pd

def create_chart(df, chart_type):
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Month'] = df['Order Date'].dt.to_period('M').astype(str)
    data = df.groupby('Month')['Sales'].sum().reset_index()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=data['Month'],
        y=data['Sales'],
        mode='lines+markers',
        name='Monthly Sales',
        line=dict(color='#2E86C1', width=3),
        marker=dict(size=6, color='#2E86C1'),
    ))

    fig.update_layout(
        title=dict(
            text="<b>Monthly Sales Trend</b>",
            x=0.5,
            font=dict(size=20, color='black', family='Arial')
        ),
        xaxis_title='<b>Month</b>',
        yaxis_title='<b>Sales (USD)</b>',
        plot_bgcolor='white',
        paper_bgcolor='white',


        showlegend=True,
        legend=dict(
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