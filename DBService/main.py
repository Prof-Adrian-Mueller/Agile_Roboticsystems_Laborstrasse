
import pandas as pd
from sqlite3 import Date
from Control.ExcelImporter import ExcelImporter
from DBUIAdapter import DBUIAdapter
  



ui_db = DBUIAdapter()
# Methode insert_tube
# ui_db.adapter.insert_tube('000006',6,'maxi1','PHB 377')

# ----------------------------------------------
# probe_nr_list = [1, 2, 3, 4, 5]

# # Aufruf der Methode mit der Liste und den einzelnen Werten für exp_id und plasmid_nr
# ui_db.adapter.insert_tubes(probe_nr_list, 'maxi1', 'PHB 377')


# all_tubes = ui_db.adapter.get_all_tcubes()

#     # Drucken Sie die Ergebnisse
# for tube in all_tubes:
#         print(tube)
# ________________________________
# ui_db.adapter.add_experiment("maxi", "Mustermann", 5,32, '2023-10-22')
# return Experiments daten
# print(ui_db.adapter.get_experiment_by_id("maxi1"))
# print(ui_db.adapter.get_experiment_count_for_laborant("maxi"))
# print(ui_db.adapter.get_laborant_count())
# ui_db.adapter.add_experiment(2, "Max", "Mustermann", 5, '2023-10-22')
# all_experiments=ui_db.adapter.get_experiments()
# for experiment in all_experiments:
#     print(f"Experiment ID: {experiment.exp_id}, Name: {experiment.name}, Vorname: {experiment.vorname}, Anzahl Tubes: {experiment.anz_tubes},anzahl Plasmid:{experiment.anz_plasmid} Datum: {experiment.datum}")
#  ________________________________________
# ui_db.adapter.add_laborant("maxi","sch")
# ++++++++++++++++++++++++++++++++++++++++++
# ui_db.create_qr_code(5)
# ui_db.adapter.drop_table_tube_qrcode()
# # Select all data
# ui_db.adapter.select_all_from_tubeqrcode()
# Abrufen der ersten 5 QR-Codes
# first_five_qr_codes = ui_db.adapter.get_next_qr_codes(5)
# print("Erste 5 QR-Codes:", first_five_qr_codes)

# # Abrufen der nächsten 4 QR-Codes
# next_four_qr_codes = ui_db.adapter.get_next_qr_codes(4)
# print("Nächste 4 QR-Codes:", next_four_qr_codes)
# ui_db.adapter.check_qr_code_count(10)
# ++++++++++++++++++++++++++++++++++++++++++++

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

# ++++++++++++++++++++++++++++++++++

# Metadaten

# ui_db.insert_metadaten()
# ui_db.adapter.select_all_from_plasmid()

# +++++++++++++++++++++++++++++++++

# importer.import_data()

# ui_db.insert_experiment_data()
# # ui_db.delete_all_experiment()
# all_experiments = ui_db.adapter.get_all_experiments()
    # Verarbeiten oder anzeigen Sie die Experimente
# for experiment in all_experiments:
#         print("_______________________________Returned___________________________")
#         print(f"Experiment ID: {experiment.exp_id}, Name: {experiment.name}, Vorname: {experiment.vorname}, Anzahl Tubes: {experiment.anz_tubes}, Video ID: {experiment.video_id}, Datum: {experiment.datum}, Anzahl Fehler: {experiment.anz_fehler}, Bemerkung: {experiment.bemerkung}")





