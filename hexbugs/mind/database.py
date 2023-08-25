from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from hexbugs.mind.models import Base
from hexbugs.mind.utils import check_trigger_exists, execute_sql_file
from hexbugs.config import Config

engine = create_engine(f"sqlite:///{Config.DB_PATH}")
Base.metadata.create_all(engine)

if not check_trigger_exists('verify_bug_id_before_transaction'):
    execute_sql_file(Config.SQL_PATH)

Session = sessionmaker(bind=engine)
