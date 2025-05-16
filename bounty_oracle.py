import asyncio
import json
import os
from datetime import datetime
from web3 import Web3
from dotenv import load_dotenv
import ipfshttpclient
import pytest
import pandas as pd
from pathlib import Path

# Load environment variables
load_dotenv()

# Initialize Web3 and IPFS
w3 = Web3(Web3.HTTPProvider(os.getenv('BAHAMUT_RPC_URL')))
ipfs_client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')

# Load contract ABI and address
with open('artifacts/contracts/EscrowContract.sol/EscrowContract.json') as f:
    contract_json = json.load(f)
    contract_abi = contract_json['abi']

CONTRACT_ADDRESS = os.getenv('ESCROW_CONTRACT_ADDRESS')
escrow_contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)

class BountyOracle:
    def __init__(self):
        self.active_bounties = {}
        self.submissions = {}
        self.test_results = {}
        
    async def process_bounty(self, bounty_id):
        """Process a single bounty after its deadline"""
        bounty = await self.get_bounty_details(bounty_id)
        if not bounty['isActive']:
            return
            
        # Get all submissions for this bounty
        submissions = await self.get_submissions(bounty_id)
        
        # Score each submission
        scores = []
        for submission in submissions:
            score = await self.evaluate_submission(submission)
            scores.append({
                'address': submission['submitter'],
                'score': score,
                'agent_cid': submission['agentCID']
            })
            
        # Sort by score and determine winners
        scores.sort(key=lambda x: x['score'], reverse=True)
        winners = [s for s in scores if s['score'] >= 80]  # 80% threshold
        
        if winners:
            # Calculate reward share
            reward_share = bounty['amount'] // len(winners)
            
            # Process payouts
            for winner in winners:
                await self.process_payout(
                    bounty_id,
                    winner['address'],
                    winner['agent_cid'],
                    winner['score'],
                    reward_share
                )
                
    async def evaluate_submission(self, submission):
        """Evaluate a single submission"""
        try:
            # Download agent code from IPFS
            agent_code = await self.download_from_ipfs(submission['agentCID'])
            
            # Run test suite
            test_results = await self.run_tests(agent_code)
            
            # Calculate final score
            score = self.calculate_score(test_results)
            
            return score
            
        except Exception as e:
            print(f"Error evaluating submission: {e}")
            return 0
            
    async def run_tests(self, agent_code):
        """Run the test suite on the agent code"""
        # Save agent code to temporary file
        with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as f:
            f.write(agent_code.encode())
            temp_path = f.name
            
        try:
            # Run pytest
            result = pytest.main([temp_path, '-v'])
            
            # Parse test results
            return {
                'passed': result == 0,
                'test_count': 1,  # In real implementation, parse actual test count
                'coverage': 100   # In real implementation, calculate actual coverage
            }
        finally:
            os.unlink(temp_path)
            
    def calculate_score(self, test_results):
        """Calculate final score based on test results"""
        if not test_results['passed']:
            return 0
            
        # Weight different factors
        weights = {
            'test_pass': 0.6,
            'coverage': 0.4
        }
        
        score = (
            weights['test_pass'] * 100 +
            weights['coverage'] * test_results['coverage']
        )
        
        return min(score, 100)  # Cap at 100
        
    async def process_payout(self, bounty_id, winner, agent_cid, score, amount):
        """Process the payout to a winner"""
        try:
            # Call contract to release reward
            tx = escrow_contract.functions.releaseReward(
                bounty_id,
                winner,
                agent_cid,
                score
            ).build_transaction({
                'from': os.getenv('ORACLE_ADDRESS'),
                'gas': 200000,
                'gasPrice': w3.eth.gas_price,
                'nonce': w3.eth.get_transaction_count(os.getenv('ORACLE_ADDRESS'))
            })
            
            # Sign and send transaction
            signed_tx = w3.eth.account.sign_transaction(tx, os.getenv('ORACLE_PRIVATE_KEY'))
            tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            
            # Wait for transaction receipt
            receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
            
            print(f"Payout processed: {amount} FTN to {winner}")
            return receipt
            
        except Exception as e:
            print(f"Error processing payout: {e}")
            return None

async def main():
    oracle = BountyOracle()
    
    # Event filters
    bounty_posted_filter = escrow_contract.events.BountyPosted.create_filter(fromBlock='latest')
    agent_submitted_filter = escrow_contract.events.AgentSubmitted.create_filter(fromBlock='latest')
    
    print("Oracle started. Listening for events...")
    
    while True:
        try:
            # Check for new bounties
            bounty_events = bounty_posted_filter.get_new_entries()
            for event in bounty_events:
                print(f"New bounty posted: {event['args']['bountyId']}")
                
            # Check for new submissions
            submission_events = agent_submitted_filter.get_new_entries()
            for event in submission_events:
                print(f"New submission for bounty {event['args']['bountyId']}")
                
            # Process any bounties that have passed their deadline
            current_time = datetime.now().timestamp()
            for bounty_id in oracle.active_bounties:
                if oracle.active_bounties[bounty_id]['deadline'] <= current_time:
                    await oracle.process_bounty(bounty_id)
                    
            await asyncio.sleep(60)  # Check every minute
            
        except Exception as e:
            print(f"Error in main loop: {e}")
            await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main()) 