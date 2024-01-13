import pandas as pd
import concurrent.futures

from DBService.Model.Plasmid import Plasmid
from DBService.Control.DatabaseAdapter import DatabaseAdapter

class ExcelImporter:
    def __init__(self, adapter,file_path):
        self.adapter=adapter
        self.file_path = file_path
        self.plasmids = []


    def import_data(self):
        print("import_data")
        df = pd.read_excel(self.file_path)
        required_columns = ['Plasmid Nr.', 'Antibiotika', 'Vektor', 'Insert', 'Spezies/Quelle',
                            'Sequenz Nr. Name Datum Maxi',
                            'Quelle + Datum der Konstruktion', 'Verdau', 'Klonierungsstrategie Bemerkung',
                            'Farbcode der Plasmide:']
        ausgabe_data = []

        # Überprüfen, ob die erforderlichen Spalten vorhanden sind
        for column in required_columns:
            if column not in df.columns:
                ausgabe_data.append(f"Die erforderliche Spalte '{column}' ist nicht in der Excel-Datei vorhanden.")
                return ausgabe_data

        # Überprüfen, ob die Tabelle 'Plasmid' existiert
        try:
            if not self.adapter.does_table_exist("Plasmid"):
                print("Tabelle 'Plasmid' existiert nicht. Sie wird erstellt.")
                self.adapter.create_plasmid_table()
        except Exception as e:
            return [f"Error checking Plasmid table existence: {str(e)}"]  # Return a list containing the error message

        for index, row in df.iterrows():
            # Überspringe die Zeile, wenn 'Plasmid Nr.' leer ist
            if pd.isna(row['Plasmid Nr.']):
                continue
            # Erstelle ein Plasmid-Objekt mit den erforderlichen Spalten
            plasmid = Plasmid(
                row['Plasmid Nr.'], row['Antibiotika'], row['Vektor'], row['Insert'], row['Spezies/Quelle'],
                row['Sequenz Nr. Name Datum Maxi'], row['Quelle + Datum der Konstruktion'], row['Verdau'],
                row['Klonierungsstrategie Bemerkung'], row['Farbcode der Plasmide:']
            )
            self.plasmids.append(plasmid)

            # Füge das Plasmid in die Datenbank ein
        if not self.adapter.insert_plasmid(self.plasmids):
            return ["Error inserting plasmid"]
        return ausgabe_data
