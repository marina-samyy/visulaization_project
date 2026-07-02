import plotly.graph_objects as go
 
def create_chart(df, chart_id):
 
    if chart_id == 'box':
        
 
        categories = df['Category'].unique()
 
       
        colors = {
            'Furniture':        '#AED6F1',  # Light blue
            'Office Supplies':  '#A9DFBF',  # Light green
            'Technology':       '#FAD7A0',  # Light orange
        }
 
        fig = go.Figure()
 
        for cat in categories:
            cat_df = df[df['Category'] == cat]['Profit']
 
            fig.add_trace(go.Box(
                y=cat_df,
                name=cat,
                marker=dict(
                    color=colors.get(cat, '#D5D8DC'),
                    outliercolor='#E74C3C',          # Red outliers
                    line=dict(color='black', width=1)
                ),
                line=dict(color='black', width=1.5),
                boxmean='sd',                        
                boxpoints='outliers',                
            ))
 
        
        fig.update_layout(
            title=dict(
                text='<b>Profit Distribution by Product Category</b>',
                x=0.5,
                font=dict(size=22, color='black')
            ),
            xaxis_title=dict(text='<b>Product Category</b>', font=dict(color='black')),
            yaxis_title=dict(text='<b>Profit (USD)</b>',      font=dict(color='black')),
            plot_bgcolor='white',
            paper_bgcolor='white',
            showlegend=True,
            legend=dict(
                title=dict(text='<b>Category</b>'),
                bordercolor='black', borderwidth=1,
                yanchor='top', y=0.98, xanchor='right', x=0.98
            ),
            margin=dict(l=80, r=60, t=90, b=60)
        )
 
        fig.update_xaxes(
            showline=True, linewidth=2, linecolor='black', mirror=True,
            tickfont=dict(color='black'),
            showgrid=False
        )
        fig.update_yaxes(
            showline=True, linewidth=2, linecolor='black', mirror=True,
            tickfont=dict(color='black'),
            tickprefix='$',
            gridcolor='#D3D3D3', griddash='dot', showgrid=True,
            zeroline=True, zerolinecolor='black', zerolinewidth=2
        )
 
        return fig
 