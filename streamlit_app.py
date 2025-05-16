import asyncio
import streamlit as st
import requests
from datetime import datetime
import json
import hashlib
import os
from pathlib import Path
import tarfile
import tempfile
import pandas as pd
from dotenv import load_dotenv

# Create and set a new event loop if one doesn't exist
try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

# Set page configuration
st.set_page_config(
    page_title="AI Agent Bounty Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 4rem;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0 0;
        gap: 1rem;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ffffff;
        border-radius: 4px 4px 0 0;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #4CAF50;
        color: white;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .bounty-card {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #ffffff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .success-message {
        padding: 1rem;
        border-radius: 5px;
        background-color: #d4edda;
        color: #155724;
        margin: 1rem 0;
    }
    .error-message {
        padding: 1rem;
        border-radius: 5px;
        background-color: #f8d7da;
        color: #721c24;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Load environment variables
load_dotenv()
 
 
# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/150", width=150)
    st.title("AI Agent Marketplace")
    st.markdown("---")
    
    
    st.markdown("---")
    st.markdown("### About")
    st.info("""
    This marketplace allows you to:
    - Post bounties for AI agents
    - Submit your AI agents
    - Win rewards in FTN tokens
    """)

def main():
    st.title("🤖 AI Agent Bounty Platform")
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 Post Bounty", "🏆 Leaderboard", "🤖 Submit Agent", "📊 Analytics", "🌟 Featured Bounties"])
    
    with tab1:
        show_post_bounty()
    with tab2:
        show_leaderboard()
    with tab3:
        show_submit_agent()
    with tab4:
        show_analytics()
    with tab5:
        show_featured_bounties()

def show_post_bounty():
    st.header("Post a New Bounty")
    
    # Define models and their base rewards (in FTN)
    models = {
        "Microsoft Phi-3-mini (3.8B)": 100,
        "Microsoft Phi-3-small (7B)": 80,
        "Google Gemma 2B": 120,
        "Google Gemma 7B": 70,
        "Mistral 7B": 70,
        "StableLM 2B": 120,
        "StableLM 3B": 100,
        "Qwen 0.5B": 150,
        "Qwen 1.5B": 130,
        "Qwen 4B": 90,
        "Qwen 7B": 70,
    }
    
    with st.form("bounty_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Bounty Title", placeholder="e.g., Document Classifier Agent")
            description = st.text_area("Description", height=150, placeholder="Describe the task your agent should solve, e.g., 'Classify documents by topic with at least 80% accuracy.'")
            
            # Model selection with dynamic reward
            selected_model = st.selectbox(
                "Select Base Model",
                options=list(models.keys()),
                format_func=lambda x: f"{x} (Reward: {models[x]} FTN)"
            )
            
            # Display the reward amount (read-only)
            st.number_input(
                "Reward Amount (FTN)",
                value=models[selected_model],
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
                # Simulate IPFS upload and get CID
                test_cid = "Qm" + hashlib.sha256(test_file.getvalue()).hexdigest()[:40]
                st.success(f"Test suite uploaded! CID: {test_cid}")
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
            if not test_cid:
                st.error("Please upload a test suite or provide a valid CID")
                return
                
            try:
                # Simulate blockchain transaction
                tx_hash = "0x" + hashlib.sha256(str(datetime.now()).encode()).hexdigest()[:40]
                st.success(f"Bounty posted successfully! Transaction hash: {tx_hash}")
                st.info(f"""
                The bounty is now escrowed on Bahamut testnet:
                - Base Model: {selected_model}
                - Reward: {models[selected_model]} FTN
                - Test Suite CID: {test_cid}
                - Anyone can view the criteria and prize amount on-chain.
                """)
            except Exception as e:
                st.error(f"Error posting bounty: {str(e)}")

def show_leaderboard():
    st.header("🏆 Bounty Leaderboard")
    
    # Refresh button
    if st.button("🔄 Refresh"):
        st.info("Refreshing leaderboard data...")
    
    # Sample bounty data
    bounties = [
        {
            "id": 1,
            "title": "Document Classifier Agent",
            "reward": "1 FTN",
            "model_hash": "0x1234...5678",
            "test_cid": "QmTest123...",
            "status": "Active",
            "submissions": 3
        }
    ]
    
    for bounty in bounties:
        with st.expander(f"{bounty['title']} - {bounty['reward']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Model Hash:** {bounty['model_hash']}")
                st.write(f"**Test CID:** {bounty['test_cid']}")
            with col2:
                st.write(f"**Status:** {bounty['status']}")
                st.write(f"**Submissions:** {bounty['submissions']}")
            
            if st.button("View Details", key=f"view_{bounty['id']}"):
                st.info("Agent builders now have access to the requirements and the allowed base model. All test cases are open, fair, and reproducible.")

def show_submit_agent():
    st.header("Submit Your Agent")
    
    # Colab Integration (Outside the form)
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
        # Select bounty
        bounty_id = st.selectbox(
            "Select Bounty",
            options=[(1, "Document Classifier Agent - 1 FTN")],
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
            requirements = st.text_area(
                "Additional Requirements",
                height=100,
                help="List any additional Python packages your agent needs (beyond the base requirements)."
            )
            
        with col2:
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
            if not agent_code:
                st.error("Please provide your agent code")
                return
                
            try:
                # Simulate submission
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
                - Code Length: {len(agent_code)} characters
                - Additional Requirements: {len(requirements.split()) if requirements else 0} packages
                - Documentation: {len(readme)} characters
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

def show_analytics():
    st.header("📊 Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            label="Total Bounties",
            value="12",
            delta="3 new this week"
        )
        
        st.metric(
            label="Total Rewards",
            value="1,500 FTN",
            delta="500 FTN this week"
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
    
    # Sample chart data
    chart_data = {
        'Date': pd.date_range(start='2024-03-01', periods=15, freq='D'),
        'Bounties': [1, 2, 3, 2, 4, 3, 5, 4, 6, 5, 7, 6, 8, 7, 9],
        'Rewards': [100, 200, 300, 200, 400, 300, 500, 400, 600, 500, 700, 600, 800, 700, 900]
    }
    
    st.line_chart(pd.DataFrame(chart_data).set_index('Date'))

def show_featured_bounties():
    st.header("🌟 Featured Bounties")
    st.markdown("""
    Discover exciting opportunities at the intersection of AI and blockchain technology.
    These featured bounties focus on innovative use cases and infrastructure development.
    """)
    
    # Featured bounty categories
    categories = {
        "⚖️ Legal AI": {
            "color": "#9B59B6",
            "bounties": [
                {
                    "title": "Bankruptcy Case Evidence Analyzer",
                    "reward": "700 FTN",
                    "description": "Develop an AI agent that analyzes bankruptcy case documents to identify relevant evidence and generate supporting arguments.",
                    "requirements": [
                        "Document analysis and classification",
                        "Evidence extraction and validation",
                        "Argument generation framework",
                        "Legal precedent matching",
                        "Case law integration"
                    ],
                    "model": "Google Gemma 7B",
                    "deadline": "90 days"
                },
                {
                    "title": "Bankruptcy Risk Assessment Tool",
                    "reward": "550 FTN",
                    "description": "Create an AI agent that evaluates bankruptcy risk by analyzing financial documents and market conditions.",
                    "requirements": [
                        "Financial document parsing",
                        "Risk factor identification",
                        "Market trend analysis",
                        "Risk scoring system",
                        "Regulatory compliance checks"
                    ],
                    "model": "Mistral 7B",
                    "deadline": "60 days"
                },
                {
                    "title": "Legal Document Generation System",
                    "reward": "450 FTN",
                    "description": "Build an AI agent that generates legal documents for bankruptcy proceedings with proper formatting and compliance.",
                    "requirements": [
                        "Document template system",
                        "Legal terminology database",
                        "Compliance verification",
                        "Multi-format export",
                        "Version control integration"
                    ],
                    "model": "Microsoft Phi-3-small (7B)",
                    "deadline": "45 days"
                }
            ]
        },
        "🔍 Blockchain Analytics": {
            "color": "#FF6B6B",
            "bounties": [
                {
                    "title": "AI-Powered Blockchain Fraud Detection",
                    "reward": "500 FTN",
                    "description": "Develop an AI agent that can detect suspicious patterns and potential fraud in blockchain transactions.",
                    "requirements": [
                        "Real-time transaction analysis",
                        "Pattern recognition for common fraud types",
                        "Low false positive rate",
                        "Integration with major blockchains"
                    ],
                    "model": "Mistral 7B",
                    "deadline": "30 days"
                },
                {
                    "title": "Smart Contract Vulnerability Scanner",
                    "reward": "400 FTN",
                    "description": "Create an AI agent that can analyze smart contracts for potential vulnerabilities and security risks.",
                    "requirements": [
                        "Static code analysis",
                        "Common vulnerability detection",
                        "Gas optimization suggestions",
                        "Integration with popular development environments"
                    ],
                    "model": "Microsoft Phi-3-small (7B)",
                    "deadline": "45 days"
                }
            ]
        },
        "🔄 Web2-Web3 Bridge": {
            "color": "#4ECDC4",
            "bounties": [
                {
                    "title": "AI-Powered Web2 to Web3 Migration Assistant",
                    "reward": "600 FTN",
                    "description": "Build an AI agent that helps traditional web applications migrate to Web3 infrastructure.",
                    "requirements": [
                        "Code analysis and transformation",
                        "Smart contract generation",
                        "Migration planning and optimization",
                        "Integration testing framework"
                    ],
                    "model": "Google Gemma 7B",
                    "deadline": "60 days"
                },
                {
                    "title": "Decentralized AI Model Marketplace",
                    "reward": "450 FTN",
                    "description": "Develop an AI agent that facilitates the secure and fair trading of AI models on the blockchain.",
                    "requirements": [
                        "Model verification system",
                        "Fair pricing mechanism",
                        "Secure model transfer",
                        "Usage tracking and royalties"
                    ],
                    "model": "Qwen 7B",
                    "deadline": "40 days"
                }
            ]
        },
        "🤖 AI Infrastructure": {
            "color": "#45B7D1",
            "bounties": [
                {
                    "title": "Decentralized AI Training Orchestrator",
                    "reward": "550 FTN",
                    "description": "Create an AI agent that coordinates distributed AI training across multiple nodes.",
                    "requirements": [
                        "Task distribution algorithm",
                        "Progress tracking",
                        "Fault tolerance",
                        "Resource optimization"
                    ],
                    "model": "StableLM 3B",
                    "deadline": "50 days"
                },
                {
                    "title": "Blockchain-Based AI Model Version Control",
                    "reward": "350 FTN",
                    "description": "Build an AI agent that manages version control and provenance tracking for AI models on the blockchain.",
                    "requirements": [
                        "Version tracking system",
                        "Provenance verification",
                        "Model comparison tools",
                        "Rollback capabilities"
                    ],
                    "model": "Microsoft Phi-3-mini (3.8B)",
                    "deadline": "35 days"
                }
            ]
        }
    }
    
    # Add category filter
    st.markdown("### Filter Bounties")
    selected_categories = st.multiselect(
        "Select Categories",
        options=list(categories.keys()),
        default=list(categories.keys())
    )
    
    # Display categories and their bounties
    for category, data in categories.items():
        if category in selected_categories:
            st.markdown(f"### {category}")
            
            for bounty in data["bounties"]:
                with st.container():
                    st.markdown(f"""
                    <div style='padding: 20px; border-radius: 10px; background-color: {data['color']}20; border: 1px solid {data['color']}40;'>
                        <h3 style='color: {data['color']}; margin-bottom: 10px;'>{bounty['title']}</h3>
                        <p style='color: #666;'>{bounty['description']}</p>
                        <div style='display: flex; justify-content: space-between; margin: 10px 0;'>
                            <span>💰 Reward: {bounty['reward']}</span>
                            <span>🤖 Model: {bounty['model']}</span>
                            <span>⏰ Deadline: {bounty['deadline']}</span>
                        </div>
                        <div style='margin-top: 10px;'>
                            <strong>Requirements:</strong>
                            <ul style='margin-top: 5px;'>
                                {''.join(f'<li>{req}</li>' for req in bounty['requirements'])}
                            </ul>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        if st.button("View Details", key=f"view_{bounty['title']}"):
                            st.info("""
                            This bounty is part of our Featured Bounties program, which focuses on:
                            - Innovative use cases
                            - Infrastructure development
                            - Cross-chain compatibility
                            - Security and scalability
                            """)
                    with col2:
                        if st.button("Apply Now", key=f"apply_{bounty['title']}"):
                            st.success("Redirecting to submission form...")
                            # In a real implementation, this would switch to the Submit Agent tab
                            # with the bounty pre-selected
                    
                    st.markdown("---")
    
    # Additional information
    with st.expander("ℹ️ About Featured Bounties"):
        st.markdown("""
        ### What are Featured Bounties?
        
        Featured Bounties are special opportunities that focus on:
        
        1. **Innovation**
           - Novel use cases
           - Emerging technologies
           - Cross-domain solutions
        
        2. **Infrastructure**
           - Core blockchain components
           - AI infrastructure
           - Integration tools
        
        3. **Impact**
           - High-value applications
           - Community benefits
           - Long-term potential
        
        ### Benefits
        
        - Higher rewards
        - Priority evaluation
        - Community recognition
        - Potential for long-term collaboration
        
        ### How to Participate
        
        1. Review the requirements
        2. Choose your preferred bounty
        3. Submit your solution
        4. Get evaluated by our expert panel
        """)

if __name__ == "__main__":
    main()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Built on Bahamut blockchain for AI + On-chain Logic competition</p>
    <p>© 2024 AI Agent Marketplace. All rights reserved.</p>
</div>
""", unsafe_allow_html=True) 