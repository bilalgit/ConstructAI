from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    ForeignKey
)

from sqlalchemy.orm import relationship

from database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    location = Column(String)

    contract_value = Column(Float)

    start_date = Column(Date)

    planned_duration = Column(Integer)

    activities = relationship(
        "Activity",
        back_populates="project",
        cascade="all, delete-orphan"
    )


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)

    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=False
    )

    activity_code = Column(String)

    name = Column(String, nullable=False)

    wbs = Column(String)

    category = Column(String)

    unit = Column(String)

    quantity = Column(Float)

    # Baseline schedule
    planned_start = Column(Date)

    planned_finish = Column(Date)

    planned_duration = Column(Integer)

    # Actual status
    actual_start = Column(Date)

    actual_finish = Column(Date)

    actual_duration = Column(Integer)

    progress = Column(Float, default=0.0)

        # CPM calculations

    early_start = Column(Date)

    early_finish = Column(Date)

    late_start = Column(Date)

    late_finish = Column(Date)

    total_float = Column(Float)

    is_critical = Column(
        Integer,
        default=0
    )

    project = relationship(
        "Project",
        back_populates="activities"
    )


class Dependency(Base):
    __tablename__ = "dependencies"

    id = Column(Integer, primary_key=True, index=True)

    predecessor_id = Column(
        Integer,
        ForeignKey("activities.id"),
        nullable=False
    )

    successor_id = Column(
        Integer,
        ForeignKey("activities.id"),
        nullable=False
    )

    dependency_type = Column(
        String,
        default="FS"
    )

    lag_days = Column(
        Integer,
        default=0
    )


class DelayEvent(Base):
    __tablename__ = "delay_events"

    id = Column(Integer, primary_key=True, index=True)

    activity_id = Column(
        Integer,
        ForeignKey("activities.id"),
        nullable=False
    )

    delay_date = Column(Date)

    category = Column(String)

    description = Column(String)

    duration_days = Column(Float)

    impact_days = Column(Float)

    activity = relationship("Activity")