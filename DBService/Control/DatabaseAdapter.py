from Model.Experiment import Experiment
from Model.Experimente import Experimente
class DatabaseAdapter:
    def __init__(self, db):
        self.db = db
        self.last_qr_code_index = 0  # Initialisieren den Zähler
   
   



    def insert_tube(self, qr_code, exp_id, plasmid_nr):
        # Überprüfen, ob die Tabelle existiert
        if not self.does_table_exist("Tubes"):
            print("Tabelle 'Tubes' existiert nicht. Sie wird erstellt.")
            self.db.create_tubes_table()
        else:
            print("Tabelle 'Tubes' existiert bereits.")

        with self.db as conn:
            # Fügen Sie das Tube in die Datenbank ein
            conn.execute('''
                INSERT INTO Tubes (qr_code, exp_id, plasmid_nr)
                VALUES (?, ?, ?)
            ''', (qr_code, exp_id, plasmid_nr))
            print(f"Tube mit QR-Code {qr_code} hinzugefügt.")
    def get_all_tubes(self):
        with self.db as conn:
            # SQL-Abfrage, um alle Einträge aus der Tubes Tabelle zu holen
            cursor = conn.execute("SELECT * FROM Tubes")
            tubes = cursor.fetchall()

            # Optional: Konvertieren Sie die Ergebnisse in eine Liste von Objekten oder Dictionaries
            tubes_list = []
            for tube in tubes:
                tube_dict = {
                    'qr_code': tube[0],
                    'exp_id': tube[1],
                    'plasmid_nr': tube[2]
                }
                tubes_list.append(tube_dict)

            return tubes_list
    # def create_tube_qrcode_table_if_not_exists(self):
    #     if not self.does_table_exist("TubeQrcode"):
    #         with self.db as conn:
    #             conn.execute('''
    #                 CREATE TABLE IF NOT EXISTS TubeQrcode (
    #                     qr_code TEXT PRIMARY KEY,
    #                     datum TEXT
    #                 )
    #             ''')
    #         print("Tabelle 'TubeQrcode' wurde erstellt.")
    def drop_table_tube_qrcode(self):
        with self.db as conn:
            # Löschen der Tabelle TubeQrcode
            conn.execute("DROP TABLE IF EXISTS TubeQrcode")

    def insert_data(self, tubeQrcode):
        with self.db as conn:
            conn.execute("INSERT INTO TubeQrcode (qr_code, datum) VALUES (?, ?)", (tubeQrcode.qr_code, tubeQrcode.datum))

    def select_all_from_tubeqrcode(self):
         # Überprüfen, ob die Tabelle existiert
        if not self.does_table_exist("Tubes"):
            print("Tabelle 'Tubes' existiert nicht. Sie wird erstellt.")
            self.db.create_tubes_table()
            with self.db as conn:
                rows = conn.execute("SELECT * FROM TubeQrcode").fetchall()
                for row in rows:
                        formatted_qr_code = str(row[0]).zfill(6)
                        print((formatted_qr_code, row[1]))
        else:
            print("Tabelle 'Tubes' existiert bereits.")
       

    def get_next_qr_codes(self, count):
        with self.db as conn:
            # Abrufen der QR-Codes ab der letzten Position
            cursor = conn.execute("SELECT * FROM TubeQrcode ORDER BY qr_code LIMIT ? OFFSET ?", (count, self.last_qr_code_index))
            qr_codes = cursor.fetchall()

            # Aktualisieren Sie den Zähler
            self.last_qr_code_index += len(qr_codes)

            # Formatieren und zurückgeben der QR-Codes
            formatted_qr_codes = [(str(row[0]).zfill(6), row[1]) for row in qr_codes]
            return formatted_qr_codes

    def insert_plasmid(self, plasmid):
     # Überprüfen, ob die Tabelle existiert
        if not self.does_table_exist("Plasmid"):
            print("Tabelle 'Plasmid' existiert nicht. Sie wird erstellt.")
            self.db.create_plasmid_table()
        else:
            print("Tabelle 'Plasmid' existiert bereits.")

        with self.db as conn:
            # Überprüfen und konvertieren Sie den Datentyp von plasmid.name
            name = str(plasmid.name) if plasmid.name is not None else None
            
            # Konvertieren Sie Datumswerte in Strings
            datum_maxi = plasmid.datum_maxi.strftime('%Y-%m-%d') if plasmid.datum_maxi is not None else None
            konstruktion_datum = plasmid.konstruktion_datum.strftime('%Y-%m-%d') if plasmid.konstruktion_datum is not None else None
            
            # Fügen Sie das Plasmid in die Datenbank ein
            conn.execute('''
            INSERT INTO Plasmid (plasmid_nr, vektor, "insert", sequenz_nr, name, datum_maxi, quelle, konstruktion_datum)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (plasmid.plasmid_nr, plasmid.vektor, plasmid.insert, plasmid.sequenz_nr, name, datum_maxi, plasmid.quelle, konstruktion_datum))

    def add_experiment(self, exp_id, name, vorname, anz_tubes, datum):
        # Überprüfen, ob die Tabelle existiert
        if not self.does_table_exist("Experiment"):
            print("Tabelle 'Experiment' existiert nicht. Sie wird erstellt.")
            self.db.create_experiment_table()

        with self.db as conn:
            # Überprüfen, ob das Experiment bereits existiert
            cursor = conn.execute('SELECT COUNT(*) FROM Experiment WHERE exp_id = ?', (exp_id,))
            exists = cursor.fetchone()[0] > 0

            if exists:
                # Aktualisiere das vorhandene Experiment
                conn.execute('''
                    UPDATE Experiment
                    SET name = ?, vorname = ?, anz_tubes = ?, datum = ?
                    WHERE exp_id = ?
                ''', (name, vorname, anz_tubes, datum, exp_id))
                print(f"Experiment mit ID {exp_id} wurde aktualisiert.")
            else:
                # Füge ein neues Experiment hinzu
                conn.execute('''
                    INSERT INTO Experiment (exp_id, name, vorname, anz_tubes, datum)
                    VALUES (?, ?, ?, ?, ?)
                ''', (exp_id, name, vorname, anz_tubes, datum))
                print(f"Experiment mit ID {exp_id} wurde hinzugefügt.")

    def get_experiments(self):
        with self.db as conn:
            cursor = conn.execute('SELECT * FROM Experiment')
            experiments = cursor.fetchall()

            # Optional: Konvertieren Sie die Ergebnisse in eine Liste von Experiment-Objekten
            experiment_list = []
            for exp in experiments:
                experiment_obj = Experimente(exp_id=exp[0], name=exp[1], vorname=exp[2], anz_tubes=exp[3], datum=exp[4])
                experiment_list.append(experiment_obj)

            return experiment_list       
        
   
    def insert_experiment(self, experiment):
        if not self.does_table_exist("Experiment"):
            print("Tabelle 'Experiment' existiert nicht. Sie wird erstellt.")
            self.db.create_experiment_table()
        with self.db as conn:
            # video_id in einen String
            video_id_str = str(experiment.video_id)

            # konvert das Datum in einen String im Format YYYY-MM-DD
            datum_str = experiment.datum.strftime('%Y-%m-%d') if experiment.datum is not None else None

            # Überprüfen, ob das Experiment bereits existiert
            cursor = conn.execute('SELECT COUNT(*) FROM Experiment WHERE exp_id = ?', (experiment.exp_id,))
            exists = cursor.fetchone()[0] > 0

            if exists:
                # Aktualisiere das vorhandene Experiment
                conn.execute('''
                    UPDATE Experiment
                    SET name = ?, vorname = ?, anz_tubes = ?, video_id = ?, datum = ?, anz_fehler = ?, bemerkung = ?
                    WHERE exp_id = ?
                ''', (experiment.name, experiment.vorname, experiment.anz_tubes, video_id_str, datum_str, experiment.anz_fehler, experiment.bemerkung, experiment.exp_id))
            else:
                # ein neues Experiment einfügen
                conn.execute('''
                    INSERT INTO Experiment (exp_id, name, vorname, anz_tubes, video_id, datum, anz_fehler, bemerkung)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (experiment.exp_id, experiment.name, experiment.vorname, experiment.anz_tubes, video_id_str, datum_str, experiment.anz_fehler, experiment.bemerkung))
   
    def delete_all_experiments(self):
        with self.db as conn:
            # alle Einträge in der Tabelle Experiment löschen
            conn.execute('DELETE FROM Experiment')
            print("Alle Experimente wurden gelöscht.")


            
    def select_all_from_plasmid(self):
        print("_______________Plasmid__________")
        with self.db as conn:
            rows = conn.execute("SELECT * FROM Plasmid").fetchall()
            for row in rows:
                print(row)

    def get_all_experiments(self):
        with self.db as conn:
            cursor = conn.execute('SELECT * FROM Experiment')
            experiments = cursor.fetchall()

            # Optional: Konvertiere die Ergebnisse in eine Liste von Experiment-Objekten
            experiment_list = []
            for exp in experiments:
                experiment_obj = Experiment(exp_id=exp[0], name=exp[1], vorname=exp[2], anz_tubes=exp[3], video_id=exp[4], datum=exp[5], anz_fehler=exp[6], bemerkung=exp[7])
                experiment_list.append(experiment_obj)

            return experiment_list
        
    def does_table_exist(self, table_name):
        with self.db as conn:
            result = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,)).fetchone()
            return result is not None