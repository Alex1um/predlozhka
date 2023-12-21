import pickle

database = {"channels": set(), "admin_chats": dict(), "channel_admins": dict(), "user_chats": dict()}

def load_database():
    with open("database.pickle", "rb") as f:
        global database
        database = pickle.load(f)

def save_database():
    with open("database.pickle", "wb") as f:
        pickle.dump(database, f)