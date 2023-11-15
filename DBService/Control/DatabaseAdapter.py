from Model.Experiment import Experiment
class DatabaseAdapter:
    def __init__(self, db):
        self.db = db

    def insert_data(self, tubeQrcode):
        with self.db as conn:
            conn.execute("INSERT INTO TubeQrcode (qr_code, datum) VALUES (?, ?)", (tubeQrcode.qr_code, tubeQrcode.datum))

    def select_all_from_tubeqrcode(self):
        with self.db as conn:
            rows = conn.execute("SELECT * FROM TubeQrcode").fetchall()
            for row in rows:
                    formatted_qr_code = str(row[0]).zfill(6)
                    print((formatted_qr_code, row[1]))

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


   
    def insert_experiment(self, experiment):
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