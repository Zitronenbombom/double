# double
## Installation


1. **Download**  
   Lade das Projekt herunter:  
   - Entweder über **Git**:  
     ```bash
     git clone https://github.com/dein-user/dein-repo.git
     ```
   - Oder einfach als **ZIP-Datei herunterladen und entpacken**

2. **Ordner vorbereiten**  
   - Erstelle im Projektverzeichnis einen Ordner namens **`bilder/`**
   - Füge dort deine gewünschten **Symbol-Bilder** ein (`.png`, `.jpg`, `.jpeg`)

3. **Programm starten**  
   - **Doppelklicke** auf `generate_cards.exe`
   - Die generierten Karten und die PDF findest du dann unter:  
     `cards_output/YYYY-MM-DD_HH-MM-SS/`

4. **Drucken (optional)**  
   - Die Datei `dobble_karten_6_pro_seite.pdf` enthält 6 Karten pro A4-Seite  

---

## Hinweise

- Je mehr Bilder du in `bilder/` hast, desto mehr Symbole pro Karte sind möglich.
- Das Spiel basiert auf dem **Dobble-Prinzip**:  
  Jede Kartenpaarung hat **genau ein gemeinsames Symbol**.
- Nur `.png`, `.jpg`, `.jpeg`-Dateien werden unterstützt.




## Gültige Symbolanzahlen für Dobble-Karten

Damit das Dobble-Prinzip funktioniert (jede Kartenpaarung hat **genau ein gemeinsames Symbol**), gelten folgende mathematische Regeln:

- Formel: **benötigte Bilder = n × (n - 1) + 1**
- **n - 1 muss eine Primzahl** sein

| Symbole pro Karte (`n`) | Benötigte Bilder | Gültig (`n - 1` ist prim?)       | Gültig |
|-------------------------|------------------|----------------------------------|--------|
| 3                       | 7                | (2 ist prim)                     | ja     |
| 4                       | 13               | (3 ist prim)                     | ja     |
| 5                       | 21               | (4 ist keine Primzahl)           | nein   |
| 6                       | 31               | (5 ist prim)                     | ja     |
| 7                       | 43               | (6 ist keine Primzahl)           | nein   |
| 8                       | 57               | (7 ist prim)                     | ja     |
| 9                       | 73               | (8 ist keine Primzahl)           | nein   |
| 10                      | 91               | (9 ist keine Primzahl)           | nein   |
| 11                      | 111              | (10 ist keine Primzahl)          | nein   |
| 12                      | 133              | (11 ist prim)                    | ja     |
| 13                      | 157              | (12 ist keine Primzahl)          | nein   |
| 14                      | 183              | (13 ist prim)                    | ja     |


> Je mehr Bilder im `bilder/`-Ordner, desto mehr Symbole pro Karte sind möglich – **aber nur für gültige Werte** nach dieser Regel.