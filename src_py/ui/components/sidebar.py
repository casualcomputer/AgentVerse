"""
Sidebar component for the AgentVerse platform.
"""
import streamlit as st

def render_sidebar():
    """Render the application sidebar"""
    with st.sidebar:
        st.image("https://via.placeholder.com/150", width=150)
        st.title("AI Agent Marketplace")
        st.markdown("---")
        
        # Navigation options here if needed
        
        st.markdown("---")
        st.markdown("### About")
        st.info("""
        This marketplace allows you to:
        - Post bounties for AI agents
        - Submit your AI agents
        - Win rewards in FTN tokens
        """) 