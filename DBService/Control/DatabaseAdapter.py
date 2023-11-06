

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




            
    def select_all_from_plasmid(self):
        print("_______________Plasmid__________")
        with self.db as conn:
            rows = conn.execute("SELECT * FROM Plasmid").fetchall()
            for row in rows:
                print(row)

    def does_table_exist(self, table_name):
        with self.db as conn:
            result = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,)).fetchone()
            return result is not None