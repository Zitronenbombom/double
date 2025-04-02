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

| Symbole pro Karte (`n`) | Benötigte Bilder | Gültig (`n - 1` ist prim?)       |
|-------------------------|------------------|----------------------------------|
| 3                       | 7                | (2 ist prim)                   |
| 4                       | 13               | (3 ist prim)                   |
| 5                       | 21               | (4 ist keine Primzahl)         |
| 6                       | 31               | (5 ist prim)                   |
| 7                       | 43               | (6 ist keine Primzahl)         |
| 8                       | 57               | (7 ist prim)                   |
| 9                       | 73               | (8 ist keine Primzahl)         |
| 10                      | 91               | (9 ist prim)                   |

> Je mehr Bilder im `bilder/`-Ordner, desto mehr Symbole pro Karte sind möglich – **aber nur für gültige Werte** nach dieser Regel.