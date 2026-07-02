import plotly.express as px
import pandas as pd

def create_chart(df, chart_id):
    # --- 1. Data Preparation & Aggregation ---
    if chart_id == 'stacked_column':
        title, x_title, y_title = "Total Sales by Region and Segment", "Region", "Sales"
        label_col, value_col, color_col = 'Region', 'Sales', 'Segment'
        orientation = 'v'
        data = df.groupby([label_col, color_col])[value_col].sum().reset_index()
        total_order = data.groupby(label_col)[value_col].sum().sort_values(ascending=False).index.tolist()
        
    elif chart_id == 'stacked_bar':
        title, x_title, y_title = "Profit Composition by Sub-Category", "Profit", "Sub-Category"
        label_col, value_col, color_col = 'Sub-Category', 'Profit', 'Segment'
        orientation = 'h'
        data = df.groupby([label_col, color_col])[value_col].sum().reset_index()
        total_order = data.groupby(label_col)[value_col].sum().sort_values(ascending=False).head(7).index.tolist()[::-1]
        data = data[data[label_col].isin(total_order)]

    # --- 2. Lighter Color Strategy (Soft Gradients) ---
    winner_label = total_order[-1] if orientation == 'h' else total_order[0]
    
    # Even lighter "Soft" Palettes
    blue_shades = ['#D6EAF8', '#85C1E9', '#3498DB'] # Very Light, Soft Blue, Blue
    green_shades = ['#E8F8F5', '#A3E4D7', '#48C9B0'] # Very Light, Soft Green, Teal-Green
    
    unique_segs = sorted(data[color_col].unique())
    color_map = {}
    for label in data[label_col].unique():
        shades = green_shades if label == winner_label else blue_shades
        for i, seg in enumerate(unique_segs):
            color_map[f"{label}_{seg}"] = shades[i % len(shades)]

    data['Color_Key'] = data[label_col] + "_" + data[color_col]

    # --- 3. Create Figure ---
    fig = px.bar(
        data, 
        x=label_col if orientation == 'v' else value_col,
        y=value_col if orientation == 'v' else label_col,
        color='Color_Key',
        orientation=orientation,
        category_orders={label_col: total_order},
        color_discrete_map=color_map,
        template="plotly_white"
    )

    # --- 4. Styling & Clean Gridlines ---
    fig.update_traces(
        texttemplate='<b>%{value:.2s}</b>', 
        textposition='inside',
        insidetextfont=dict(color='black', size=11),
        marker_line_color='white', 
        marker_line_width=1.5,
        showlegend=False 
    )

    # Manual Dual Legend
    for i, seg in enumerate(unique_segs):
        fig.add_bar(x=[None], y=[None], name=f"{seg} (Standard)", 
                    marker_color=blue_shades[i % len(blue_shades)], showlegend=True)
    for i, seg in enumerate(unique_segs):
        fig.add_bar(x=[None], y=[None], name=f"{seg} (Winner)", 
                    marker_color=green_shades[i % len(green_shades)], showlegend=True)

    fig.update_layout(
        title=dict(text=f"<b>{title}</b>", x=0.5, font=dict(size=22, color="black")),
        xaxis_title=dict(text=f"<b>{x_title}</b>", font=dict(color="black")),
        yaxis_title=dict(text=f"<b>{y_title}</b>", font=dict(color="black")),
        legend=dict(title=dict(text="<b>Revenue Breakdown</b>"), bordercolor="black", borderwidth=1, 
                    yanchor="top", y=0.98, xanchor="right", x=0.98),
        margin=dict(l=120, r=50, t=80, b=50),
        plot_bgcolor='white', paper_bgcolor='white'
    )

    # --- THE GRIDLINE FIX ---
    # Common border/line style
    line_style = dict(showline=True, linewidth=2, linecolor='black', mirror=True, tickfont=dict(color='black'))
    # Dotted grid style for the numbers axis
    grid_style = dict(gridcolor='#D3D3D3', griddash='dot', zeroline=True, zerolinecolor='black', zerolinewidth=2)

    if orientation == 'v':
        # Vertical Chart: Gridlines on Y (Numbers), No grid on X (Labels)
        fig.update_xaxes(**line_style, showgrid=False) 
        fig.update_yaxes(**line_style, **grid_style, showgrid=True, rangemode="tozero")
    else:
        # Horizontal Chart: Gridlines on X (Numbers), No grid on Y (Labels)
        fig.update_xaxes(**line_style, **grid_style, showgrid=True, rangemode="tozero")
        fig.update_yaxes(**line_style, showgrid=False)

    return fig