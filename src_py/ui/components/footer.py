"""
Footer component for the AgentVerse platform.
"""
import streamlit as st
from src_py.config.settings import APP_CONFIG

def render_footer():
    """Render the application footer"""
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center'>
        <p>Built on Bahamut blockchain for AI + On-chain Logic competition</p>
        <p>© 2024 AI Agent Marketplace. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True) 