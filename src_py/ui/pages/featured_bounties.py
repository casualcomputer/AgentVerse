"""
Featured Bounties page for the AgentVerse platform.
"""
import streamlit as st

def render_page():
    """Render the featured bounties page"""
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
                            st.success("Bounty selected! Navigate to the 'Submit Agent' tab to continue.")
                    
                    st.markdown("---") 