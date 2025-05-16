"""
Main application entry point for the AgentVerse platform.
"""
import streamlit as st
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add the parent directory to Python path so src_py is recognized as a module
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))

# Load environment variables from .env file if it exists
if os.path.exists(".env"):
    load_dotenv()

# Import UI components
from src_py.ui.components.sidebar import render_sidebar
from src_py.ui.components.footer import render_footer

# Import page renderers
from src_py.ui.pages.post_bounty import render_page as render_post_bounty
from src_py.ui.pages.leaderboard import render_page as render_leaderboard
from src_py.ui.pages.submit_agent import render_page as render_submit_agent
from src_py.ui.pages.analytics import render_page as render_analytics
from src_py.ui.pages.featured_bounties import render_page as render_featured_bounties
from src_py.ui.pages.oracle_dashboard import render_page as render_oracle_dashboard
from src_py.ui.pages.legal_data_explorer import render_page as render_legal_data_explorer

# Import settings
from src_py.config.settings import APP_CONFIG, UI_CONFIG

def main():
    """Main application entry point"""
    # Set page configuration
    st.set_page_config(
        page_title=APP_CONFIG['title'],
        page_icon=APP_CONFIG['icon'],
        layout=APP_CONFIG['layout'],
        initial_sidebar_state=APP_CONFIG['initial_sidebar_state']
    )
    
    # Apply custom CSS
    st.markdown(UI_CONFIG['css'], unsafe_allow_html=True)
    
    # Render sidebar
    render_sidebar()
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📝 Post Bounty", 
        "🤖 Submit Agent", 
        "🏆 Leaderboard", 
        "📊 Analytics", 
        "🌟 Featured Bounties",
        "📚 Legal Data Explorer"
    ])
    
    # Render each tab
    with tab1:
        render_post_bounty()
    with tab2:
        render_submit_agent()
    with tab3:
        render_leaderboard()
    with tab4:
        render_analytics()
    with tab5:
        render_featured_bounties()
    with tab6:
        render_legal_data_explorer()
    
    # Render footer
    render_footer()

if __name__ == "__main__":
    main() 