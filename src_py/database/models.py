from datetime import datetime
from sqlalchemy import Column, Integer, String, Numeric, Boolean, BigInteger, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Bounty(Base):
    __tablename__ = 'bounties'
    
    id = Column(Integer, primary_key=True)
    sponsor_address = Column(String(42), nullable=False)  # Ethereum address length
    reward = Column(Numeric(18, 8), nullable=False)  # For precise decimal handling
    deadline = Column(BigInteger, nullable=False)  # UNIX timestamp
    paid_out = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    submissions = relationship("Submission", back_populates="bounty")
    winners = relationship("Winner", back_populates="bounty")

class Submission(Base):
    __tablename__ = 'submissions'
    
    id = Column(Integer, primary_key=True)
    bounty_id = Column(Integer, ForeignKey('bounties.id'), nullable=False)
    agent_address = Column(String(42), nullable=False)  # Ethereum address length
    submitted_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    bounty = relationship("Bounty", back_populates="submissions")

class Winner(Base):
    __tablename__ = 'winners'
    
    id = Column(Integer, primary_key=True)
    bounty_id = Column(Integer, ForeignKey('bounties.id'), nullable=False)
    winner_address = Column(String(42), nullable=False)  # Ethereum address length
    payout_amount = Column(Numeric(18, 8), nullable=False)  # For precise decimal handling
    paid_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    bounty = relationship("Bounty", back_populates="winners")

class Oracle(Base):
    __tablename__ = 'oracles'
    
    id = Column(Integer, primary_key=True)
    oracle_address = Column(String(42), nullable=False, unique=True)  # Ethereum address length
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

class TestResult(Base):
    __tablename__ = 'test_results'
    submission_id = Column(Integer, ForeignKey('submissions.id'), primary_key=True)
    score = Column(Numeric(18, 8), nullable=False)
    passed = Column(Boolean, nullable=False)
    evaluated_at = Column(DateTime, default=datetime.utcnow)

    submission = relationship("Submission")

class Payout(Base):
    __tablename__ = 'payouts'
    id = Column(Integer, primary_key=True)
    bounty_id = Column(Integer, ForeignKey('bounties.id'), nullable=False)
    winner_address = Column(String(42), nullable=False)
    share = Column(Numeric(18, 8), nullable=False)
    tx_hash = Column(String(66), nullable=True)
    paid_at = Column(DateTime, default=datetime.utcnow)

    bounty = relationship("Bounty") 