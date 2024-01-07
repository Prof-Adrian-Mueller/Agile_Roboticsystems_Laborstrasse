import pandas as pd

from DBService.Model.Plasmid import Plasmid
from DBService.Control.DatabaseAdapter import DatabaseAdapter

class ExcelImporter:
    def __init__(self, adapter,file_path):
        self.adapter=adapter
        self.file_path = file_path
        self.plasmids = []

    # def import_data(self):
    #     df = pd.read_excel(self.file_path)
    #     required_columns = ['Plasmid_nr', 'Vektor', 'Insert', 'Sequnez_nr', 'Name', 'Datum_maxi', 'Quelle', 'Konstruktion_datum']
        
    #     for column in required_columns:
    #         if column not in df.columns:
    #             print(f"Die erforderliche Spalte '{column}' ist nicht in der Excel-Datei vorhanden.")
    #             return

    #     for index, row in df.iterrows():
    #         plasmid = Plasmid(row['Plasmid_nr'], row['Vektor'], row['Insert'], row['Sequnez_nr'], row['Name'], row['Datum_maxi'], row['Quelle'], row['Konstruktion_datum'])
    #         self.plasmids.append(plasmid)

    #     # Ausgabe der Daten
    #     for plasmid in self.plasmids:
    #         print(f"Plasmid Nr: {plasmid.plasmid_nr}, Vektor: {plasmid.vektor}, Insert: {plasmid.insert}, Sequenz Nr: {plasmid.sequenz_nr}, Name: {plasmid.name}, Datum Maxi: {plasmid.datum_maxi}, Quelle: {plasmid.quelle}, Konstruktion Datum: {plasmid.konstruktion_datum}")
    #         self.adapter.insert_plasmid(plasmid)        
    
    # def import_data(self):
    #     df = pd.read_excel(self.file_path)
    #     required_columns = ['Plasmid_nr', 'Vektor', 'Insert', 'Sequnez_nr', 'Name', 'Datum_maxi', 'Quelle', 'Konstruktion_datum']
    #     ausgabe_data = []
    #
    #     for column in required_columns:
    #         if column not in df.columns:
    #             ausgabe_data.append(f"Die erforderliche Spalte '{column}' ist nicht in der Excel-Datei vorhanden.")
    #             return ausgabe_data
    #
    #     for index, row in df.iterrows():
    #         plasmid = Plasmid(row['Plasmid_nr'], row['Vektor'], row['Insert'], row['Sequnez_nr'], row['Name'], row['Datum_maxi'], row['Quelle'], row['Konstruktion_datum'])
    #         self.plasmids.append(plasmid)
    #
    #     # Ausgabe der Daten
    #     for plasmid in self.plasmids:
    #         ausgabe_data.append(f"Plasmid Nr: {plasmid.plasmid_nr}, Vektor: {plasmid.vektor}, Insert: {plasmid.insert}, Sequenz Nr: {plasmid.sequenz_nr}, Name: {plasmid.name}, Datum Maxi: {plasmid.datum_maxi}, Quelle: {plasmid.quelle}, Konstruktion Datum: {plasmid.konstruktion_datum}")
    #         self.adapter.insert_plasmid(plasmid)
    #
    #     return ausgabe_data

    def import_data(self):
        print("import_data")
        df = pd.read_excel(self.file_path)
        required_columns = ['Plasmid Nr.', 'Antibiotika', 'Vektor', 'Insert', 'Spezies/Quelle', 'Sequenz Nr. Name Datum Maxi',
                            'Quelle + Datum der Konstruktion', 'Verdau', 'Klonierungsstrategie Bemerkung', 'Farbcode der Plasmide:']
        ausgabe_data = []

        # Überprüfen, ob die erforderlichen Spalten vorhanden sind
        for column in required_columns:
            if column not in df.columns:
                ausgabe_data.append(f"Die erforderliche Spalte '{column}' ist nicht in der Excel-Datei vorhanden.")
                return ausgabe_data
        # Überprüfen, ob die Tabelle 'Plasmid' existiert
        if not self.adapter.does_table_exist("Plasmid"):
            print("Tabelle 'Plasmid' existiert nicht. Sie wird erstellt.")
            self.adapter.create_plasmid_table()
        for index, row in df.iterrows():
            # Überspringe die Zeile, wenn 'Plasmid Nr.' leer ist
            if pd.isna(row['Plasmid Nr.']):
                continue
            # Erstelle ein Plasmid-Objekt mit den erforderlichen Spalten
            plasmid = Plasmid(
                row['Plasmid Nr.'], row['Antibiotika'], row['Vektor'], row['Insert'], row['Spezies/Quelle'],
                row['Sequenz Nr. Name Datum Maxi'], row['Quelle + Datum der Konstruktion'], row['Verdau'], row['Klonierungsstrategie Bemerkung'], row['Farbcode der Plasmide:']
            )
            self.plasmids.append(plasmid)

        # Ausgabe der Daten
        for plasmid in self.plasmids:
            ausgabe_data.append(
                f"Plasmid Nr: {plasmid.plasmid_nr}, Antibiotika: {plasmid.antibiotika},Vektor: {plasmid.vektor}, Insert: {plasmid.insert},Quelle:{plasmid.quelle}, Sequenz Nr: {plasmid.sequenz_nr}, Konstruktion: {plasmid.konstruktion}, Verdau: {plasmid.verdau}, Bemerkung: {plasmid.bemerkung}, Farbecode: {plasmid.farbecode}")
            self.adapter.insert_plasmid(plasmid)

        return ausgabe_data

