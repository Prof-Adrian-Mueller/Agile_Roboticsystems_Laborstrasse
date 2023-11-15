from Control.DatabaseConnection import DatabaseConnection
from Control.DatabaseAdapter import DatabaseAdapter
from Control.ExcelImporter import ExcelImporter
from Control.ExperimentImporter import ExperimentImporter
from QRGenAdapter import QRGenAdapter
import tkinter as tk
from tkinter import filedialog

class DBUIAdapter:
    def __init__(self):
        self.db = DatabaseConnection("laborstreet_management")
        self.adapter = DatabaseAdapter(self.db)
        self.qr_gen = QRGenAdapter(self.adapter)
        # self.importer=ExcelImporter(self.adapter, file_path = 'D:\\Bachelorarbeit\\Plasmid_l.xlsx')
        self.importer = None  # Initialisieren Sie den Importer später


    def select_file(self):
        root = tk.Tk()
        root.withdraw()  # Verstecken Sie das Hauptfenster
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
        return file_path
        
    def create_qr_code(self,total: int):
        for i in range(total):
            self.qr_gen.create_tube_qrcode()

    def insert_metadaten(self,file_path):
       # file_path=self.select_file()
        if file_path:
            self.importer=ExcelImporter(self.adapter,file_path)
            self.importer.import_data()
        else:
            print("Keine Datei ausgewählt.")

    def insert_experiment_data(self,file_path):
        # file_path = self.select_file()
        if file_path:
            # eine Instanz des ExperimentImporters mit dem ausgewählten Dateipfad
            self.experiment_importer = ExperimentImporter(self.adapter, file_path)
            #die Methode import_data auf, um die Daten zu importieren
            self.experiment_importer.import_data()
        else:
            print("Keine Datei ausgewählt.")



    def delete_all_experiment(self):
        self.adapter.delete_all_experiments()


