"""
Post Bounty page for the AgentVerse platform.
"""
import streamlit as st
from datetime import datetime, timedelta

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
            
            # Display the fixed reward amount (1 FTN for demo)
            st.info("For this demo, all bounties are posted with a 1 FTN reward")
            reward = st.number_input(
                "Reward Amount (FTN)",
                value=1.0,
                disabled=True,
                help="Reward is fixed at 1 FTN for this demo"
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
            
            # Add a deadline display
            deadline = datetime.now() + timedelta(days=1)
            st.info(f"Bounty Deadline: {deadline.strftime('%Y-%m-%d %H:%M')} (24 hours from posting)")
            
            st.markdown("### Requirements")
            st.markdown("""
            - Agent must be deployed on IPFS
            - Must pass all test cases
            - Must be submitted before the deadline
            """)
        
        submitted = st.form_submit_button("🚀 Post Bounty")
        
        if submitted:
            if not title:
                st.error("Please provide a bounty title")
                return
            
            if not description:
                st.error("Please provide a bounty description")
                return
                
            # Create a progress bar for the transaction
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Update status
                status_text.info("Preparing to post bounty on Bahamut blockchain...")
                progress_bar.progress(25)
                
                # Combine title and description
                full_description = f"{title}: {description}"
                
                # Submit to blockchain
                status_text.info("Sending transaction to Bahamut blockchain...")
                progress_bar.progress(50)
                
                tx_receipt = blockchain_service.post_bounty(full_description)
                
                # Update progress
                status_text.info("Transaction sent! Waiting for confirmation...")
                progress_bar.progress(75)
                
                # Final update
                progress_bar.progress(100)
                status_text.success("Transaction confirmed!")
                
                st.success(f"🎉 Bounty posted successfully!")
                
                st.info(f"""
                ### Transaction Details:
                - **Transaction Hash**: [{tx_receipt['tx_hash']}](https://horizon.ftnscan.com/tx/{tx_receipt['tx_hash']})
                - **Contract**: [{blockchain_service.contract_address}](https://horizon.ftnscan.com/address/{blockchain_service.contract_address})
                - **Description**: {full_description}
                - **Reward**: 1 FTN
                - **Deadline**: {deadline.strftime('%Y-%m-%d %H:%M')} (24 hours from now)
                
                You can view this transaction on [Bahamut Explorer](https://horizon.ftnscan.com/tx/{tx_receipt['tx_hash']})
                """)
                
            except Exception as e:
                progress_bar.progress(100)
                status_text.error("Transaction failed!")
                st.error(f"Error posting bounty: {str(e)}")
                st.error("Please check the console for more details and try again.") 