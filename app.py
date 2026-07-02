import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Import your chart modules from the charts folder
from charts import bar_column
from charts import stacked
from charts import clusterd
from charts import scatter_bubble
from charts import line_chart
from charts import area_chart
from charts import violin
from charts import Histogram
from charts import Box
# Note: You can add distribution and timeseries imports here as you create those files

# ==============================
# Load & Setup
# ==============================
df = pd.read_csv('data/processed/cleaned_superstore.csv')
if 'Order Date' in df.columns:
    df['Order Date'] = pd.to_datetime(df['Order Date'])

app = dash.Dash(__name__)
app.title = "Executive Dark Dashboard"

# ==============================
# Layout (Same Design & Color)
# ==============================
app.layout = html.Div(style={
    'backgroundColor': '#0f172a', 
    'backgroundImage': 'radial-gradient(circle at top right, #1e293b, #0f172a)',
    'minHeight': '100vh', 'padding': '30px', 'fontFamily': 'Segoe UI', 'color': 'white'
}, children=[
    html.Div([
        html.H1("📊 E-Commerce Sales Performance", style={'margin': '0', 'fontWeight': 'bold'}),
        html.P("Executive Intelligence Dashboard • Custom Edition", style={'color': '#94a3b8'})
    ], style={'textAlign': 'center', 'marginBottom': '30px'}),

    html.Div([
        # Filter 1: Regions
        html.Div([
            html.Label("📍 Regions", style={'fontWeight': 'bold', 'color': '#38bdf8'}),
            dcc.Dropdown(
                id='region-filter',
                options=[{'label': r, 'value': r} for r in sorted(df['Region'].unique())],
                value=list(df['Region'].unique()),
                multi=True,
                style={'color': '#0f172a'}
            )
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '10px'}),

        # Filter 2: Specific Chart Selector
        html.Div([
            html.Label("📈 Analysis View", style={'fontWeight': 'bold', 'color': '#38bdf8'}),
            dcc.Dropdown(
                id='chart-selector',
                options=[
                    # Week 1
                    {'label': 'Column Chart', 'value': 'column'},
                    {'label': 'Bar Chart', 'value': 'bar'},
                    # Week 2
                    {'label': 'Stacked Column Chart', 'value': 'stacked_column'},
                    {'label': 'Stacked Bar Chart', 'value': 'stacked_bar'},
                    {'label': 'Clustered Column Chart', 'value': 'clustered_column'},
                    {'label': 'Clustered Bar Chart', 'value': 'clustered_bar'},
                    # Week 3 & 4
                    {'label': 'Scatter Chart', 'value': 'scatter'},
                    {'label': 'Bubble Chart', 'value': 'bubble'},
                    # Week 5, 6, & 7
                    {'label': 'Histogram Chart', 'value': 'histogram'},
                    {'label': 'Box Chart', 'value': 'box'},
                    {'label': 'Violin Chart', 'value': 'violin'},
                    # Week 8 & 9
                    {'label': 'Line Chart', 'value': 'line'},
                    {'label': 'Area Chart', 'value': 'area'},
                ],
                value='column',
                clearable=False,
                style={'color': '#0f172a'}
            )
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '10px'}),

        # Filter 3: Segments
        html.Div([
            html.Label("👥 Segments", style={'fontWeight': 'bold', 'color': '#38bdf8'}),
            dcc.Checklist(
                id='segment-filter',
                options=[{'label': s, 'value': s} for s in df['Segment'].unique()],
                value=list(df['Segment'].unique()),
                inline=True,
                style={'marginTop': '10px'}
            )
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '10px', 'verticalAlign': 'top'}),
    ], style={'backgroundColor': '#1e293b', 'padding': '20px', 'borderRadius': '20px', 'marginBottom': '30px', 'border': '1px solid #334155'}),

    # KPI Section
    html.Div(id='kpi-cards', style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '30px'}),

    # Graph Section
    html.Div([
        dcc.Graph(id='main-display-graph', style={'height': '600px'})
    ], style={'backgroundColor': '#0f172a', 'padding': '20px', 'borderRadius': '10px', 'border': '1px solid #334155'})
])

# ==============================
# Callback Logic
# ==============================
@app.callback(
    [Output('kpi-cards', 'children'), Output('main-display-graph', 'figure')],
    [Input('region-filter', 'value'), 
     Input('chart-selector', 'value'),
     Input('segment-filter', 'value')]
)
def update_view(regions, chart_id, segments):
    # Dynamic Filtering
    f_df = df[(df['Region'].isin(regions)) & (df['Segment'].isin(segments))]
    
    # Update KPI Cards
    kpi_layout = [
        html.Div([html.Small("SALES"), html.H2(f"${f_df['Sales'].sum():,.0f}")], style={'width': '30%', 'backgroundColor': '#1e293b', 'padding': '20px', 'borderRadius': '15px', 'textAlign': 'right', 'borderRight': '5px solid #38bdf8'}),
        html.Div([html.Small("PROFIT"), html.H2(f"${f_df['Profit'].sum():,.0f}")], style={'width': '30%', 'backgroundColor': '#1e293b', 'padding': '20px', 'borderRadius': '15px', 'textAlign': 'right', 'borderRight': '5px solid #10b981'}),
        html.Div([html.Small("ORDERS"), html.H2(f"{len(f_df):,}")], style={'width': '30%', 'backgroundColor': '#1e293b', 'padding': '20px', 'borderRadius': '15px', 'textAlign': 'right', 'borderRight': '5px solid #f59e0b'}),
    ]

    if f_df.empty:
        return kpi_layout, px.scatter(title="No data matches selection")

    # Routing logic to specific files in /charts/ folder
    try:
        # Week 1
        if chart_id in ['column', 'bar']:
            fig = bar_column.create_chart(f_df, chart_id)
        
        # Week 2
        elif chart_id in ['stacked_column', 'stacked_bar']:
            fig = stacked.create_chart(f_df, chart_id)
        elif chart_id in ['clustered_column', 'clustered_bar']:
            fig = clusterd.create_chart(f_df, chart_id)

        # Week 3 & 4
        elif chart_id in ['scatter', 'bubble']:
            fig = scatter_bubble.create_chart(f_df, chart_id)

        # Week 7 - Violin Chart
        elif chart_id == 'violin':
            fig = violin.create_chart(f_df, chart_id)


        elif chart_id == 'box':
            fig = Box.create_chart(f_df, chart_id)
            

        elif chart_id in ['histogram', 'box', 'violin']:
            fig = Histogram.create_chart(f_df, chart_id)  


        # Week 8
        elif chart_id in ['line']:
            fig = line_chart.create_chart(f_df, chart_id)

        # Week 9
        elif chart_id in ['area']:
            fig = area_chart.create_chart(f_df, chart_id)

        # Week 5-9 placeholders (Add your logic files as you go)
        else:
            fig = px.scatter(title="Chart selection logic being built...")
            fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')

    except AttributeError:
        # Prevents crashing if the file exists but the function isn't ready
        fig = px.scatter(title=f"Function for {chart_id} not yet defined in charts folder")
        fig.update_layout(template="plotly_dark")

    return kpi_layout, fig

if __name__ == '__main__':
    app.run(debug=True)