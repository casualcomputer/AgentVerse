"""
Blockchain service for interacting with the Bahamut blockchain.
"""
import hashlib
import subprocess
import os
from datetime import datetime

class BlockchainService:
    """Service for interacting with blockchain contracts and transactions via Node.js scripts"""
    
    def __init__(self):
        """Initialize blockchain connection"""
        self.contract_address = os.getenv("ESCROW_CONTRACT_ADDRESS", "0xeA141c8B753Cc244745603412Ae731CB078Bac9d")
        self.node_path = os.getenv("NODE_PATH", "node")
        self.scripts_dir = os.getenv("SCRIPTS_DIR", "scripts")
    
    def get_events(self, event_name):
        """
        Get events from the blockchain by name
        
        Args:
            event_name (str): Name of the event to query
            
        Returns:
            list: List of event objects
        """
        # TODO: Implement event fetching from the blockchain if needed
        return []
    
    def get_submissions(self, bounty_id):
        """
        Get submissions for a bounty
        
        Args:
            bounty_id (int): ID of the bounty
            
        Returns:
            list: List of submission objects
        """
        # TODO: Implement fetching submissions from the blockchain if needed
        return []
    
    def post_bounty(self, description):
        script = os.path.join(self.scripts_dir, "postBounty.js")
        result = subprocess.run([
            self.node_path, script, self.contract_address, description
        ], capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Error posting bounty: {result.stderr}")
        return {"tx_hash": self._extract_tx_hash(result.stdout)}
    
    def submit_agent(self, bounty_id):
        script = os.path.join(self.scripts_dir, "submitAgent.js")
        result = subprocess.run([
            self.node_path, script, self.contract_address, str(bounty_id)
        ], capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Error submitting agent: {result.stderr}")
        return {"tx_hash": self._extract_tx_hash(result.stdout)}
    
    def batch_payout(self, bounty_id, winners):
        script = os.path.join(self.scripts_dir, "batchPayout.js")
        winners_arg = ",".join(winners)
        result = subprocess.run([
            self.node_path, script, self.contract_address, str(bounty_id), winners_arg
        ], capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Error in batch payout: {result.stderr}")
        return {"tx_hash": self._extract_tx_hash(result.stdout)}
    
    def _extract_tx_hash(self, output):
        for line in output.splitlines():
            if "Tx hash:" in line:
                return line.split("Tx hash:")[-1].strip()
        return None
    
    def submit_agent(self, bounty_id, agent_cid, code_hash):
        """
        Submit an agent to a bounty
        
        Args:
            bounty_id (int): ID of the bounty
            agent_cid (str): IPFS CID of the agent code
            code_hash (str): Hash of the agent code for verification
            
        Returns:
            dict: Transaction receipt
        """
        # Mock implementation for demo
        tx_hash = "0x" + hashlib.sha256(str(datetime.now()).encode()).hexdigest()[:40]
        return {
            'tx_hash': tx_hash,
            'status': 'success',
            'block_number': 12345678
        }
    
    def post_bounty(self, description, reward, test_cid):
        """
        Post a new bounty
        
        Args:
            description (str): Description of the bounty
            reward (int): Reward amount in FTN
            test_cid (str): IPFS CID of test suite
            
        Returns:
            dict: Transaction receipt
        """
        # Mock implementation for demo
        tx_hash = "0x" + hashlib.sha256(str(datetime.now()).encode()).hexdigest()[:40]
        return {
            'tx_hash': tx_hash,
            'status': 'success',
            'block_number': 12345678,
            'bounty_id': len(self.get_events('BountyPosted')) + 1
        } 