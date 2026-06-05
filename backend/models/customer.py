from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, ForeignKey, Text, JSON, Enum as SQLEnum, Index
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime
import uuid
import enum

class CustomerStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    CHURNED = "churned"
    SUSPENDED = "suspended"

class Customer(Base):
    __tablename__ = "customers"
    __table_args__ = (
        Index('idx_business_status', 'business_id', 'status'),
        Index('idx_business_created', 'business_id', 'created_at'),
    )

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id = Column(String(36), ForeignKey("businesses.id"), nullable=False, index=True)
    
    # Customer Information
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=True)
    email = Column(String(255), nullable=False, index=True)
    phone = Column(String(20), nullable=True)
    company = Column(String(255), nullable=True)
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    postal_code = Column(String(20), nullable=True)
    
    # Customer Status
    status = Column(SQLEnum(CustomerStatus), default=CustomerStatus.ACTIVE, index=True)
    
    # Customer Value
    total_revenue = Column(Float, default=0.0)
    lifetime_value = Column(Float, default=0.0)
    average_order_value = Column(Float, default=0.0)
    total_orders = Column(Integer, default=0)
    
    # Customer Metrics
    churn_probability = Column(Float, default=0.0)
    satisfaction_score = Column(Float, nullable=True)
    nps_score = Column(Integer, nullable=True)
    
    # Engagement
    last_purchase_date = Column(DateTime, nullable=True)
    last_interaction_date = Column(DateTime, nullable=True)
    days_since_last_interaction = Column(Integer, default=0)
    
    # Metadata
    metadata = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    # Relationships
    business = relationship("Business", back_populates="customers")

    def __repr__(self):
        return f"<Customer {self.email}>"