import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            if exc_type or exc_val or exc_tb:  # If an error occurred, rollback any changes
                self.conn.rollback()
            else:  # Otherwise, commit any changes
                self.conn.commit()
            self.conn.close()

    def create_table(self):
        with self as conn:
            conn.execute('''
            CREATE TABLE IF NOT EXISTS TubeQrcode (
                qr_code INTEGER PRIMARY KEY,
                datum DATE
            )
            ''')


