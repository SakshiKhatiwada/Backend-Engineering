from RoleBasedAccessControl.app.models import User


def get_user(db, username: str):
    if username in db:
        user = db[username]
        return User(**user)
    
