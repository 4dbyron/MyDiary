
from app import DB_conns

db = DB_conns()


def create_tables():
    db.query(
        "CREATE TABLE users(id serial PRIMARY KEY, name VARCHAR(100), email VARCHAR(100), username VARCHAR(30), password VARCHAR(100));")

    db.query(
        "CREATE TABLE entries(entry_id serial, user_id INTEGER REFERENCES users(id), title VARCHAR(200), story TEXT, date_created TIMESTAMP DEFAULT NOW());")


if __name__ == '__main__':
    create_tables()
