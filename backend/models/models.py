"""
Database models for the application
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Text, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from core.database import Base
import enum


class UserRole(str, enum.Enum):
    """User roles"""
    SUPER_ADMIN = "super_admin"
    BUSINESS_OWNER = "business_owner"
    SALES_EXECUTIVE = "sales_executive"
    CUSTOMER = "customer"


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    role = Column(Enum(UserRole), default=UserRole.CUSTOMER, nullable=False)
    is_active = Column(Boolean, default=True)
    email_verified = Column(Boolean, default=False)
    phone_verified = Column(Boolean, default=False)
    profile_picture_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)
    
    # Relationships
    businesses = relationship("Business", back_populates="owner")
    leads = relationship("Lead", back_populates="owner")
    customers = relationship("Customer", back_populates="user")


class Business(Base):
    """Business model"""
    __tablename__ = "businesses"
    
    id = Column(String(36), primary_key=True)
    owner_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    business_name = Column(String(255), nullable=False)
    business_email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(20), nullable=False)
    industry = Column(String(100), nullable=False)
    website = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    logo_url = Column(String(500), nullable=True)
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String(255), nullable=True)
    subscription_tier = Column(String(50), default="free")
    status = Column(String(50), default="active")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    owner = relationship("User", back_populates="businesses")
    leads = relationship("Lead", back_populates="business")
    customers = relationship("Customer", back_populates="business")
    team_members = relationship("TeamMember", back_populates="business")
    subscriptions = relationship("Subscription", back_populates="business")


class Lead(Base):
    """Lead model"""
    __tablename__ = "leads"
    
    id = Column(String(36), primary_key=True)
    business_id = Column(String(36), ForeignKey("businesses.id"), nullable=False)
    owner_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    customer_id = Column(String(36), ForeignKey("customers.id"), nullable=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    company = Column(String(255), nullable=True)
    position = Column(String(100), nullable=True)
    source = Column(String(100), nullable=False)  # form, api, email, etc.
    status = Column(String(50), default="new")  # new, contacted, qualified, converted, lost
    score = Column(Float, default=0.0)
    estimated_value = Column(Float, default=0.0)
    converted_at = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    tags = Column(JSON, default=[])
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    business = relationship("Business", back_populates="leads")
    owner = relationship("User", back_populates="leads")
    interactions = relationship("Interaction", back_populates="lead")


class Customer(Base):
    """Customer model"""
    __tablename__ = "customers"
    
    id = Column(String(36), primary_key=True)
    business_id = Column(String(36), ForeignKey("businesses.id"), nullable=False)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    company = Column(String(255), nullable=True)
    lifetime_value = Column(Float, default=0.0)
    churn_risk = Column(Float, default=0.0)
    status = Column(String(50), default="active")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    business = relationship("Business", back_populates="customers")
    user = relationship("User", back_populates="customers")
    interactions = relationship("Interaction", back_populates="customer")


class Interaction(Base):
    """Customer interaction model"""
    __tablename__ = "interactions"
    
    id = Column(String(36), primary_key=True)
    lead_id = Column(String(36), ForeignKey("leads.id"), nullable=True)
    customer_id = Column(String(36), ForeignKey("customers.id"), nullable=True)
    interaction_type = Column(String(50), nullable=False)  # email, call, meeting, note
    subject = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    lead = relationship("Lead", back_populates="interactions")
    customer = relationship("Customer", back_populates="interactions")


class Subscription(Base):
    """Subscription model"""
    __tablename__ = "subscriptions"
    
    id = Column(String(36), primary_key=True)
    business_id = Column(String(36), ForeignKey("businesses.id"), nullable=False)
    plan_id = Column(String(36), ForeignKey("subscription_plans.id"), nullable=False)
    status = Column(String(50), default="active")  # active, cancelled, suspended
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    auto_renew = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    business = relationship("Business", back_populates="subscriptions")
    plan = relationship("SubscriptionPlan", back_populates="subscriptions")


class SubscriptionPlan(Base):
    """Subscription plan model"""
    __tablename__ = "subscription_plans"
    
    id = Column(String(36), primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    billing_cycle = Column(String(20), default="monthly")  # monthly, annual
    features = Column(JSON, nullable=False)
    max_leads = Column(Integer, default=1000)
    max_customers = Column(Integer, default=1000)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    subscriptions = relationship("Subscription", back_populates="plan")


class TeamMember(Base):
    """Team member model"""
    __tablename__ = "team_members"
    
    id = Column(String(36), primary_key=True)
    business_id = Column(String(36), ForeignKey("businesses.id"), nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)
    status = Column(String(50), default="active")
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    business = relationship("Business", back_populates="team_members")


class AuditLog(Base):
    """Audit log model"""
    __tablename__ = "audit_logs"
    
    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    action = Column(String(100), nullable=False)
    resource_type = Column(String(100), nullable=False)
    resource_id = Column(String(36), nullable=False)
    changes = Column(JSON, nullable=True)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(500), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
