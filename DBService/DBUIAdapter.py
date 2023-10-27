from DBService.Control.DatabaseConnection import DatabaseConnection
from DBService.Control.DatabaseAdapter import DatabaseAdapter
from DBService.QRGenAdapter import QRGenAdapter


class DBUIAdapter:
    def __init__(self):
        self.db = DatabaseConnection("laborstreet_management")
        self.adapter = DatabaseAdapter(self.db)
        self.qr_gen = QRGenAdapter(self.adapter)

    def create_qr_code(self,total: int):
        for i in range(total):
            self.qr_gen.create_tube_qrcode()