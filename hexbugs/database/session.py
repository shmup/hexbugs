from hexbugs.config import Config
from hexbugs.database import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import all models here
from hexbugs.models import Action, Game, GamePlayer, Player, Transaction

engine = create_engine(f"sqlite:///{Config.DB_PATH}")

# Consider using migrations for schema updates in production
Base.metadata.create_all(engine)

# If your application is not multi-threaded, consider using sessionmaker directly
Session = sessionmaker(bind=engine)
