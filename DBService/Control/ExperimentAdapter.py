import tkinter
from tkinter import filedialog
from DBService.Control.DatabaseConnection import DatabaseConnection
from DBService.Control.DatabaseAdapter import DatabaseAdapter
from DBService.Control.ExperimentImporter import ExperimentImporter
from DBService.Control.LaborantAdapter import LaborantAdapter
from DBService.Model.Experiment import Experiment
from DBService.Model.Experimente import Experimente
from DBService.Control.TubeAdapter import TubeAdapter


class ExperimentAdapter:
    def __init__(self, db):
        self.experiment_importer = None
        self.db = db
        # self.db = DatabaseConnection("laborstreet_management")
        self.database_adapter = DatabaseAdapter(self.db)
        self.ensure_tables_exist()
        self.laborant_adapter = LaborantAdapter(self.db)

    def ensure_tables_exist(self):
        if not self.database_adapter.does_table_exist("Laborant"):
            self.db.create_laborant_table()
            print("Tabelle 'Laborant' wurde erstellt.")

        if not self.database_adapter.does_table_exist("GlobalIDs"):
            self.db.create_global_ids_table()
            print("Tabelle 'GlobalIDs' wurde erstellt.")

        if not self.database_adapter.does_table_exist("Tubes"):
            self.db.create_tubes_table()
            print("Tabelle 'Tubes' wurde erstellt.")

        if not self.database_adapter.does_table_exist("Experiment"):
            self.db.create_experiment_table()
            print("Tabelle 'Experiment' wurde erstellt.")

    def add_experiment(self, name, vorname, anz_tubes, anz_plasmid, datum, exp_id_param):
        # if anz_tubes % 2 != 0:
        #     print("Die Anzahl der Tubes muss eine gerade Zahl sein. Das Experiment wird nicht hinzugefügt.")
        #     return None
        # self.update_global_id(anz_tubes)
        if self.laborant_adapter.does_laborant_exist(name):
            print(f"Ein Laborant mit dem Namen {name} existiert.")
        else:
            self.laborant_adapter.add_laborant(name, vorname)

            print(f"Kein Laborant mit dem Namen {name} gefunden.")
        exp_anzahl = self.laborant_adapter.get_experiment_count_for_laborant(name)
        if exp_anzahl is not None:
            print("Experiments_anzahl: " + str(exp_anzahl))
        else:
            print("Kein Laborant mit dem Namen " + name + " gefunden.")

        if not exp_id_param:
            exp_id = f"{name}{exp_anzahl + 1}{datum}"
        else:
            exp_id = exp_id_param

        with self.db as conn:
            cursor = conn.execute('SELECT COUNT(*) FROM Experiment WHERE exp_id = ?', (exp_id,))
            exists = cursor.fetchone()[0] > 0

            if exists:
                conn.execute('''
                        UPDATE Experiment
                        SET name = ?, vorname = ?, anz_tubes = ?, anz_plasmid = ?, datum = ?
                        WHERE exp_id = ?
                    ''', (name, vorname, anz_tubes, anz_plasmid, datum, exp_id))
                print(f"Experiment mit ID {exp_id} wurde aktualisiert.")
            else:
                conn.execute('''
                        INSERT INTO Experiment (exp_id, name, vorname, anz_tubes, anz_plasmid, datum)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (exp_id, name, vorname, anz_tubes, anz_plasmid, datum))
                print(f"Experiment mit ID {exp_id} wurde hinzugefügt.")

                # Erhöhe anz_exp um 1 für den spezifischen Laboranten
                conn.execute('''
                        UPDATE Laborant
                        SET anz_exp = anz_exp + 1
                        WHERE name = ?
                    ''', (name,))
                print(f"Experimentanzahl für Laborant {name} wurde um 1 erhöht.")

        return exp_id
    def get_global_id(self):
        with self.db as conn:
            cursor = conn.execute("SELECT global_id FROM GlobalIDs")
            result = cursor.fetchone()
            if result and result[0] is not None:
                return result[0]
            else:
                return 0

    def update_global_id(self,anzahl_neue_tubes):
        current_id = self.get_global_id()
        new_id = current_id + int(anzahl_neue_tubes)
        with self.db as conn:
            # Überprüfen, ob ein Eintrag vorhanden ist
            cursor = conn.execute("SELECT COUNT(*) FROM GlobalIDs")
            exists = cursor.fetchone()[0] > 0

            if exists:
                # Aktualisiere den vorhandenen Eintrag
                conn.execute("UPDATE GlobalIDs SET global_id = ?", (new_id,))
            else:
                # Füge den ersten Eintrag hinzu
                conn.execute("INSERT INTO GlobalIDs (global_id) VALUES (?)", (new_id,))

            return new_id
    def get_experiment_by_id(self, exp_id):
        with self.db as conn:
            cursor = conn.execute('SELECT * FROM Experiment WHERE exp_id = ?', (exp_id,))
            result = cursor.fetchone()

            if result:
                experiment = Experiment(exp_id=result[0], name=result[1], vorname=result[2], anz_tubes=result[3],
                                         anz_plasmid=result[4], datum=result[5],video_id=result[6],anz_fehler=result[7],bemerkung=result[8])
                return experiment
            else:
                print(f"Kein Experiment mit der ID {exp_id} gefunden.")
                return(f"Kein Experiment mit der ID {exp_id} gefunden.")

                # return None

    def available_qrcode(self, exp_id, tubes_required):
        try:
            # von = self.get_latest_tube()
            von = self.get_global_id()

            anz_tubes_exp_id = self.get_anz_tubes_exp_id(exp_id)
            last = self.get_latest_tube_by_exp_id(exp_id)
            print(f"last:{last}")
            bis = von + abs(last - anz_tubes_exp_id)
            print(f"bis:{bis}")
            list_of_tubes = []
            if bis is not None and bis >= von:
                for x in range(von + 1, bis + 1):
                    list_of_tubes.append(x)
                    print(f"{x:06d}")
                return list_of_tubes
        except Exception as ex:
            return []
    def get_latest_tube(self):
        try:
            with self.db as conn:
                # print(f"Suche nach dem neuesten Tube für Experiment-ID: {exp_id}")
                print(f"Suche nach dem neuesten Tube für Experiment")
                cursor=conn.execute("SELECT COUNT(*) FROM Tubes")
                latest_tube = cursor.fetchone()
                if not latest_tube:
                    # print(f"Kein Tube für Experiment-ID {exp_id} gefunden.")
                    print(f"Kein Tube für Experiment gefunden.")

                    return 0
                print(f"all tubes von :{latest_tube[0]}")
                return latest_tube[0]
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")
            return None

    def get_anz_tubes_exp_id(self, exp_id):
        try:
            with self.db as conn:
                cursor = conn.execute('SELECT anz_tubes FROM Experiment WHERE exp_id = ?', (exp_id,))
                result = cursor.fetchone()

                if result:
                    # Die Anpassung hier: nur die Anzahl der Tubes zurückgeben
                    anz_tubes = result[0]
                    print(f"anz_tubes:von {exp_id}  ist:{anz_tubes}")
                    return anz_tubes
                else:
                    print(f"Kein Experiment mit der ID {exp_id} gefunden.")
                    return None
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")
            return None
    def get_latest_tube_by_exp_id(self, exp_id):
        try:
            with self.db as conn:
                print(f"Suche nach dem neuesten Tube für Experiment-ID: {exp_id}")
                cursor = conn.execute("SELECT * FROM Tubes WHERE exp_id = ? ORDER BY qr_code DESC LIMIT 1", (exp_id,))
                latest_tube = cursor.fetchone()
                if not latest_tube:
                    print(f"Kein Tube für Experiment-ID {exp_id} gefunden.")
                    return 0

                formatted_qr_code = f"{latest_tube[0]:06d}"
                tube_dict = {
                    'qr_code': formatted_qr_code,
                    'probe_nr': latest_tube[1],
                    'exp_id': latest_tube[2],
                    'plasmid_nr': latest_tube[3]
                }
                print(f"latest_tube{latest_tube[1]}")
                return latest_tube[1]
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")
            return None




    # def available_qrcode(self,exp_id):
    #     try:
    #         von=self.get_latest_tube_by_exp_id(exp_id)
    #         print("available")
    #         bis=self.get_anz_tubes_exp_id(exp_id)
    #         print(bis)
    #         list_of_tubes = []
    #         if bis is not None and bis >= von:
    #             for x in range(von + 1, bis + 1):
    #                 list_of_tubes.append(x)
    #                 print(f"{x:06d}")
    #             return list_of_tubes
    #     except Exception as ex:
    #         return []


    def get_all_experiments(self):

        with self.db as conn:
            cursor = conn.execute('SELECT * FROM Experiment')
            experiments = cursor.fetchall()

            # Optional: Konvertiere die Ergebnisse in eine Liste von Experiment-Objekten
            experiment_list = []
            for exp in experiments:
                experiment_obj = Experiment(exp_id=exp[0], name=exp[1], vorname=exp[2], anz_tubes=exp[3],anz_plasmid=exp[4],
                                            video_id=exp[5], datum=exp[6], anz_fehler=exp[7], bemerkung=exp[8])
                experiment_list.append(experiment_obj)

            return experiment_list

    def delete_all_experiment(self):
        with self.db as conn:
            # alle Einträge in der Tabelle Experiment löschen
            conn.execute('DELETE FROM Experiment')
            print("Alle Experimente wurden gelöscht.")

    def get_tubes_data_for_experiment(self, exp_id):
        try:
            with self.db as conn:
                cursor = conn.execute('''
                    SELECT 
                        t.probe_nr, 
                        t.qr_code, 
                        t.plasmid_nr, 
                        p.vektor, 
                        p."insert", 
                        e.name, 
                        e.vorname, 
                        e.exp_id, 
                        e.datum, 
                        e.anz_fehler
                    FROM Tubes t
                    INNER JOIN Plasmid p ON t.plasmid_nr = p.plasmid_nr
                    INNER JOIN Experiment e ON t.exp_id = e.exp_id
                    WHERE t.exp_id = ?
                ''', (exp_id,))
                tubes_data = cursor.fetchall()

                tubes_data_list = []
                for data in tubes_data:
                    tube_data_dict = {
                        'probe_nr': data[0],
                        'qr_code': f"{data[1]:06d}",
                        'plasmid_nr': data[2],
                        'vektor': data[3],
                        'insert': data[4],
                        'name': data[5],
                        'vorname': data[6],
                        'exp_id': data[7],
                        'datum': data[8],
                        'anz_fehler': data[9]
                    }
                    tubes_data_list.append(tube_data_dict)
                return tubes_data_list
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")
            return []

    def get_probe_numbers_by_plasmid_for_experiment(self, exp_id):
        try:
            with self.db as conn:
                # Überprüfen, ob das Experiment existiert
                cursor = conn.execute("SELECT COUNT(*) FROM Experiment WHERE exp_id = ?", (exp_id,))
                if cursor.fetchone()[0] == 0:
                    print(f"Kein Experiment mit der ID {exp_id} gefunden.")
                    return {}

                # SQL-Abfrage, um die Daten zu holen
                cursor = conn.execute('''
                    SELECT 
                        t.plasmid_nr, 
                        t.probe_nr
                    FROM Tubes t
                    WHERE t.exp_id = ?
                ''', (exp_id,))
                tubes_data = cursor.fetchall()

                plasmid_probe_dict = {}
                for plasmid_nr, probe_nr in tubes_data:
                    if plasmid_nr not in plasmid_probe_dict:
                        plasmid_probe_dict[plasmid_nr] = []
                    plasmid_probe_dict[plasmid_nr].append(probe_nr)

                return plasmid_probe_dict
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")
            return {}

    def delete_experiment(self, exp_id):
        try:
            print("deleting exp")
            with self.db as conn:
                # Überprüfe, ob das Experiment existiert
                cursor = conn.execute("SELECT COUNT(*) FROM Experiment WHERE exp_id = ?", (exp_id,))
                experiment_exists = cursor.fetchone()[0] > 0

                if not experiment_exists:
                    print(f"Kein Experiment mit ID {exp_id} gefunden.")
                    return

                # Überprüfe, ob das Experiment Tubes hat
                cursor = conn.execute("SELECT COUNT(*) FROM Tubes WHERE exp_id = ?", (exp_id,))
                tube_count = cursor.fetchone()[0]

                if tube_count > 0:
                    # Löschen aller Tubes, die mit dem Experiment verknüpft sind
                    conn.execute("DELETE FROM Tubes WHERE exp_id = ?", (exp_id,))
                    print(f"Alle Tubes für Experiment-ID {exp_id} wurden gelöscht.")
                else:
                    print(f"Keine Tubes für Experiment-ID {exp_id} gefunden.")

                # Löschen des Experiments
                conn.execute("DELETE FROM Experiment WHERE exp_id = ?", (exp_id,))
                print(f"Experiment mit ID {exp_id} wurde gelöscht.")

        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")
            
    def insert_experiment_data(self,file_path):
        # file_path = self.select_file()

        if file_path:
            # eine Instanz des ExperimentImporters mit dem ausgewählten Dateipfad
            self.experiment_importer = ExperimentImporter(file_path,)
            #die Methode import_data auf, um die Daten zu importieren
            return self.experiment_importer.import_data()
        else:
            return "Keine Datei ausgewählt."
        
    def select_file(self):
        root = tkinter.Tk()
        root.withdraw()  # Verstecken Sie das Hauptfenster
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
        return file_path