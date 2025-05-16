"""
Leaderboard page for the AgentVerse platform.
"""
import streamlit as st
from src_py.services.blockchain import BlockchainService
from src_py.utils.helpers import format_cid, format_tx_hash, format_address

def render_page():
    """Render the leaderboard page"""
    st.header("🏆 Bounty Leaderboard")
    
    blockchain_service = BlockchainService()
    
    # Refresh button
    if st.button("🔄 Refresh"):
        st.info("Refreshing leaderboard data...")
    
    # Get bounty data from blockchain
    try:
        bounties = blockchain_service.get_events('BountyPosted')
        
        if not bounties:
            st.info("No active bounties at the moment. Be the first to post one!")
            return
            
        for bounty in bounties:
            with st.expander(f"{bounty['args']['description']} - {bounty['args']['amount']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Creator:** {format_address(bounty['args']['creator'])}")
                    st.write(f"**Bounty ID:** {bounty['args']['bountyId']}")
                with col2:
                    st.write(f"**Status:** Active")
                    
                    # Get submissions for this bounty
                    submissions = blockchain_service.get_submissions(bounty['args']['bountyId'])
                    st.write(f"**Submissions:** {len(submissions)}")
                
                # Show submissions if available
                if submissions:
                    st.markdown("### Submissions")
                    for submission in submissions:
                        st.markdown(f"""
                        - **Agent ID:** {submission['agent_id']}
                        - **Submitter:** {format_address(submission['submitter'])}
                        - **IPFS CID:** {format_cid(submission['ipfs_cid'])}
                        - **Submitted:** {submission['timestamp']}
                        """)
                        
                # Allow viewing details
                if st.button("View Requirements", key=f"view_{bounty['args']['bountyId']}"):
                    st.info("Agent builders now have access to the requirements and the allowed base model. All test cases are open, fair, and reproducible.")
    
    except Exception as e:
        st.error(f"Error loading leaderboard: {str(e)}") 