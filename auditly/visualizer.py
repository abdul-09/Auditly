import plotly.graph_objects as go
import streamlit as st

def create_score_gauge(score):
    """Create a gauge chart for the overall SEO score"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {
            'axis': {'range': [0, 100], 'tickwidth': 1},
            'bar': {'color': "rgba(255, 75, 75, 0.8)"},
            'steps': [
                {'range': [0, 33], 'color': "rgba(255, 0, 0, 0.1)"},
                {'range': [33, 66], 'color': "rgba(255, 165, 0, 0.1)"},
                {'range': [66, 100], 'color': "rgba(0, 255, 0, 0.1)"}
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': score
            }
        }
    ))

    fig.update_layout(
        height=300,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': "white"}
    )

    st.plotly_chart(fig, use_container_width=True)

def create_metrics_chart(metrics):
    """Create a bar chart for different SEO metrics"""
    fig = go.Figure()
    
    categories = list(metrics.keys())
    values = list(metrics.values())
    
    fig.add_trace(go.Bar(
        x=categories,
        y=values,
        marker_color='rgba(255, 75, 75, 0.8)',
        text=values,
        textposition='auto',
    ))

    fig.update_layout(
        height=300,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': "white"},
        yaxis=dict(
            range=[0, 100],
            gridcolor='rgba(255,255,255,0.1)'
        ),
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.1)'
        )
    )

    st.plotly_chart(fig, use_container_width=True)
