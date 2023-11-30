import pandas as pd
from DBService.Control.DatabaseAdapter import DatabaseAdapter

from DBService.Model.Experiment import Experiment


class ExperimentImporter:
    def __init__(self, adapter, file_path):
        self.adapter = adapter
        self.file_path = file_path
        self.experiments = []

    def import_data(self):
        df = pd.read_excel(self.file_path)
        required_columns = ['exp_id', 'name', 'vorname', 'anz_tubes', 'video_id', 'datum', 'anz_fehler', 'bemerkung']
        
        ausgabe_data = []

        for column in required_columns:
            if column not in df.columns:
                ausgabe_data.append(f"Die erforderliche Spalte '{column}' ist nicht in der Excel-Datei vorhanden.")
                return ausgabe_data

        for index, row in df.iterrows():
            experiment = Experiment(row['exp_id'], row['name'], row['vorname'], row['anz_tubes'], row['video_id'], row['datum'], row['anz_fehler'], row['bemerkung'])
            self.experiments.append(experiment)

        # Ausgabe der Daten
        for experiment in self.experiments:
            print("_______________________________Imported_________________________________________________")
            ausgabe_data.append(f"Experiment ID: {experiment.exp_id}, Name: {experiment.name}, Vorname: {experiment.vorname}, Anzahl Tubes: {experiment.anz_tubes}, Video ID: {experiment.video_id}, Datum: {experiment.datum}, Anzahl Fehler: {experiment.anz_fehler}, Bemerkung: {experiment.bemerkung}")         
            self.adapter.insert_experiment(experiment)
        return ausgabe_data