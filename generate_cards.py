import os
import math
import random
from PIL import Image, ImageDraw
from datetime import datetime

# === Konfiguration ===
BILDER_ORDNER = "bilder"
BASIS_ORDNER = "cards_output"
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
KARTEN_ORDNER = os.path.join(BASIS_ORDNER, timestamp)
KARTEN_GROESSE = 2000  # Pixel

# === Lade Symbole ===
def lade_symbole():
    dateien = [f for f in os.listdir(BILDER_ORDNER) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    symbole = [os.path.join(BILDER_ORDNER, f) for f in dateien]
    print(f"Gefundene Bilder ({len(symbole)}):")
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
    karten = []

    karten.append([0] + [i + 1 for i in range(q)])
    for i in range(1, q + 1):
        karte = [0]
        for j in range(1, q + 1):
            karte.append(q * i + j)
        karten.append(karte)

    for i in range(1, q + 1):
        for j in range(1, q + 1):
            karte = [i]
            for k in range(1, q + 1):
                wert = q + 1 + q * (k - 1) + ((i * (k - 1) + j - 1) % q)
                karte.append(wert)
            karten.append(karte)

    return karten

# === Positionierungslogik ===
def berechne_symbolpositionen(n, radius):
    zentrum = (KARTEN_GROESSE // 2, KARTEN_GROESSE // 2)
    koordinaten = []

    if n <= 6:
        for i in range(n):
            winkel = 2 * math.pi * i / n
            x = zentrum[0] + math.cos(winkel) * radius
            y = zentrum[1] + math.sin(winkel) * radius
            koordinaten.append((x, y))

    elif 7 <= n <= 9:
        innen = 1
        außen = n - innen
        koordinaten.append(zentrum)
        for i in range(außen):
            winkel = 2 * math.pi * i / außen
            x = zentrum[0] + math.cos(winkel) * radius
            y = zentrum[1] + math.sin(winkel) * radius
            koordinaten.append((x, y))

    else:
        ringe = []
        rest = n
        ring_radien = [radius * 0.5, radius * 0.85, radius]
        ring_kapazitaet = [1, 6, 12, 18, 24]

        for r, cap in zip(ring_radien, ring_kapazitaet):
            anz = min(rest, cap)
            rest -= anz
            ringe.append((r, anz))
            if rest <= 0:
                break

        for r, anz in ringe:
            for i in range(anz):
                winkel = 2 * math.pi * i / anz
                x = zentrum[0] + math.cos(winkel) * r
                y = zentrum[1] + math.sin(winkel) * r
                koordinaten.append((x, y))

    return koordinaten

# === Erzeuge eine runde Karte mit Symbolbildern ===
def erstelle_karte_bild(symbole_pfade, symbol_indices, nummer):
    n = len(symbol_indices)
    image = Image.new("RGBA", (KARTEN_GROESSE, KARTEN_GROESSE), (255, 255, 255, 255))
    draw = ImageDraw.Draw(image)

    abstand_zum_rand = 20
    rand_dicke = max(KARTEN_GROESSE // 150, 5)

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

    SYMBOL_RADIUS = (KARTEN_GROESSE // 2) - abstand_zum_rand - 20
    platz_durchmesser = SYMBOL_RADIUS * 2
    symbolfläche = (platz_durchmesser ** 2 * math.pi) / (n * 10)
    SYMBOL_GROESSE = int(math.sqrt(symbolfläche))
    SYMBOL_GROESSE = max(60, min(SYMBOL_GROESSE, 300))

    positionen = berechne_symbolpositionen(n, SYMBOL_RADIUS * 0.65)

    for (x, y), idx in zip(positionen, symbol_indices):
        symbol_path = symbole_pfade[idx % len(symbole_pfade)]
        symbol_img = Image.open(symbol_path).convert("RGBA")
        symbol_img = symbol_img.resize((SYMBOL_GROESSE, SYMBOL_GROESSE), Image.LANCZOS)

        x = int(x - SYMBOL_GROESSE / 2)
        y = int(y - SYMBOL_GROESSE / 2)
        image.paste(symbol_img, (x, y), symbol_img)

    image.convert("RGB").save(os.path.join(KARTEN_ORDNER, f"karte_{nummer+1:03}.png"))

# === PDF mit 6 Karten pro A4-Seite ===
def erstelle_pdf(karten_ordner):
    seiten_bilder = []
    dateien = sorted(f for f in os.listdir(karten_ordner) if f.endswith(".png"))

    seitenbreite = 2480
    seitenhoehe = 3508
    seitenrand = 100

    spalten = 2
    reihen = 3
    karten_pro_seite = spalten * reihen

    verfuegbar_x = seitenbreite - 2 * seitenrand
    verfuegbar_y = seitenhoehe - 2 * seitenrand
    kartenbreite = verfuegbar_x // spalten
    kartenhoehe = verfuegbar_y // reihen

    positionen = []
    for zeile in range(reihen):
        for spalte in range(spalten):
            x = seitenrand + spalte * kartenbreite
            y = seitenrand + zeile * kartenhoehe
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
        print(f"PDF gespeichert unter:\n{pdf_pfad}")
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
    print(f"Verwendete Bilder: {benoetigte_symbole} (für {max_n} Symbole pro Karte)")

    karten_indices = generiere_dobble_karten(max_n)
    os.makedirs(KARTEN_ORDNER, exist_ok=True)

    for i, karte in enumerate(karten_indices):
        erstelle_karte_bild(symbole_pfade, karte, i)

    print(f"{len(karten_indices)} Karten erstellt.")
    print(f"Gespeichert unter: {KARTEN_ORDNER}")

    erstelle_pdf(KARTEN_ORDNER)

if __name__ == "__main__":
    main()
