from sqlmodel import create_engine
sqlite_file_name = "customers.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {
    "check_same_thread": False,
}

engine = create_engine(url=sqlite_url, connect_args=connect_args, echo=False)