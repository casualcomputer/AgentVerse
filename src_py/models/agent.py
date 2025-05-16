"""
Agent data model for the AgentVerse platform.
"""
from datetime import datetime
from typing import Dict, Optional

class Agent:
    """
    Represents an AI agent in the marketplace
    """
    
    def __init__(
        self,
        id: int,
        name: str,
        description: str,
        model: str,
        agent_cid: str,
        code_hash: str,
        submitter: str,
        bounty_id: Optional[int] = None,
        tx_hash: Optional[str] = None,
        submitted_date: Optional[datetime] = None,
        metrics: Optional[Dict] = None
    ):
        """
        Initialize an agent
        
        Args:
            id (int): Unique identifier
            name (str): Name of the agent
            description (str): Detailed description
            model (str): Base model used
            agent_cid (str): IPFS CID of agent code
            code_hash (str): Hash of the agent code
            submitter (str): Address of submitter
            bounty_id (int, optional): Associated bounty ID
            tx_hash (str, optional): Transaction hash
            submitted_date (datetime, optional): Date submitted
            metrics (Dict, optional): Performance metrics
        """
        self.id = id
        self.name = name
        self.description = description
        self.model = model
        self.agent_cid = agent_cid
        self.code_hash = code_hash
        self.submitter = submitter
        self.bounty_id = bounty_id
        self.tx_hash = tx_hash
        self.submitted_date = submitted_date or datetime.now()
        self.metrics = metrics or {
            'accuracy': 0,
            'inference_speed': 0,
            'memory_usage': 0
        }
        
    def to_dict(self) -> dict:
        """
        Convert to dictionary
        
        Returns:
            dict: Dictionary representation
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'model': self.model,
            'agent_cid': self.agent_cid,
            'code_hash': self.code_hash,
            'submitter': self.submitter,
            'bounty_id': self.bounty_id,
            'tx_hash': self.tx_hash,
            'submitted_date': self.submitted_date,
            'metrics': self.metrics
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Agent':
        """
        Create from dictionary
        
        Args:
            data (dict): Dictionary data
            
        Returns:
            Agent: New agent instance
        """
        return cls(
            id=data.get('id'),
            name=data.get('name'),
            description=data.get('description'),
            model=data.get('model'),
            agent_cid=data.get('agent_cid'),
            code_hash=data.get('code_hash'),
            submitter=data.get('submitter'),
            bounty_id=data.get('bounty_id'),
            tx_hash=data.get('tx_hash'),
            submitted_date=data.get('submitted_date'),
            metrics=data.get('metrics')
        ) 