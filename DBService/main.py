
import pandas as pd
from sqlite3 import Date
from Control.ExcelImporter import ExcelImporter
from DBUIAdapter import DBUIAdapter
  



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


# ui_db.insert_metadaten()
# importer.import_data()

ui_db.insert_experiment_data()
# ui_db.delete_all_experiment()
all_experiments = ui_db.adapter.get_all_experiments()
    # Verarbeiten oder anzeigen Sie die Experimente
for experiment in all_experiments:
        print("_______________________________Returned___________________________")
        print(f"Experiment ID: {experiment.exp_id}, Name: {experiment.name}, Vorname: {experiment.vorname}, Anzahl Tubes: {experiment.anz_tubes}, Video ID: {experiment.video_id}, Datum: {experiment.datum}, Anzahl Fehler: {experiment.anz_fehler}, Bemerkung: {experiment.bemerkung}")

# ui_db.adapter.select_all_from_plasmid()



