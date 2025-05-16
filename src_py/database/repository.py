from typing import List, Optional
from datetime import datetime
from .models import Bounty, Submission, Winner, Oracle
from .database import get_db

class BountyRepository:
    @staticmethod
    def create(sponsor_address: str, reward: float, deadline: int) -> Bounty:
        with get_db() as db:
            bounty = Bounty(
                sponsor_address=sponsor_address,
                reward=reward,
                deadline=deadline
            )
            db.add(bounty)
            db.flush()
            return bounty

    @staticmethod
    def get_by_id(bounty_id: int) -> Optional[Bounty]:
        with get_db() as db:
            return db.query(Bounty).filter(Bounty.id == bounty_id).first()

    @staticmethod
    def get_active() -> List[Bounty]:
        with get_db() as db:
            current_time = int(datetime.utcnow().timestamp())
            return db.query(Bounty).filter(
                Bounty.deadline > current_time,
                Bounty.paid_out == False
            ).all()

class SubmissionRepository:
    @staticmethod
    def create(bounty_id: int, agent_address: str) -> Submission:
        with get_db() as db:
            submission = Submission(
                bounty_id=bounty_id,
                agent_address=agent_address
            )
            db.add(submission)
            db.flush()
            return submission

    @staticmethod
    def get_by_bounty(bounty_id: int) -> List[Submission]:
        with get_db() as db:
            return db.query(Submission).filter(Submission.bounty_id == bounty_id).all()

class WinnerRepository:
    @staticmethod
    def create(bounty_id: int, winner_address: str, payout_amount: float) -> Winner:
        with get_db() as db:
            winner = Winner(
                bounty_id=bounty_id,
                winner_address=winner_address,
                payout_amount=payout_amount
            )
            db.add(winner)
            db.flush()
            return winner

    @staticmethod
    def get_by_bounty(bounty_id: int) -> List[Winner]:
        with get_db() as db:
            return db.query(Winner).filter(Winner.bounty_id == bounty_id).all()

class OracleRepository:
    @staticmethod
    def create(oracle_address: str) -> Oracle:
        with get_db() as db:
            oracle = Oracle(oracle_address=oracle_address)
            db.add(oracle)
            db.flush()
            return oracle

    @staticmethod
    def get_by_address(oracle_address: str) -> Optional[Oracle]:
        with get_db() as db:
            return db.query(Oracle).filter(Oracle.oracle_address == oracle_address).first()

    @staticmethod
    def get_active() -> List[Oracle]:
        with get_db() as db:
            return db.query(Oracle).filter(Oracle.is_active == True).all() 