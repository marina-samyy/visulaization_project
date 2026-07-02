import plotly.graph_objects as go
import numpy as np

def create_chart(df, chart_id):
    # --- 1. Data Logic & Jittering for Clutter (Solution 1) ---
    # We add a small amount of random 'noise' to the data to prevent overplotting
    def jitter(series):
        return series + np.random.uniform(-0.01, 0.01, size=len(series))

    fig = go.Figure()

    if chart_id == 'scatter':
        # W3: Discount vs Profit Relationship
        title, x_title, y_title = "Impact of Discount on Profitability", "Discount (%)", "Profit (USD)"
        
        # Rule 6: Color Strategy - Outliers highlighted in Green, standard in Blue
        # Defining outliers as transactions with negative profit despite low discount
        df['is_outlier'] = (df['Profit'] < -500) & (df['Discount'] < 0.2)
        
        # Standard Performance
        std_df = df[~df['is_outlier']]
        fig.add_trace(go.Scatter(
            x=jitter(std_df['Discount']), 
            y=std_df['Profit'],
            mode='markers',
            name='Standard Performance',
            marker=dict(color='#AED6F1', line=dict(width=1, color='black'), size=8)
        ))
        
        # Outliers
        outlier_df = df[df['is_outlier']]
        fig.add_trace(go.Scatter(
            x=jitter(outlier_df['Discount']), 
            y=outlier_df['Profit'],
            mode='markers+text',
            name='Performance Outlier',
            text="Critical Loss", # Rule 8: Outlier labeling
            textposition="top center",
            marker=dict(color='#A9DFBF', line=dict(width=1, color='black'), size=12)
        ))

    elif chart_id == 'bubble':
        # W4: Sales vs Profit with Quantity (Size) and Category (Color)
        title, x_title, y_title = "Sales vs Profit by Product Category", "Sales (USD)", "Profit (USD)"
        
        # Rule 6: Using uniform light colors for different clusters (Categories)
        categories = df['Category'].unique()
        colors = ['#AED6F1', '#A9DFBF', '#FAD7A0'] # Light blue, light green, light orange
        
        for i, cat in enumerate(categories):
            cat_df = df[df['Category'] == cat]
            fig.add_trace(go.Scatter(
                x=cat_df['Sales'],
                y=cat_df['Profit'],
                mode='markers',
                name=cat,
                marker=dict(
                    size=cat_df['Quantity'],
                    sizemode='area',
                    sizeref=2.*max(df['Quantity'])/(40.**2),
                    sizemin=4,
                    color=colors[i % len(colors)],
                    line=dict(width=1, color='black') # Rule 6: Black borders
                )
            ))

    # --- 2. Shared Layout & Rule Compliance ---
    fig.update_layout(
        template='plotly_white',
        title=dict(text=f"<b>{title}</b>", x=0.5, font=dict(size=20, color="black")), # Rule 5
        xaxis_title=dict(text=f"<b>{x_title}</b>", font=dict(color="black")), # Rule 5
        yaxis_title=dict(text=f"<b>{y_title}</b>", font=dict(color="black")), # Rule 5
        # Rule 4: Include Legend top-right
        legend=dict(title=dict(text="<b>Legend</b>"), bordercolor="black", borderwidth=1,
                    yanchor="top", y=0.98, xanchor="right", x=0.98),
        plot_bgcolor='white', 
        paper_bgcolor='white',
        margin=dict(l=80, r=50, t=80, b=50)
    )

    # Rule 1 & 2: Black border and Zero Baseline
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black', mirror=True,
                     gridcolor='#D3D3D3', griddash='dot', showgrid=True) # Rule 7
    
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black', mirror=True,
                     zeroline=True, zerolinecolor='black', zerolinewidth=2, # Rule 2
                     gridcolor='#D3D3D3', griddash='dot', showgrid=True) # Rule 7

    return fig