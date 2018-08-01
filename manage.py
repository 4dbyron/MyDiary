from app.models import db_table

db = db_table("db_name = my_diary_db")
db.create_tables()
