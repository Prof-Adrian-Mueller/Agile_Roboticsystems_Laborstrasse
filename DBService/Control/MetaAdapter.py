
import tkinter as tk
from tkinter import filedialog
from Control.ExcelImporter import ExcelImporter
from Control.DatabaseAdapter import DatabaseAdapter
from Control.DatabaseConnection import DatabaseConnection


 # TODO
    # get metadaten bei Plasmid_nr
    # zurückgeben=>alle metadaten von Plasmid_nr
class MetaAdapter:
    def __init__(self):
        self.db = DatabaseConnection("laborstreet_management")
        self.database_adapter = DatabaseAdapter(self.db)
        self.ensure_tables_exist()
       

        self.importer = None  # Initialisieren Sie den Importer später

    def ensure_tables_exist(self):
        if not self.database_adapter.does_table_exist("Plasmid"):
            self.db.create_plasmid_table()
            print("Tabelle 'Plasmid' wurde erstellt.")


    def insert_metadaten(self):
        file_path=self.select_file()
        if file_path:
            self.importer=ExcelImporter(self.database_adapter,file_path)
            self.importer.import_data()
        else:
            print("Keine Datei ausgewählt.")


    def select_file(self):
        root = tk.Tk()
        root.withdraw()  # Verstecken Sie das Hauptfenster
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
        return file_path        
    

    def select_all_from_plasmid(self):
        print("_______________Plasmid__________")
        with self.db as conn:
            rows = conn.execute("SELECT * FROM Plasmid").fetchall()
            for row in rows:
                print(row)
   
    def delete_plasmid(self, plasmid_nr):
        with self.db as conn:
            # SQL-Abfrage, um das Plasmid zu löschen
            cursor = conn.execute("DELETE FROM Plasmid WHERE plasmid_nr = ?", (plasmid_nr,))
            
            # Überprüfen, ob Zeilen gelöscht wurden
            if cursor.rowcount > 0:
                print(f"Plasmid mit der Nummer {plasmid_nr} wurde gelöscht.")
            else:
                print(f"Kein Plasmid mit der Nummer {plasmid_nr} gefunden.")



   