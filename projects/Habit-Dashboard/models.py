from datetime import date
from sqlalchemy import Column, Integer, Float, Date, create_engine, UniqueConstraint
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class DailyEntry(Base):
    __tablename__  = "daily_entry"
    id             = Column(Integer, primary_key=True)
    day            = Column(Date, default=date.today, nullable=False, unique=True)

    sleep_hours    = Column(Float)   # 0‑24
    mood           = Column(Integer) # 1‑5
    weight_kg      = Column(Float)
    workouts_min   = Column(Integer) # 0—n
    code_min       = Column(Integer)

    __table_args__ = (UniqueConstraint("day", name="_uniq_day"),)

# sqlite:///habit.db in project root
engine = create_engine("sqlite:///habit.db", echo=False, future=True)
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
