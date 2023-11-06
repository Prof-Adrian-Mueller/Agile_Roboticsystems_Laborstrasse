
import pandas as pd
from sqlite3 import Date
from Control.DatabaseConnection import DatabaseConnection
from Control.DatabaseAdapter import DatabaseAdapter
from Control.TubeMetaDaten import TubeMetaDatenImporter
from Control.ExcelImporter import ExcelImporter
from DBUIAdapter import DBUIAdapter
from QRGenAdapter import QRGenAdapter
from TubeQrcode import TubeQrcode
  



ui_db = DBUIAdapter()
# ui_db.create_qr_code(5)

# # Select all data
# ui_db.adapter.select_all_from_tubeqrcode()



# file_path = 'D:\\Bachelorarbeit\\Plasmid_l.xlsx'



    
#     # Instanz der Klasse erstellen
# importer = TubeMetaDatenImporter(file_path)
    
#     # Methode zum Importieren und Ausgeben der Daten aufrufen
# importer.import_data()



# df = pd.read_excel('D:\\Bachelorarbeit\\Plasmid_l.xlsx', engine='openpyxl')
# print(df)

# file_path = 'D:\\Bachelorarbeit\\Plasmid_l.xlsx'
# importer = ExcelImporter(file_path)
# ui_db.db.create_plasmid_table()
ui_db.insert_metadaten()
ui_db.adapter.select_all_from_plasmid()
#importer.import_data()