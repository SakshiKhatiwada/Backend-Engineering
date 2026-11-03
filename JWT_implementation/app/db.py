from sqlmodel import create_engine, Session

DB_URL = "sqlite:///../auth.db"

engine= create_engine(DB_URL, connect_args={"check_same_thread": False})

def get_session():
    with Session(engine) as session:
        yield session