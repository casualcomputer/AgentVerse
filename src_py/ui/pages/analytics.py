"""
Analytics page for the AgentVerse platform.
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def render_page():
    """Render the analytics page"""
    st.header("📊 Analytics")
    
    # Sample metrics data
    metrics = {
        'total_bounties': 12,
        'new_bounties': 3,
        'total_submissions': 25,
        'new_submissions': 8,
        'total_rewards': 1500,
        'new_rewards': 500
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            label="Total Bounties",
            value=metrics['total_bounties'],
            delta=f"{metrics['new_bounties']} new this week"
        )
        
        st.metric(
            label="Total Rewards",
            value=f"{metrics['total_rewards']} FTN",
            delta=f"{metrics['new_rewards']} FTN this week"
        )
    
    with col2:
        st.metric(
            label="Active Bounties",
            value="5",
            delta="2 new"
        )
        
        st.metric(
            label="Average Score",
            value="87%",
            delta="2% increase"
        )
    
    # Generate sample chart data
    chart_data = generate_sample_chart_data()
    
    # Activity chart
    st.subheader("Platform Activity")
    st.line_chart(chart_data[['Bounties', 'Submissions']])
    
    # Rewards chart
    st.subheader("Rewards Distribution")
    st.area_chart(chart_data[['Rewards']])
    
    # Model distribution chart
    model_data = {
        'Model': ['Google Gemma 2B', 'Microsoft Phi-3-mini', 'Qwen 0.5B', 'Mistral 7B', 'Qwen 7B'],
        'Count': [8, 6, 5, 4, 2]
    }
    st.subheader("Model Popularity")
    st.bar_chart(pd.DataFrame(model_data).set_index('Model'))

def generate_sample_chart_data():
    """Generate sample chart data for demo purposes"""
    # Generate 15 days of data
    dates = pd.date_range(end=datetime.now(), periods=15, freq='D')
    
    # Generate sample values with an upward trend and some randomness
    import random
    bounties = [i + random.randint(0, 2) for i in range(1, 16)]
    submissions = [b * random.randint(2, 3) for b in bounties]
    rewards = [s * random.randint(80, 120) for s in submissions]
    
    return pd.DataFrame({
        'Date': dates,
        'Bounties': bounties,
        'Submissions': submissions,
        'Rewards': rewards
    }).set_index('Date') 