from datetime import datetime
from src_py.database.database import get_db, init_db
from src_py.database.models import Bounty, Submission, TestResult, Payout
import time 

def evaluate_submission(submission):
    # Dummy scoring: random or fixed for demo
    # In real use, run actual evaluation logic
    score = 100.0  # All pass for demo
    passed = True
    return score, passed

def process_expired_bounties(request=None):
    now = int(datetime.utcnow().timestamp())
    with get_db() as db:
        expired_bounties = db.query(Bounty).filter(Bounty.deadline <= now, Bounty.paid_out == False).all()
        for bounty in expired_bounties:
            print(f"Processing bounty {bounty.id}...")
            submissions = db.query(Submission).filter(Submission.bounty_id == bounty.id).all()
            winners = []
            for submission in submissions:
                score, passed = evaluate_submission(submission)
                # Write test result
                test_result = TestResult(
                    submission_id=submission.id,
                    score=score,
                    passed=passed,
                    evaluated_at=datetime.utcnow()
                )
                db.add(test_result)
                if passed:
                    winners.append(submission.agent_address)
            # Payout logic: split reward equally among winners
            if winners:
                share = float(bounty.reward) / len(winners)
                for winner in winners:
                    payout = Payout(
                        bounty_id=bounty.id,
                        winner_address=winner,
                        share=share,
                        tx_hash="0xDEMOHASH",
                        paid_at=datetime.utcnow()
                    )
                    db.add(payout)
            bounty.paid_out = True
            print(f"Bounty {bounty.id} processed. Winners: {winners}")
        db.commit()
    return "Processed expired bounties", 200

def run_oracle():
    print("Oracle service started. Polling for expired bounties...")
    while True:
        process_expired_bounties()
        time.sleep(60)  # Poll every 60 seconds

if __name__ == "__main__":
    run_oracle() 