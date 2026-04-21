# database/models.py
from sqlalchemy import (
    Column, BigInteger, Integer, SmallInteger, String, Float,
    Boolean, Text, LargeBinary, DateTime, JSON, UniqueConstraint
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(String(64), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(32), nullable=False, default="user")
    is_active = Column(Boolean, nullable=False, default=True)
    behavioral_profile = Column(LargeBinary)           # BYTEA — Uthkarsh's serialized UserProfile
    profile_updated_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class ActiveSession(Base):
    __tablename__ = "active_sessions"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    session_id = Column(BigInteger, unique=True, nullable=False)
    user_id = Column(BigInteger, nullable=False)
    device_hash = Column(BigInteger, nullable=False)
    ip_hash = Column(Integer, nullable=False)
    geo_hash = Column(Integer, nullable=False)
    current_risk_score = Column(Float, nullable=False, default=0.0)
    current_decision = Column(String(16), nullable=False, default="ALLOW")
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    last_active_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)


class RiskEventLog(Base):
    __tablename__ = "risk_event_log"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    session_id = Column(BigInteger, nullable=False)
    user_id = Column(BigInteger, nullable=False)
    event_type = Column(String(32), nullable=False)
    timestamp_unix = Column(BigInteger, nullable=False)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())
    risk_score = Column(Float, nullable=False)
    rule_score = Column(Float, nullable=False)
    ml_score = Column(Float, nullable=False, default=0.0)
    risk_level = Column(String(16), nullable=False)
    decision = Column(String(16), nullable=False)
    reason_code = Column(Integer, nullable=False, default=0)
    ip_hash = Column(Integer)
    device_hash = Column(BigInteger)
    geo_hash = Column(Integer)
    bytes_transferred = Column(Integer, default=0)
    endpoint_hash = Column(Integer)
    login_hour = Column(SmallInteger)
    failed_attempts = Column(SmallInteger, default=0)
    row_hmac = Column(LargeBinary, nullable=False)


class AdminAuditLog(Base):
    __tablename__ = "admin_audit_log"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    admin_user_id = Column(BigInteger, nullable=False)
    action = Column(String(64), nullable=False)
    target_user_id = Column(BigInteger)
    target_session_id = Column(BigInteger)
    details = Column(JSON)
    ip_hash = Column(Integer)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())
    row_hmac = Column(LargeBinary, nullable=False)


class DeviceRegistry(Base):
    __tablename__ = "device_registry"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False)
    device_hash = Column(BigInteger, nullable=False)
    first_seen_at = Column(DateTime(timezone=True), server_default=func.now())
    last_seen_at = Column(DateTime(timezone=True), server_default=func.now())
    is_trusted = Column(Boolean, nullable=False, default=False)
    trust_granted_by = Column(BigInteger)
    __table_args__ = (UniqueConstraint("user_id", "device_hash"),)


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False)
    session_id = Column(BigInteger)
    alert_type = Column(String(64), nullable=False)
    severity = Column(String(16), nullable=False)
    description = Column(Text)
    risk_score = Column(Float)
    is_resolved = Column(Boolean, nullable=False, default=False)
    resolved_by = Column(BigInteger)
    resolved_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class MLModelVersion(Base):
    __tablename__ = "ml_model_versions"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    file_path = Column(String(512), nullable=False)
    trained_at = Column(DateTime(timezone=True), server_default=func.now())
    training_data_size = Column(Integer, nullable=False)
    false_positive_rate = Column(Float)
    detection_rate = Column(Float)
    contamination = Column(Float)
    n_estimators = Column(Integer)
    is_active = Column(Boolean, nullable=False, default=False)
    notes = Column(Text)