import plotly.express as px
import pandas as pd

def create_chart(df, chart_type):
    if chart_type == 'column':
        # --- 1. Regional Sales Comparison (Column) ---
        # Grouping by Region for Sales as per your requirement
        data = df.groupby('Region')['Sales'].sum().reset_index()
        label_col = 'Region'
        value_col = 'Sales'
        title_text = "Total Sales by Region"
        axis_label = "Sales (Thousands)"
        
        # Sort descending so the winner is on the far left
        data = data.sort_values(by=value_col, ascending=False)

    elif chart_type == 'bar':
        # --- 2. Top 5 Sub-Category Profit (Horizontal Bar) ---
        # Grouping by Sub-Category for Profit as per your requirement
        data = df.groupby('Sub-Category')['Profit'].sum().reset_index()
        # Filtering for Top 5 Magnitude
        data = data.sort_values(by='Profit', ascending=False).head(5)
        
        label_col = 'Sub-Category'
        value_col = 'Profit'
        title_text = "Top 5 Most Profitable Sub-Categories"
        axis_label = "Profit (Thousands)"
        
        # Re-sort ascending for horizontal bar so the winner is at the TOP
        data = data.sort_values(by=value_col, ascending=True)

    # --- Shared Styling Logic ---
    max_val = data[value_col].max()
    data['Color_Group'] = data[value_col].apply(
        lambda x: 'Highest Performer' if x == max_val else 'Standard Performance'
    )

    # Dynamic creation based on chart_type
    if chart_type == 'column':
        fig = px.bar(
            data, x=label_col, y=value_col,
            color='Color_Group',
            color_discrete_map={'Highest Performer': '#90EE90', 'Standard Performance': '#ADD8E6'}
        )
        text_pos = 'outside'
        orientation = 'v'
    else:
        fig = px.bar(
            data, x=value_col, y=label_col,
            orientation='h',
            color='Color_Group',
            color_discrete_map={'Highest Performer': '#90EE90', 'Standard Performance': '#ADD8E6'}
        )
        text_pos = 'outside'
        orientation = 'h'

    # Update Traces and Layout
    fig.update_traces(
        texttemplate='%{y:.2s}' if chart_type == 'column' else '%{x:.2s}',
        textposition=text_pos,
        marker_line_color='black',
        marker_line_width=1
    )
    
    fig.update_layout(
        title=dict(text=f"<b>{title_text}</b>", x=0.5, font=dict(size=20)),
        xaxis_title=f"<b>{label_col if chart_type == 'column' else axis_label}</b>",
        yaxis_title=f"<b>{axis_label if chart_type == 'column' else label_col}</b>",
        plot_bgcolor='white',
        paper_bgcolor='white',
        legend=dict(title=None, orientation="v", y=0.98, x=0.99, xanchor="right", borderwidth=1),
        margin=dict(l=100, r=50, t=80, b=50)
    )
    
    # Add borders to axes
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black', mirror=True)
    
    return fig