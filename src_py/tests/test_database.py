import unittest
from datetime import datetime, timedelta
from src_py.database.database import init_db, get_db
from src_py.database.repository import (
    BountyRepository,
    SubmissionRepository,
    WinnerRepository,
    OracleRepository
)

class TestDatabase(unittest.TestCase):
    def setUp(self):
        """Set up test database"""
        # Initialize database with test tables
        init_db()
        
        # Test data
        self.test_sponsor = "0x1234567890123456789012345678901234567890"
        self.test_agent = "0x0987654321098765432109876543210987654321"
        self.test_oracle = "0x1111111111111111111111111111111111111111"
        self.test_reward = 1.5
        self.test_deadline = int((datetime.utcnow() + timedelta(days=1)).timestamp())

    def test_bounty_creation(self):
        """Test bounty creation and retrieval"""
        # Create a bounty
        bounty = BountyRepository.create(
            sponsor_address=self.test_sponsor,
            reward=self.test_reward,
            deadline=self.test_deadline
        )
        
        # Verify bounty was created
        self.assertIsNotNone(bounty.id)
        self.assertEqual(bounty.sponsor_address, self.test_sponsor)
        self.assertEqual(float(bounty.reward), self.test_reward)
        self.assertEqual(bounty.deadline, self.test_deadline)
        self.assertFalse(bounty.paid_out)

    def test_submission_creation(self):
        """Test submission creation and retrieval"""
        # Create a bounty first
        bounty = BountyRepository.create(
            sponsor_address=self.test_sponsor,
            reward=self.test_reward,
            deadline=self.test_deadline
        )
        
        # Create a submission
        submission = SubmissionRepository.create(
            bounty_id=bounty.id,
            agent_address=self.test_agent
        )
        
        # Verify submission was created
        self.assertIsNotNone(submission.id)
        self.assertEqual(submission.bounty_id, bounty.id)
        self.assertEqual(submission.agent_address, self.test_agent)
        
        # Get submissions for bounty
        submissions = SubmissionRepository.get_by_bounty(bounty.id)
        self.assertEqual(len(submissions), 1)
        self.assertEqual(submissions[0].agent_address, self.test_agent)

    def test_winner_creation(self):
        """Test winner creation and retrieval"""
        # Create a bounty first
        bounty = BountyRepository.create(
            sponsor_address=self.test_sponsor,
            reward=self.test_reward,
            deadline=self.test_deadline
        )
        
        # Create a winner
        winner = WinnerRepository.create(
            bounty_id=bounty.id,
            winner_address=self.test_agent,
            payout_amount=self.test_reward
        )
        
        # Verify winner was created
        self.assertIsNotNone(winner.id)
        self.assertEqual(winner.bounty_id, bounty.id)
        self.assertEqual(winner.winner_address, self.test_agent)
        self.assertEqual(float(winner.payout_amount), self.test_reward)
        
        # Get winners for bounty
        winners = WinnerRepository.get_by_bounty(bounty.id)
        self.assertEqual(len(winners), 1)
        self.assertEqual(winners[0].winner_address, self.test_agent)

    def test_oracle_creation(self):
        """Test oracle creation and retrieval"""
        # Create an oracle
        oracle = OracleRepository.create(
            oracle_address=self.test_oracle
        )
        
        # Verify oracle was created
        self.assertIsNotNone(oracle.id)
        self.assertEqual(oracle.oracle_address, self.test_oracle)
        self.assertTrue(oracle.is_active)
        
        # Get oracle by address
        retrieved_oracle = OracleRepository.get_by_address(self.test_oracle)
        self.assertIsNotNone(retrieved_oracle)
        self.assertEqual(retrieved_oracle.oracle_address, self.test_oracle)

    def test_active_bounties(self):
        """Test retrieval of active bounties"""
        # Create an active bounty
        active_bounty = BountyRepository.create(
            sponsor_address=self.test_sponsor,
            reward=self.test_reward,
            deadline=self.test_deadline
        )
        
        # Create an expired bounty
        expired_deadline = int((datetime.utcnow() - timedelta(days=1)).timestamp())
        expired_bounty = BountyRepository.create(
            sponsor_address=self.test_sponsor,
            reward=self.test_reward,
            deadline=expired_deadline
        )
        
        # Get active bounties
        active_bounties = BountyRepository.get_active()
        
        # Verify only active bounty is returned
        self.assertEqual(len(active_bounties), 1)
        self.assertEqual(active_bounties[0].id, active_bounty.id)

if __name__ == '__main__':
    unittest.main() 