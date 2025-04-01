import os
import math
import random
from PIL import Image, ImageDraw
from datetime import datetime


# === Konfiguration ===
BILDER_ORDNER = "bilder"
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
KARTEN_ORDNER = f"cards_output_{timestamp}"
# SYMBOL_GROESSE = 200
KARTEN_GROESSE = 1100

# === Lade Symbole ===
def lade_symbole():
    dateien = [f for f in os.listdir(BILDER_ORDNER) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    symbole = [os.path.join(BILDER_ORDNER, f) for f in dateien]
    print(f"🔍 Gefundene Bilder ({len(symbole)}):")
    for s in symbole:
        print("   -", s)
    return symbole

# === Prüfe Primzahl ===
def ist_primzahl(n):
    if n < 2: return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0: return False
    return True

# === Bestimme maximale gültige Symbolanzahl ===
def bestimme_max_n(symbole_anzahl):
    for n in range(symbole_anzahl, 1, -1):
        if ist_primzahl(n - 1) and n * (n - 1) + 1 <= symbole_anzahl:
            return n
    return None

# === Erzeuge mathematisch gültige Dobble-Karten ===
def generiere_dobble_karten(n):
    q = n - 1
    symbole = list(range(n * q + 1))
    karten = []

    # Erste Karte
    karten.append([0] + [i + 1 for i in range(q)])

    # q Karten
    for i in range(1, q + 1):
        karte = [0]
        for j in range(1, q + 1):
            karte.append(q * i + j)
        karten.append(karte)

    # q^2 Karten
    for i in range(1, q + 1):
        for j in range(1, q + 1):
            karte = [i]
            for k in range(1, q + 1):
                wert = q + 1 + q * (k - 1) + ((i * (k - 1) + j - 1) % q)
                karte.append(wert)
            karten.append(karte)

    return karten

# === Erzeuge eine runde Karte mit Symbolbildern ===
def erstelle_karte_bild(symbole_pfade, symbol_indices, nummer):
    n = len(symbol_indices)
    image = Image.new("RGBA", (KARTEN_GROESSE, KARTEN_GROESSE), (255, 255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Zeichne dünnen Kreis als Rahmen
    rand_dicke = 8
    abstand_zum_rand = 50  
    draw.ellipse(
        [
            abstand_zum_rand,
            abstand_zum_rand,
            KARTEN_GROESSE - abstand_zum_rand,
            KARTEN_GROESSE - abstand_zum_rand
        ],
        outline="black",
        width=rand_dicke,
    )

    # Platzberechnung
    SYMBOL_RADIUS = (KARTEN_GROESSE // 2) - abstand_zum_rand - 20

    # Dynamische Symbolgröße basierend auf Fläche
    platz_durchmesser = SYMBOL_RADIUS * 2
    symbolfläche = (platz_durchmesser ** 2 * math.pi) / (n * 10)
    SYMBOL_GROESSE = int(math.sqrt(symbolfläche))
    SYMBOL_GROESSE = max(60, min(SYMBOL_GROESSE, 300)) 

    # Symbole platzieren
    winkel_offset = random.uniform(0, 2 * math.pi)
    for i, idx in enumerate(symbol_indices):
        symbol_path = symbole_pfade[idx % len(symbole_pfade)]
        symbol_img = Image.open(symbol_path).convert("RGBA")
        symbol_img = symbol_img.resize((SYMBOL_GROESSE, SYMBOL_GROESSE), Image.LANCZOS)

        winkel = 2 * math.pi * i / len(symbol_indices) + winkel_offset
        x = int(KARTEN_GROESSE / 2 + math.cos(winkel) * 250 - SYMBOL_GROESSE / 2)
        y = int(KARTEN_GROESSE / 2 + math.sin(winkel) * 250 - SYMBOL_GROESSE / 2)

        image.paste(symbol_img, (x, y), symbol_img)

    # Speichere als RGB für PDF-Kompatibilität
    image.convert("RGB").save(os.path.join(KARTEN_ORDNER, f"karte_{nummer+1:03}.png"))

def erstelle_pdf(karten_ordner):
    seiten_bilder = []
    dateien = sorted(f for f in os.listdir(karten_ordner) if f.endswith(".png"))

    # A4 in 300 DPI
    seitenbreite = 2480
    seitenhoehe = 3508

    # Karten pro Zeile und Spalte
    spalten = 2
    reihen = 3
    karten_pro_seite = spalten * reihen

    # Kartengröße (etwas kleiner, damit alles gut passt)
    kartenbreite = 780
    kartenhoehe = 780

    # Zwischenräume
    abstand_x = (seitenbreite - spalten * kartenbreite) // (spalten + 1)
    abstand_y = (seitenhoehe - reihen * kartenhoehe) // (reihen + 1)

    # Alle Positionen berechnen
    positionen = []
    for zeile in range(reihen):
        for spalte in range(spalten):
            x = abstand_x + spalte * (kartenbreite + abstand_x)
            y = abstand_y + zeile * (kartenhoehe + abstand_y)
            positionen.append((x, y))

    seite = None
    karten_count = 0

    for i, datei in enumerate(dateien):
        if karten_count % karten_pro_seite == 0:
            if seite:
                seiten_bilder.append(seite)
            seite = Image.new("RGB", (seitenbreite, seitenhoehe), (255, 255, 255))

        karte = Image.open(os.path.join(karten_ordner, datei)).convert("RGB")
        karte = karte.resize((kartenbreite, kartenhoehe), Image.LANCZOS)

        pos = positionen[karten_count % karten_pro_seite]
        seite.paste(karte, pos)

        karten_count += 1

    if seite:
        seiten_bilder.append(seite)

    if seiten_bilder:
        pdf_pfad = os.path.join(karten_ordner, "dobble_karten_6_pro_seite.pdf")
        seiten_bilder[0].save(pdf_pfad, save_all=True, append_images=seiten_bilder[1:])
        print(f"PDF mit 6 Karten pro Seite gespeichert unter:\n{pdf_pfad}")
    else:
        print("Keine Karten gefunden für PDF-Erstellung.")

# === Hauptfunktion ===
def main():
    symbole_pfade = lade_symbole()
    anzahl_symbole = len(symbole_pfade)

    max_n = bestimme_max_n(anzahl_symbole)
    if max_n is None:
        print("Nicht genug Bilder oder keine gültige Symbolanzahl gefunden.")
        return

    benoetigte_symbole = max_n * (max_n - 1) + 1
    print(f"Es werden {benoetigte_symbole} Bilder genutzt für {max_n} Symbole pro Karte.")

    karten_indices = generiere_dobble_karten(max_n)
    os.makedirs(KARTEN_ORDNER, exist_ok=True)

    for i, karte in enumerate(karten_indices):
        erstelle_karte_bild(symbole_pfade, karte, i)

    print(f"{len(karten_indices)} Karten wurden erstellt mit {max_n} Symbolen pro Karte.")

    erstelle_pdf(KARTEN_ORDNER)

if __name__ == "__main__":
    main()
