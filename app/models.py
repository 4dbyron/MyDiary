"""Create & Manage tables in my_diary"""
import psycopg2


class db_table(object):
    """Initialise tables"""

    def __init__(self, db_name):
        self.db_name = db_name

    def create_tables(self):
        conn = psycopg2.connect(self.db_name)
        cursor = conn.cursor()

        # Generate Users Table
        cursor.execute("CREATE TABLE users (id serial PRIMARY KEY, " \
                       "username varchar not null unique,password varchar not null )"
                       )
        # Generate Entries Table
        cursor.execute("CREATE TABLE entries (id serial PRIMARY KEY, title varchar not null unique" \
                       ",content varchar not null, user_id integer references users(id))")
        conn.commit()
        conn.close()

    def drop_all(self):
        conn = psycopg2.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT table_schema, table_name FROM information_schema.tables"\
            " WHERE table_schema = 'public' ORDER BY table_schema,table_name")

        records = cursor.fetchall()
        for row in records:
            cursor.execute("drop table " + row[1] + " cascade")
        cursor.close()
        conn.commit()
        conn.close()


class user(object):
    """Save Users to Database"""

    def __init__(self, db_name):
        """Initialize empty user object"""
        self.data = None
        self.username = None
        self.password = None
        self.db_name = db_name

    def create(self, name, password):
        """add new user"""
        self.username = name
        self.password = password
        self.save()

    def save(self):
        """save user data after Creation or Modification"""
        conn = psycopg2.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)",
                       (self.username, self.password,)
                       )
        conn.commit()
        conn.close()

    def get_all(self):
        """Return all users"""
        conn = psycopg2.connect(self.db_name)
        cursor = conn.cursor()
        # save data
        cursor.execute("SELECT * FROM users")
        table_data = cursor.fetchall()
        temp = []
        token = None
        for single_user in table_data:
            temp.append({"id": single_user[0], "username": single_user[1], "password": single_user[2]})
        self.data = temp
        conn.commit()
        conn.close()
        return self.data


class entry(object):
    def __init__(self, db_name):
        self.data = None
        self.title = None
        self.content = None
        self.user_id = None
        self.db_name = db_name

    def create(self, title, content, user_id):
        self.title = title
        self.content = content
        self.user_id = user_id
        self.save()

    def save(self):
        """Save an Entry"""
        conn = psycopg2.connect(self.db_name)
        cursor = conn.cursor()
        # save data
        cursor.execute("INSERT INTO entries (title, content, user_id ) VALUES (%s, %s, %s)",
                       (self.title, self.content, self.user_id,)
                       )
        conn.commit()
        conn.close()

    def update(self, id, title, content):
        """Update an entry"""
        conn = psycopg2.connect(self.db_name)
        cursor = conn.cursor()
        # save data
        cursor.execute("UPDATE entries SET content = %s , title = %s WHERE id = %s",
                       (content, title, id,)
                       )
        conn.commit()
        conn.close()

    def get_all(self):
        """Return All MyDiary Users"""
        conn = psycopg2.connect(self.db_name)
        cursor = conn.cursor()

        # save data
        cursor.execute("SELECT * FROM entries")
        table_data = cursor.fetchall()
        temp = []
        token = None
        for single_entry in table_data:
            temp.append({"id": single_entry[0], "title": single_entry[1], "content": single_entry[2],
                         "user_id": single_entry[3]})
        self.data = temp
        conn.commit()
        conn.close()
        return self.data
