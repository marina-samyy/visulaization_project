import plotly.graph_objects as go
import pandas as pd
import numpy as np

def create_chart(df, chart_id):
    categories = df['Category'].unique()
    
    colors = {
        'Furniture': '#AED6F1',       
        'Office Supplies': '#A9DFBF',  
        'Technology': '#FAD7A0'        
    }

    fig = go.Figure()

    for cat in categories:
        cat_df = df[df['Category'] == cat]['Profit']
        q1 = cat_df.quantile(0.01)
        q99 = cat_df.quantile(0.99)
        cat_df = cat_df.clip(lower=q1, upper=q99)
        median_val = cat_df.median()

        fig.add_trace(go.Violin(
            x=[cat] * len(cat_df),
            y=cat_df,
            name=cat,
            width=0.8,
            fillcolor=colors.get(cat, '#AED6F1'),
            opacity=0.8,
            
            line_color='black',
            line_width=1.5,
            
            box_visible=True,
            box_fillcolor='white',
            
            meanline_visible=False,
            points='outliers',
            pointpos=0,
            marker=dict(
                color='black',
                size=4,
                opacity=0.5
            ),

            showlegend=True,
        ))

        fig.add_annotation(
            x=cat,
            y=median_val,
            text=f"<b>{median_val:.1f}</b>",
            showarrow=False,
            yshift=18,
            font=dict(size=11, color='black'),
            bgcolor='white',
            bordercolor='black',
            borderwidth=1
        )

    fig.update_layout(
        title=dict(
            text="<b>Profit Distribution by Product Category</b>",
            x=0.5,
            font=dict(size=20, color='black', family='Arial')
        ),
        xaxis_title='<b>Category</b>',
        yaxis_title='<b>Profit (USD)</b>',

        showlegend=True,
        legend=dict(
            title=dict(text='<b>Category</b>'),
            bordercolor='black',
            borderwidth=1,
            yanchor='top',
            y=0.98,
            xanchor='right',
            x=0.98
        ),

        plot_bgcolor='white',
        paper_bgcolor='white',
        violinmode='group',
        margin=dict(l=60, r=40, t=80, b=60),

        xaxis=dict(
            showline=True, linewidth=2,
            linecolor='black', mirror=True,
            showgrid=False
        ),
        yaxis=dict(
            showline=True, linewidth=2,
            linecolor='black', mirror=True,
            zeroline=True, zerolinecolor='black', zerolinewidth=2,
            gridcolor='#D3D3D3', griddash='dot', showgrid=True,
        ),
    )

    return fig