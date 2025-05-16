"""
Submit Agent page for the AgentVerse platform.
"""
import streamlit as st
import hashlib
from datetime import datetime

from src_py.services.blockchain import BlockchainService
from src_py.services.ipfs import IPFSService
from src_py.utils.helpers import format_cid, calculate_hash

def render_page():
    """Render the submit agent page"""
    st.header("Submit Your Agent")
    
    blockchain_service = BlockchainService()
    ipfs_service = IPFSService()
    
    # Development tools section (outside the form)
    st.markdown("### Develop Your Agent")
    st.markdown("""
    You can develop and test your agent in two ways:
    1. **Use Google Colab** (Recommended for beginners)
       - Click below to open our template notebook
       - All dependencies are pre-installed
       - Test your code before submission
    
    2. **Local Development**
       - Download our requirements.txt
       - Use your preferred IDE
       - Test against our validation script
    """)
    
    # Development Tools
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📓 Open Colab Template"):
            st.markdown("[👉 Open in Colab](https://colab.research.google.com/github/your-repo/agent-template.ipynb)")
    
    with col2:
        if st.button("📥 Download Requirements"):
            st.download_button(
                "requirements.txt",
                "streamlit==1.31.0\nweb3==6.11.1\npandas==2.1.4\nnumpy==1.24.3\ntorch==2.1.2\ntransformers==4.36.2",
                "requirements.txt",
                "text/plain"
            )
    
    with col3:
        if st.button("📚 View Documentation"):
            st.markdown("[📖 Read the Docs](https://your-docs-url)")
    
    # Submission Form
    with st.form("submit_agent_form"):
        # Get available bounties
        bounties = blockchain_service.get_events('BountyPosted')
        bounty_options = [(b['args']['bountyId'], f"{b['args']['description']} - {b['args']['amount']}") 
                         for b in bounties]
        
        if not bounty_options:
            bounty_options = [(1, "Document Classifier Agent - 100 FTN")]  # Default demo value
        
        # Select bounty
        bounty_id = st.selectbox(
            "Select Bounty",
            options=bounty_options,
            format_func=lambda x: x[1]
        )
        
        # File upload section
        st.markdown("### Upload Your Solution")
        st.markdown("""
        Your submission should include:
        - `agent.py`: Your main agent code
        - `requirements.txt`: Any additional dependencies
        - `README.md`: Documentation of your approach
        """)
        
        # Main agent code
        agent_code = st.text_area(
            "Agent Code (agent.py)",
            height=300,
            help="Paste your main agent code here. This should include your Agent class with predict() method."
        )
        
        # Additional files
        col1, col2 = st.columns(2)
        with col1:
            agent_name = st.text_input(
                "Agent Name",
                placeholder="e.g., DocClassifier-v1"
            )
            
            requirements = st.text_area(
                "Additional Requirements",
                height=100,
                help="List any additional Python packages your agent needs (beyond the base requirements)."
            )
        with col2:
            agent_description = st.text_area(
                "Description",
                height=100,
                placeholder="Briefly describe your approach and key features"
            )
            
            readme = st.text_area(
                "Documentation (README.md)",
                height=100,
                help="Briefly describe your approach, any special considerations, and how to use your agent."
            )
        
        # Code validation
        if agent_code:
            st.markdown("### Code Validation")
            try:
                # Basic syntax check
                compile(agent_code, '<string>', 'exec')
                st.success("✅ Code syntax is valid")
                
                # Check for required components
                if "class Agent" in agent_code and "def predict" in agent_code:
                    st.success("✅ Contains required Agent class and predict method")
                else:
                    st.warning("⚠️ Make sure your code includes an Agent class with a predict method")
                
                # Check for common issues
                if "import torch" in agent_code or "import transformers" in agent_code:
                    st.info("ℹ️ Using PyTorch/Transformers - make sure to specify version in requirements")
                
            except SyntaxError as e:
                st.error(f"❌ Syntax error in code: {str(e)}")
        
        # Submit button
        submitted = st.form_submit_button("🚀 Submit Agent")
        
        if submitted:
            if not agent_name:
                st.error("Please provide an agent name")
                return
                
            if not agent_code:
                st.error("Please provide your agent code")
                return
                
            try:
                # Upload agent code to IPFS
                agent_cid = ipfs_service.upload_file(agent_code.encode(), "agent.py")
                
                # Calculate code hash
                code_hash = calculate_hash(agent_code)
                
                # Submit to blockchain
                tx = blockchain_service.submit_agent(
                    bounty_id[0],
                    agent_cid,
                    code_hash
                )
                
                st.success("""
                🎉 Submission received! Here's what happens next:
                
                1. **Validation Phase**
                   - Code syntax check
                   - Dependency verification
                   - Basic functionality test
                
                2. **Testing Phase**
                   - Running against test cases
                   - Performance evaluation
                   - Resource usage check
                
                3. **Results**
                   - You'll receive an email with results
                   - Check the leaderboard for your score
                   - If successful, reward will be sent to your wallet
                """)
                
                # Show submission details
                st.info(f"""
                **Submission Details:**
                - Bounty: {bounty_id[1]}
                - Agent Name: {agent_name}
                - Code Length: {len(agent_code)} characters
                - IPFS CID: {format_cid(agent_cid)}
                - Transaction Hash: {tx['tx_hash']}
                """)
                
            except Exception as e:
                st.error(f"Error submitting agent: {str(e)}")
    
    # Help section
    with st.expander("ℹ️ Submission Guidelines"):
        st.markdown("""
        ### How to Submit
        
        1. **Prepare Your Code**
           - Use the template notebook or start from scratch
           - Implement the Agent class with predict() method
           - Test locally before submission
        
        2. **Required Components**
           ```python
           class Agent:
               def __init__(self):
                   # Initialize your model here
                   pass
                   
               def predict(self, input_data):
                   # Your prediction logic here
                   return prediction
           ```
        
        3. **Best Practices**
           - Document your code
           - Handle errors gracefully
           - Optimize for performance
           - Follow the template structure
        
        4. **Evaluation Criteria**
           - Code quality and documentation
           - Prediction accuracy
           - Resource efficiency
           - Error handling
        """) 