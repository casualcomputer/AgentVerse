"""
Oracle Dashboard page for the AgentVerse platform.
Allows admins to trigger payouts for bounties manually.
"""
import streamlit as st
from datetime import datetime

from src_py.services.blockchain import BlockchainService
from src_py.utils.helpers import format_address, format_cid

def render_page():
    """Render the oracle dashboard page"""
    st.header("🔮 Oracle Dashboard")
    
    st.markdown("""
    This dashboard allows you to manually trigger the evaluation and payout process for bounties.
    In a production environment, this would be automated by the oracle service.
    """)
    
    blockchain_service = BlockchainService()
    
    # Admin authentication (simple for demo)
    with st.expander("🔑 Admin Authentication"):
        st.warning("This is a demo. In production, proper authentication would be required.")
        is_authenticated = st.checkbox("I am an authorized oracle operator")
    
    if not is_authenticated:
        st.warning("Please authenticate as an admin to access the oracle dashboard.")
        return
    
    # Bounty selection
    st.subheader("Select Bounty to Process")
    
    # For demo purposes, show fixed bounties
    bounty_options = [
        (1, "Document Classifier Agent - 1 FTN"),
        (2, "Text Summarization Agent - 1 FTN"),
        (3, "Sentiment Analysis Agent - 1 FTN")
    ]
    
    selected_bounty = st.selectbox(
        "Select Bounty ID",
        options=bounty_options,
        format_func=lambda x: f"Bounty #{x[0]}: {x[1]}"
    )
    
    # Show bounty details (for demo)
    st.subheader("Bounty Details")
    st.info(f"""
    **Bounty #{selected_bounty[0]}**
    - Description: {selected_bounty[1]}
    - Deadline: {(datetime.now()).strftime('%Y-%m-%d %H:%M')} (expired)
    - Status: Ready for payout
    """)
    
    # Submissions for this bounty (for demo)
    st.subheader("Submissions")
    
    # Demo submissions with checkboxes for selection
    submissions = [
        {"id": 1, "address": "0x71C7656EC7ab88b098defB751B7401B5f6d8976F", "score": 95},
        {"id": 2, "address": "0x2546BcD3c84621e976D8185a91A922aE77ECEc30", "score": 87},
        {"id": 3, "address": "0xbDA5747bFD65F08deb54cb465eB87D40e51B197E", "score": 78}
    ]
    
    winners = []
    for submission in submissions:
        col1, col2, col3 = st.columns([1, 3, 1])
        with col1:
            is_winner = st.checkbox("Select", key=f"sub_{submission['id']}")
            if is_winner:
                winners.append(submission["address"])
        with col2:
            st.markdown(f"**Agent #{submission['id']}** by {format_address(submission['address'])}")
        with col3:
            st.markdown(f"Score: **{submission['score']}**")
    
    st.markdown("---")
    
    # Payout section
    st.subheader("Trigger Payout")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"Selected Winners: {len(winners)} agent(s)")
        if winners:
            st.markdown("Winner addresses:")
            for addr in winners:
                st.code(addr, language=None)
    
    with col2:
        if winners:
            st.success(f"Each winner will receive {1.0 / len(winners):.4f} FTN")
        else:
            st.warning("No winners selected. Please select at least one winner.")
    
    # Trigger payout button
    if st.button("🚀 Trigger Payout", disabled=len(winners) == 0):
        # Create a progress bar for the transaction
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Update status
            status_text.info("Preparing to execute batch payout...")
            progress_bar.progress(25)
            
            # Process the payout
            status_text.info("Sending transaction to Bahamut blockchain...")
            progress_bar.progress(50)
            
            tx_receipt = blockchain_service.batch_payout(selected_bounty[0], winners)
            
            # Update progress
            status_text.info("Transaction sent! Waiting for confirmation...")
            progress_bar.progress(75)
            
            # Final update
            progress_bar.progress(100)
            status_text.success("Transaction confirmed!")
            
            st.success("🎉 Payout process completed successfully!")
            
            st.info(f"""
            ### Transaction Details:
            - **Transaction Hash**: [{tx_receipt['tx_hash']}](https://horizon.ftnscan.com/tx/{tx_receipt['tx_hash']})
            - **Contract**: [{blockchain_service.contract_address}](https://horizon.ftnscan.com/address/{blockchain_service.contract_address})
            - **Bounty ID**: {selected_bounty[0]}
            - **Winners**: {len(winners)}
            - **Amount Per Winner**: {1.0 / len(winners):.4f} FTN
            
            You can view this transaction on [Bahamut Explorer](https://horizon.ftnscan.com/tx/{tx_receipt['tx_hash']})
            """)
            
        except Exception as e:
            progress_bar.progress(100)
            status_text.error("Transaction failed!")
            st.error(f"Error processing payout: {str(e)}")
            st.error("Please check the console for more details and try again.")
    
    # Show oracle logs
    with st.expander("📜 Oracle Activity Logs"):
        st.code("""
[2025-05-16 13:14:22] INFO: Oracle service started
[2025-05-16 13:14:22] INFO: Checking for expired bounties...
[2025-05-16 13:14:23] INFO: Found 1 expired bounty: Bounty #1
[2025-05-16 13:14:23] INFO: Processing submissions for Bounty #1
[2025-05-16 13:14:24] INFO: Evaluating submission from 0x71C7656EC7ab88b098defB751B7401B5f6d8976F
[2025-05-16 13:14:25] INFO: Score: 95/100
[2025-05-16 13:14:25] INFO: Evaluating submission from 0x2546BcD3c84621e976D8185a91A922aE77ECEc30
[2025-05-16 13:14:26] INFO: Score: 87/100
[2025-05-16 13:14:26] INFO: Evaluating submission from 0xbDA5747bFD65F08deb54cb465eB87D40e51B197E
[2025-05-16 13:14:27] INFO: Score: 78/100
[2025-05-16 13:14:27] INFO: Waiting for manual trigger to execute payout...
        """, language="text") 