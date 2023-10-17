

class DatabaseAdapter:
    def __init__(self, db):
        self.db = db

    def insert_data(self, tubeQrcode):
        with self.db as conn:
            conn.execute("INSERT INTO TubeQrcode (qr_code, datum) VALUES (?, ?)", (tubeQrcode.qr_code, tubeQrcode.datum))

    def select_all_from_tubeqrcode(self):
        with self.db as conn:
            rows = conn.execute("SELECT * FROM TubeQrcode").fetchall()
            for row in rows:
                    formatted_qr_code = str(row[0]).zfill(6)
                    print((formatted_qr_code, row[1]))


