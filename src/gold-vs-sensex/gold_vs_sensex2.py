import yfinance as yf
import plotly.graph_objects as go

# Fetching gold price data using GLD (SPDR Gold Shares ETF) for the last 10 days
gold_data = yf.download('GLD', period='10d', interval='1d')

# Creating a plotly graph
fig = go.Figure()

# Adding the gold price data as a trace
fig.add_trace(go.Scatter(x=gold_data.index, y=gold_data['Close'],
                         mode='lines', name='Gold Price (GLD)',
                         line=dict(color='gold')))

# Customizing layout
fig.update_layout(
    title='Gold Price for the Last 10 Days (GLD ETF)',
    xaxis_title='Date',
    yaxis_title='Price (USD)',
    template='plotly_dark',  # Dark theme (optional)
    xaxis_rangeslider_visible=False,  # Hide range slider
    hovermode='x unified',  # Unified hover label
)

# Show the plot
fig.show()
