import pandas as pd

from Model.Plasmid import Plasmid
from Control.DatabaseAdapter import DatabaseAdapter

class ExcelImporter:
    def __init__(self, adapter,file_path):
        self.adapter=adapter

        
     
        self.file_path = file_path
        self.plasmids = []

    def import_data(self):
        df = pd.read_excel(self.file_path)
        required_columns = ['Plasmid_nr', 'Vektor', 'Insert', 'Sequnez_nr', 'Name', 'Datum_maxi', 'Quelle', 'Konstruktion_datum']
        
        for column in required_columns:
            if column not in df.columns:
                print(f"Die erforderliche Spalte '{column}' ist nicht in der Excel-Datei vorhanden.")
                return

        for index, row in df.iterrows():
            plasmid = Plasmid(row['Plasmid_nr'], row['Vektor'], row['Insert'], row['Sequnez_nr'], row['Name'], row['Datum_maxi'], row['Quelle'], row['Konstruktion_datum'])
            self.plasmids.append(plasmid)

        # Ausgabe der Daten
        for plasmid in self.plasmids:
            print(f"Plasmid Nr: {plasmid.plasmid_nr}, Vektor: {plasmid.vektor}, Insert: {plasmid.insert}, Sequenz Nr: {plasmid.sequenz_nr}, Name: {plasmid.name}, Datum Maxi: {plasmid.datum_maxi}, Quelle: {plasmid.quelle}, Konstruktion Datum: {plasmid.konstruktion_datum}")
            self.adapter.insert_plasmid(plasmid)