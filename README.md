# double

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