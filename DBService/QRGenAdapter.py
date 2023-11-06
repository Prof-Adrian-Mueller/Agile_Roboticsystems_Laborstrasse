import datetime

from DBService.TubeQrcode import TubeQrcode

class QRGenAdapter:
    def __init__(self, db_adapter):
        self.db_adapter = db_adapter

    def get_last_qr_code(self):
        with self.db_adapter.db as conn:
            row = conn.execute("SELECT MAX(qr_code) FROM TubeQrcode").fetchone()
            return int(row[0]) if row[0] else 0


    def create_tube_qrcode(self):
        last_qr_code = self.get_last_qr_code()
        new_qr_code = str(last_qr_code + 1).zfill(6)  # QR-Code startet bei 000001
        print(new_qr_code)
        datum = datetime.date.today()  # Aktuelles Datum
        tube_qrcode = TubeQrcode(new_qr_code, datum)
        self.db_adapter.insert_data(tube_qrcode)
        return tube_qrcode
