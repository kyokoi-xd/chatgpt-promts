from sqlalchemy import create_engine, MetaData
from databases import Database

Database_URL = "postgresql://user:password@localhost:5432/promtarium"

database = Database(Database_URL)
metadata = MetaData()
engine = create_engine(Database_URL)