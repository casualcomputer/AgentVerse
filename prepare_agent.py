import os
import shutil
import sys
import argparse

def prepare_agent_for_submission(agent_id, target_dir="./test_agents"):
    """
    Prepares the HotpotQA agent for submission to the marketplace.
    This function:
    1. Creates a directory with the agent_id as name
    2. Copies the required files into it
    3. Creates a README with usage instructions
    
    Args:
        agent_id (str): Identifier for the agent, used as directory name
        target_dir (str): Base directory where agent will be saved
    
    Returns:
        str: Path to the prepared agent directory
    """
    # Create agent directory
    agent_dir = os.path.join(target_dir, agent_id)
    if os.path.exists(agent_dir):
        print(f"Warning: Directory {agent_dir} already exists. Files may be overwritten.")
    else:
        os.makedirs(agent_dir, exist_ok=True)
    
    # Create tests directory
    tests_dir = os.path.join(agent_dir, "tests")
    os.makedirs(tests_dir, exist_ok=True)
    
    # Copy agent.py
    shutil.copy("agent.py", agent_dir)
    
    # Copy tests/test_agent.py
    shutil.copy("tests/test_agent.py", tests_dir)
    
    # Copy data directory
    data_dir = os.path.join(agent_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    shutil.copy("data/hotpotqa_sample.json", data_dir)
    
    # Create requirements.txt
    shutil.copy("requirements.txt", agent_dir)
    
    # Create README.md
    readme_content = f"""# HotpotQA ReAct Agent

An AI agent that uses the ReAct (Reasoning + Acting) approach to answer multi-hop questions from the HotpotQA dataset.

## Features

- Breaks down complex questions into logical steps
- Uses web search to gather relevant information
- Combines information to provide comprehensive answers
- Supports both OpenAI API and local LLMs

## Setup

1. Install dependencies:
```
pip install -r requirements.txt
```

2. Set up environment variables (create a .env file):
```
OPENAI_API_KEY=your_api_key_here  # Optional, falls back to local model if not provided
```

3. Running the agent:
```
python agent.py
```

## Testing

Run tests:
```
pytest tests/
```

## Sample Questions

The agent comes pre-loaded with sample questions from the HotpotQA dataset, located in the `data/` directory.

## Model Information
- Name: {os.environ.get('MODEL_NAME', 'gpt-3.5-turbo')}
- Type: ReAct Agent
- Capabilities: Multi-hop reasoning, web search
"""
    
    with open(os.path.join(agent_dir, "README.md"), "w") as f:
        f.write(readme_content)
    
    print(f"Agent prepared for submission at: {agent_dir}")
    print("To submit this agent to the marketplace:")
    print(f"1. Set AGENT_CID={agent_id} in your environment or .env file")
    print("2. Run: node scripts/submit_agent.js")
    
    return agent_dir

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Prepare HotpotQA agent for submission')
    parser.add_argument('--agent-id', type=str, default='hotpotqa_agent_v1', 
                        help='Identifier for the agent, used as directory name')
    parser.add_argument('--target-dir', type=str, default='./test_agents',
                        help='Base directory where agent will be saved')
    
    args = parser.parse_args()
    
    prepare_agent_for_submission(args.agent_id, args.target_dir) 