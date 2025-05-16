"""
Bounty data model for the AgentVerse platform.
"""
from datetime import datetime
from typing import List, Optional

class Bounty:
    """
    Represents a bounty in the marketplace
    """
    
    def __init__(
        self,
        id: int,
        title: str,
        description: str,
        model: str,
        reward: int,
        test_cid: str,
        poster: str,
        tx_hash: str,
        posted_date: Optional[datetime] = None
    ):
        """
        Initialize a bounty
        
        Args:
            id (int): Unique identifier
            title (str): Title of the bounty
            description (str): Detailed description
            model (str): Required base model
            reward (int): Reward amount in FTN
            test_cid (str): IPFS CID of test suite
            poster (str): Address of poster
            tx_hash (str): Transaction hash
            posted_date (datetime, optional): Date posted
        """
        self.id = id
        self.title = title
        self.description = description
        self.model = model
        self.reward = reward
        self.test_cid = test_cid
        self.poster = poster
        self.tx_hash = tx_hash
        self.posted_date = posted_date or datetime.now()
        self.submissions = 0
        
    def to_dict(self) -> dict:
        """
        Convert to dictionary
        
        Returns:
            dict: Dictionary representation
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'model': self.model,
            'reward': self.reward,
            'test_cid': self.test_cid,
            'poster': self.poster,
            'tx_hash': self.tx_hash,
            'posted_date': self.posted_date,
            'submissions': self.submissions
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Bounty':
        """
        Create from dictionary
        
        Args:
            data (dict): Dictionary data
            
        Returns:
            Bounty: New bounty instance
        """
        return cls(
            id=data.get('id'),
            title=data.get('title'),
            description=data.get('description'),
            model=data.get('model'),
            reward=data.get('reward'),
            test_cid=data.get('test_cid'),
            poster=data.get('poster'),
            tx_hash=data.get('tx_hash'),
            posted_date=data.get('posted_date')
        ) 