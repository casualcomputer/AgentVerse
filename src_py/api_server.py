from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from src_py.database.database import get_db, init_db
from src_py.database.models import Bounty, Submission, TestResult, Payout
from datetime import datetime

app = FastAPI()

# Initialize DB tables
init_db()

# Pydantic models for request/response
class BountyCreate(BaseModel):
    sponsor_address: str
    reward: float
    deadline: int

class SubmissionCreate(BaseModel):
    bounty_id: int
    agent_address: str

class LeaderboardEntry(BaseModel):
    agent_address: str
    total_score: float

@app.post("/bounties")
def post_bounty(bounty: BountyCreate):
    with get_db() as db:
        new_bounty = Bounty(
            sponsor_address=bounty.sponsor_address,
            reward=bounty.reward,
            deadline=bounty.deadline
        )
        db.add(new_bounty)
        db.flush()
        return {"id": new_bounty.id}

@app.get("/bounties", response_model=List[BountyCreate])
def get_bounties():
    with get_db() as db:
        bounties = db.query(Bounty).all()
        return [BountyCreate(
            sponsor_address=b.sponsor_address,
            reward=float(b.reward),
            deadline=b.deadline
        ) for b in bounties]

@app.post("/submissions")
def submit_agent(submission: SubmissionCreate):
    with get_db() as db:
        new_submission = Submission(
            bounty_id=submission.bounty_id,
            agent_address=submission.agent_address,
            submitted_at=datetime.utcnow()
        )
        db.add(new_submission)
        db.flush()
        return {"id": new_submission.id}

@app.get("/submissions/{bounty_id}")
def get_submissions(bounty_id: int):
    with get_db() as db:
        submissions = db.query(Submission).filter(Submission.bounty_id == bounty_id).all()
        return [{
            "id": s.id,
            "agent_address": s.agent_address,
            "submitted_at": s.submitted_at
        } for s in submissions]

@app.get("/leaderboard", response_model=List[LeaderboardEntry])
def get_leaderboard():
    with get_db() as db:
        # Aggregate total score per agent
        results = db.query(Submission.agent_address, TestResult.score).join(TestResult, Submission.id == TestResult.submission_id).all()
        leaderboard = {}
        for agent_address, score in results:
            leaderboard[agent_address] = leaderboard.get(agent_address, 0) + float(score)
        return [LeaderboardEntry(agent_address=a, total_score=s) for a, s in leaderboard.items()] 