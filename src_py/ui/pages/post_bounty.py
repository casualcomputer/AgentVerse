"""
Post Bounty page for the AgentVerse platform.
"""
import streamlit as st
import hashlib
from datetime import datetime

from src_py.config.settings import MODEL_REWARDS
from src_py.services.blockchain import BlockchainService
from src_py.services.ipfs import IPFSService
from src_py.utils.helpers import show_notification, format_cid

def render_page():
    """Render the post bounty page"""
    st.header("Post a New Bounty")
    
    blockchain_service = BlockchainService()
    ipfs_service = IPFSService()
    
    with st.form("bounty_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Bounty Title", placeholder="e.g., Document Classifier Agent")
            description = st.text_area("Description", height=150, 
                placeholder="Describe the task your agent should solve, e.g., 'Classify documents by topic with at least 80% accuracy.'")
            
            # Model selection with dynamic reward
            selected_model = st.selectbox(
                "Select Base Model",
                options=list(MODEL_REWARDS.keys()),
                format_func=lambda x: f"{x} (Reward: {MODEL_REWARDS[x]} FTN)"
            )
            
            # Display the reward amount (read-only)
            st.number_input(
                "Reward Amount (FTN)",
                value=MODEL_REWARDS[selected_model],
                disabled=True,
                help="Reward is automatically set based on model size. Smaller models get higher rewards!"
            )
            
        with col2:
            # Test Harness Section
            st.markdown("### Test Suite")
            st.markdown("""
            Upload your test suite to IPFS to evaluate agent submissions. This should include:
            - Test cases and evaluation criteria
            - Input/output examples
            - Performance metrics
            - Validation scripts
            """)
            
            test_file = st.file_uploader(
                "Upload Test Suite (ZIP)",
                type=['zip'],
                help="Upload a ZIP file containing your test suite. This will be automatically uploaded to IPFS."
            )
            
            if test_file:
                # Upload to IPFS
                test_cid = ipfs_service.upload_file(test_file.getvalue())
                st.success(f"Test suite uploaded! CID: {format_cid(test_cid)}")
                st.info("This CID will be used to fetch and run tests on submitted agents.")
            else:
                test_cid = st.text_input(
                    "Or Enter Existing Test Suite CID",
                    placeholder="Qm...",
                    help="If you've already uploaded your test suite to IPFS, enter its CID here."
                )
            
            st.markdown("### Requirements")
            st.markdown("""
            - Agent must be deployed on IPFS
            - Must use the selected base model
            - Minimum accuracy: 80%
            - Must pass all test cases
            - Smaller models get higher rewards!
            """)
            
            # Model size explanation
            st.info("""
            **Reward Structure:**
            - 0.5B-2B models: 120-150 FTN
            - 3B-4B models: 90-100 FTN
            - 7B models: 70-80 FTN
            """)
        
        submitted = st.form_submit_button("🚀 Post Bounty")
        
        if submitted:
            if not title:
                st.error("Please provide a bounty title")
                return
            
            if not description:
                st.error("Please provide a bounty description")
                return
                
            if not test_cid:
                st.error("Please upload a test suite or provide a valid CID")
                return
                
            try:
                # Submit to blockchain
                tx_receipt = blockchain_service.post_bounty(
                    description=description,
                    reward=MODEL_REWARDS[selected_model],
                    test_cid=test_cid
                )
                
                st.success(f"Bounty posted successfully! Transaction hash: {tx_receipt['tx_hash']}")
                st.info(f"""
                The bounty is now escrowed on Bahamut testnet:
                - Base Model: {selected_model}
                - Reward: {MODEL_REWARDS[selected_model]} FTN
                - Test Suite CID: {format_cid(test_cid)}
                - Anyone can view the criteria and prize amount on-chain.
                """)
            except Exception as e:
                st.error(f"Error posting bounty: {str(e)}") 