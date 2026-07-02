# import plotly.graph_objects as go
# import pandas as pd

# def create_chart(df, chart_id):
#     # --- 1. Data Aggregation & Logic ---
#     if chart_id == 'clustered_column':
#         # Column Rule 10: Show the "winner" on the far left
#         title, x_title, y_title = "Regional Performance: Sales vs Profit", "Summarized Regional Units", "Values (USD)"
#         label_col = 'Region'
#         orientation = 'v'
#         data = df.groupby(label_col)[['Sales', 'Profit']].sum().reset_index()
#         data = data.sort_values('Sales', ascending=False)
#         total_order = data[label_col].tolist()
        
#     elif chart_id == 'clustered_bar':
#         # Bar Rule 9: Order magnitudes from top to bottom
#         title, x_title, y_title = "Category Profitability Overview", "Monetary Value", "Product Categories"
#         label_col = 'Category'
#         orientation = 'h'
#         data = df.groupby(label_col)[['Sales', 'Profit']].sum().reset_index()
#         data = data.sort_values('Sales', ascending=True)
#         total_order = data[label_col].tolist()

#     # --- 2. Color Strategy (Rule 7/8) ---
#     # Winner gets soft orange/gold, standard gets soft blue
#     winner_label = total_order[0] if orientation == 'v' else total_order[-1]
    
#     sales_colors = ['#FAD7A0' if x == winner_label else '#AED6F1' for x in data[label_col]]
#     profit_colors = ['#F8C471' if x == winner_label else '#5DADE2' for x in data[label_col]]

#     fig = go.Figure()

#     # Sales Trace
#     fig.add_trace(go.Bar(
#         name='Sales',
#         x=data[label_col] if orientation == 'v' else data['Sales'],
#         y=data['Sales'] if orientation == 'v' else data[label_col],
#         orientation=orientation,
#         marker_color=sales_colors,
#         text=data['Sales'].apply(lambda x: f"{x/1000:.1f}k"), # Rule 4/5: Show Magnitudes
#         textposition='outside'
#     ))

#     # Profit Trace
#     fig.add_trace(go.Bar(
#         name='Profit',
#         x=data[label_col] if orientation == 'v' else data['Profit'],
#         y=data['Profit'] if orientation == 'v' else data[label_col],
#         orientation=orientation,
#         marker_color=profit_colors,
#         text=data['Profit'].apply(lambda x: f"{x/1000:.1f}k"), # Rule 4/5: Show Magnitudes
#         textposition='outside'
#     ))

#     # --- 3. Layout & Formatting Rules ---
#     fig.update_layout(
#         barmode='group',
#         template='plotly_white',
#         title=dict(text=f"<b>{title}</b>", x=0.5, font=dict(size=22, color="black")), # Rule 6/7
#         xaxis_title=dict(text=f"<b>{x_title}</b>", font=dict(color="black")),
#         yaxis_title=dict(text=f"<b>{y_title}</b>", font=dict(color="black")),
#         # Rule 5/6: Include Legend top-right
#         legend=dict(title=dict(text="<b>Metrics Breakdown</b>"), bordercolor="black", borderwidth=1,
#                     yanchor="top", y=0.98, xanchor="right", x=0.98),
#         margin=dict(l=120, r=50, t=80, b=50),
#         plot_bgcolor='white', paper_bgcolor='white'
#     )

#     # Rule 1, 2, 8, 9: Borders, Zero Baseline, and Dotted Gridlines
#     axis_config = dict(
#         showline=True, linewidth=2, linecolor='black', mirror=True, 
#         tickfont=dict(color='black', size=12),
#         zeroline=True, zerolinecolor='black', zerolinewidth=2
#     )
    
#     grid_style = dict(gridcolor='#D3D3D3', griddash='dot', showgrid=True)

#     if orientation == 'v':
#         # Labels horizontal (Rule 3), Gridlines only on numbers (Y)
#         fig.update_xaxes(**axis_config, showgrid=False)
#         fig.update_yaxes(**axis_config, **grid_style, rangemode="tozero")
#     else:
#         # Labels horizontal (Rule 3), Gridlines only on numbers (X)
#         fig.update_xaxes(**axis_config, **grid_style, rangemode="tozero")
#         fig.update_yaxes(**axis_config, showgrid=False)

#     return fig


import plotly.graph_objects as go
import pandas as pd

def create_chart(df, chart_id):
    # --- 1. Data Aggregation & Logic ---
    if chart_id == 'clustered_column':
        title, x_title, y_title = "Regional Performance: Sales vs Profit", "Summarized Regional Units", "Values (USD)"
        label_col = 'Region'
        orientation = 'v'
        data = df.groupby(label_col)[['Sales', 'Profit']].sum().reset_index()
        # Rule 10: Winner on the far left
        data = data.sort_values('Sales', ascending=False)
        total_order = data[label_col].tolist()
        
    elif chart_id == 'clustered_bar':
        title, x_title, y_title = "Category Profitability Overview", "Monetary Value", "Product Categories"
        label_col = 'Category'
        orientation = 'h'
        data = df.groupby(label_col)[['Sales', 'Profit']].sum().reset_index()
        # Rule 9: Ordered magnitudes
        data = data.sort_values('Sales', ascending=True)
        total_order = data[label_col].tolist()

    # --- 2. Professional Color Strategy ---
    winner_label = total_order[0] if orientation == 'v' else total_order[-1]
    
    # Light Green & Medium Green for Winner
    winner_sales_color, winner_profit_color = '#A9DFBF', '#229954' 
    # Light Blue & Medium Blue for Standard
    std_sales_color, std_profit_color = '#AED6F1', '#3498DB'

    sales_colors = [winner_sales_color if x == winner_label else std_sales_color for x in data[label_col]]
    profit_colors = [winner_profit_color if x == winner_label else std_profit_color for x in data[label_col]]

    fig = go.Figure()

    # Sales Trace (Primary Data)
    fig.add_trace(go.Bar(
        x=data[label_col] if orientation == 'v' else data['Sales'],
        y=data['Sales'] if orientation == 'v' else data[label_col],
        orientation=orientation,
        marker_color=sales_colors,
        text=data['Sales'].apply(lambda x: f"{x/1000:.1f}k"),
        textposition='outside',
        showlegend=False # Hide auto-legend to build the custom one below
    ))

    # Profit Trace (Secondary Data)
    fig.add_trace(go.Bar(
        x=data[label_col] if orientation == 'v' else data['Profit'],
        y=data['Profit'] if orientation == 'v' else data[label_col],
        orientation=orientation,
        marker_color=profit_colors,
        text=data['Profit'].apply(lambda x: f"{x/1000:.1f}k"),
        textposition='outside',
        showlegend=False
    ))

    # --- 3. Manual Legend Creation (Rule 5/6) ---
    # Legend for Winner (Green)
    fig.add_trace(go.Bar(x=[None], y=[None], name="Sales (Winner)", marker_color=winner_sales_color))
    fig.add_trace(go.Bar(x=[None], y=[None], name="Profit (Winner)", marker_color=winner_profit_color))
    # Legend for Standard (Blue)
    fig.add_trace(go.Bar(x=[None], y=[None], name="Sales (Standard)", marker_color=std_sales_color))
    fig.add_trace(go.Bar(x=[None], y=[None], name="Profit (Standard)", marker_color=std_profit_color))

    # --- 4. Layout & Styling Rules ---
    fig.update_layout(
        barmode='group',
        template='plotly_white',
        title=dict(text=f"<b>{title}</b>", x=0.5, font=dict(size=22, color="black")),
        xaxis_title=dict(text=f"<b>{x_title}</b>", font=dict(color="black")),
        yaxis_title=dict(text=f"<b>{y_title}</b>", font=dict(color="black")),
        legend=dict(
            title=dict(text="<b>Metrics Breakdown</b>"), 
            bordercolor="black", borderwidth=1,
            yanchor="top", y=0.98, xanchor="right", x=0.98
        ),
        margin=dict(l=120, r=50, t=80, b=50),
        plot_bgcolor='white', paper_bgcolor='white'
    )

    # Rule 1, 2, 8: Border, Zero Baseline, and Dotted Gridlines
    axis_config = dict(
        showline=True, linewidth=2, linecolor='black', mirror=True, 
        tickfont=dict(color='black', size=12),
        zeroline=True, zerolinecolor='black', zerolinewidth=2
    )
    grid_style = dict(gridcolor='#D3D3D3', griddash='dot', showgrid=True)

    if orientation == 'v':
        fig.update_xaxes(**axis_config, showgrid=False)
        fig.update_yaxes(**axis_config, **grid_style, rangemode="tozero")
    else:
        fig.update_xaxes(**axis_config, **grid_style, rangemode="tozero")
        fig.update_yaxes(**axis_config, showgrid=False)

    return fig