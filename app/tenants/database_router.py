from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from urllib.parse import urlparse
from app.models import Base

tenant_sessions = {}

def get_tenant_session(db_uri):
    if db_uri not in tenant_sessions:
        engine = create_engine(db_uri)
        session_factory = sessionmaker(bind=engine)
        tenant_sessions[db_uri] = scoped_session(session_factory)
    return tenant_sessions[db_uri]

def create_database_if_not_exists(db_uri):
    parsed = urlparse(db_uri)
    db_name = parsed.path[1:]  
    admin_db_uri = db_uri.replace(f"/{db_name}", "/postgres")  # connect to postgres default DB

    engine = create_engine(admin_db_uri, isolation_level="AUTOCOMMIT")
    with engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE {db_name}"))

def setup_tenant_schema(db_uri):
    engine = create_engine(db_uri)
    Base.metadata.create_all(bind=engine) 
