from DBService.Control.DatabaseAdapter import DatabaseAdapter


class TrackingLogAdapter:
    def __init__(self,db):
        self.db=db
        self.database_adapter = DatabaseAdapter(self.db)
        self.ensure_tables_exist()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Hier könnten Sie ggf. Ressourcen freigeben oder Aufräumarbeiten durchführen
        pass

    def ensure_tables_exist(self):
        if not self.database_adapter.does_table_exist("TrackingLog"):
            self.db.create_tracking_log_table()
            print("Tabelle 'TrackingLog' wurde erstellt.")

    def insert_tracking_log(self, probe_nr, Startstation, Startzeit, Zielstation, Zielzeit, Dauer, Zeitstempel):
        try:
            with self.db as conn:
                conn.execute('''
                    INSERT INTO TrackingLog (probe_nr, Startstation, Startzeit, Zielstation, Zielzeit, Dauer, Zeitstempel)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (probe_nr, Startstation, Startzeit, Zielstation, Zielzeit, Dauer, Zeitstempel))
                print(f"Tracking-Log für Probe Nr. {probe_nr} hinzugefügt.")
        except Exception as e:
            print(f"Fehler beim Einfügen des Tracking-Logs: {e}")

    def get_tracking_logs_by_probe_nr(self, probe_nr):
        try:
            with self.db as conn:
                cursor = conn.execute('''
                    SELECT * FROM TrackingLog WHERE probe_nr = ?
                ''', (probe_nr,))
                tracking_logs = cursor.fetchall()
                return tracking_logs
        except Exception as e:
            print(f"Fehler beim Abrufen der Tracking-Logs: {e}")
            return None