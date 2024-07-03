# Sliding Rail Ansteuerung der Haltepunkte

- Ansteuerung vom Ende bei den Klebepunkten
- Ansteuerung der Deckelabschraubestation
- Ansteurung Ende mit Zentrifuge


## aktueller Stand 03.07.24

Sliding Rail läuft per TeachIn in mehreren Stufen von Start position zum Lasercutter zur Zentrifuge und dann zum Mülleimer
Reihenfolge der TeachIns : RailStarttoLC
                           RailKPtoFuge
                           FugetoMuell
man muss die TeachIns noch mit Zwischenschritten in einem Python Code aneinanderreihen
