import plotly.graph_objects as go
import plotly.express as px
import numpy as np
 
def create_chart(df, chart_id):
 
    if chart_id == 'histogram':
        
 
        
        
        p99 = df['Sales'].quantile(0.99)
        data = df[df['Sales'] <= p99]['Sales']
 
        
        mean_val  = data.mean()
        median_val = data.median()
        std_val   = data.std()
 
        fig = go.Figure()
 
        fig.add_trace(go.Histogram(
            x=data,
            nbinsx=40,
            name='Sales Frequency',
            marker=dict(
                color='#AED6F1',          # Light blue fill
                line=dict(color='black', width=1)   # Black border per guidelines
            ),
            opacity=0.85
        ))
 
        
        y_max = 1800 
 
        
        fig.add_shape(type='line',
            x0=mean_val, x1=mean_val, y0=0, y1=y_max,
            line=dict(color='#1A5276', width=2, dash='dash'))
 
        fig.add_annotation(
            x=mean_val, y=y_max,
            text=f"<b>Mean<br>${mean_val:,.0f}</b>",
            showarrow=False,
            yshift=10,
            font=dict(color='#1A5276', size=11),
            xanchor='left'
        )
 
        
        fig.add_shape(type='line',
            x0=median_val, x1=median_val, y0=0, y1=y_max,
            line=dict(color='#1E8449', width=2, dash='dot'))
 
        fig.add_annotation(
            x=median_val, y=y_max * 0.85,
            text=f"<b>Median<br>${median_val:,.0f}</b>",
            showarrow=False,
            yshift=10,
            font=dict(color='#1E8449', size=11),
            xanchor='right'
        )
 
        
        fig.add_shape(type='rect',
            x0=mean_val - std_val, x1=mean_val + std_val,
            y0=0, y1=y_max,
            fillcolor='rgba(174, 214, 241, 0.2)',
            line=dict(color='#5DADE2', width=1, dash='dot'))
 
        fig.add_annotation(
            x=mean_val + std_val, y=y_max * 0.5,
            text=f"<b>+1 Std</b>",
            showarrow=False,
            font=dict(color='#5DADE2', size=10),
            xanchor='left'
        )
 
        
        fig.update_layout(
            title=dict(
                text='<b>Distribution of Sales Transactions</b>',
                x=0.5,
                font=dict(size=22, color='black')
            ),
            xaxis_title=dict(text='<b>Sales Value (USD)</b>', font=dict(color='black')),
            yaxis_title=dict(text='<b>Number of Transactions</b>', font=dict(color='black')),
            plot_bgcolor='white',
            paper_bgcolor='white',
            bargap=0.05,
            showlegend=False,
            margin=dict(l=80, r=60, t=90, b=60)
        )
 
        
        fig.update_xaxes(
            showline=True, linewidth=2, linecolor='black', mirror=True,
            tickfont=dict(color='black'),
            tickprefix='$',
            gridcolor='#D3D3D3', griddash='dot', showgrid=True
        )
        fig.update_yaxes(
            showline=True, linewidth=2, linecolor='black', mirror=True,
            tickfont=dict(color='black'),
            gridcolor='#D3D3D3', griddash='dot', showgrid=True,
            rangemode='tozero'
        )
 
        return fig
 

    else:
        fig = px.scatter(title=f'Chart "{chart_id}" coming soon...')
        fig.update_layout(template='plotly_white', paper_bgcolor='white')
        return fig