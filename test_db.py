from src_py.database.database import get_db, init_db
from src_py.database.models import Bounty, Submission
from datetime import datetime, timedelta

# Initialize the database
init_db()

def test_database():
    try:
        # Initialize the database
        init_db()

        with get_db() as db:
            # Demo sponsors (posters)
            sponsors = [
                "0xPoster1aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "0xPoster2bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
                "0xPoster3cccccccccccccccccccccccccccccccccccccc"
            ]

            # Create 3 bounties, one for each sponsor
            bounties = []
            for i, sponsor in enumerate(sponsors):
                bounty = Bounty(
                    sponsor_address=sponsor,
                    reward=10.0 + i,
                    deadline=int((datetime.utcnow() + timedelta(days=7)).timestamp())
                )
                db.add(bounty)
                db.flush()
                bounties.append(bounty)
                print(f"Created bounty {bounty.id} for sponsor {sponsor}")

            # AI builders (agents) for each bounty
            agents = [
                [f"0xAgentA{i+1}{'a'*36}" for i in range(2)],   # 2 agents for bounty 1
                [f"0xAgentB{i+1}{'b'*36}" for i in range(4)],   # 4 agents for bounty 2
                [f"0xAgentC{i+1}{'c'*36}" for i in range(5)]    # 5 agents for bounty 3
            ]

            # Create submissions for each bounty
            for bounty, agent_list in zip(bounties, agents):
                for agent in agent_list:
                    submission = Submission(
                        bounty_id=bounty.id,
                        agent_address=agent
                    )
                    db.add(submission)
                    db.flush()
                    print(f"Agent {agent} submitted to bounty {bounty.id}")

            print("Demo data created: 3 posters, 3 bounties, and 2/4/5 AI builders with submissions.")

            # Print all bounties and their submissions
            print("\nBounties and their submissions:")
            all_bounties = db.query(Bounty).all()
            for bounty in all_bounties:
                print(f"Bounty ID: {bounty.id}, Sponsor: {bounty.sponsor_address}, Reward: {bounty.reward}, Deadline: {bounty.deadline}")
                submissions = db.query(Submission).filter(Submission.bounty_id == bounty.id).all()
                for submission in submissions:
                    print(f"  Submission ID: {submission.id}, Agent: {submission.agent_address}")
            print("--- End of bounties ---\n")
        return True
    except Exception as e:
        print(f"Database connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_database() 