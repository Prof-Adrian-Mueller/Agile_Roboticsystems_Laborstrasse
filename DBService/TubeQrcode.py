


__author__ = 'Wissam Alamareen'
__date__ = '01/12/2023'
__version__ = '1.0'
__last_changed__ = '18/12/2023'
class TubeQrcode:
    def __init__(self, qr_code, datum ):
        self.qr_code = qr_code  # QR-Code
        self.datum = datum      # Datum der Erstellung
     

    def __str__(self):
        return f"QR-Code: {self.qr_code}, Datum: {self.datum}"