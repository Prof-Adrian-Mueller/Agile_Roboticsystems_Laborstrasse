

from sqlite3 import Date
from Control.DatabaseConnection import DatabaseConnection
from Control.DatabaseAdapter import DatabaseAdapter
from DBUIAdapter import DBUIAdapter
from QRGenAdapter import QRGenAdapter
from TubeQrcode import TubeQrcode
  



ui_db = DBUIAdapter()
ui_db.create_qr_code(5)

# Select all data
ui_db.adapter.select_all_from_tubeqrcode()
