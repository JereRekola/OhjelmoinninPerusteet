# Copyright (c) 2025 Jere Rekola
# License: MIT

from datetime import datetime, date
from typing import List, Dict
import csv
from collections import defaultdict

def lue_data(tiedoston_nimi: str) -> List[Dict]:
    """Lukee CSV-tiedoston ja palauttaa listan riveistä sanakirjoina."""
    rivit: List[Dict] = []
    with open(tiedoston_nimi, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for rivi in reader:
            # if varmistaa ettei tyhjiä rivejä lisätä
            if rivi and rivi["Aika"]:
                rivit.append(rivi)
    return rivit

def muunna_aika(aika_str: str) -> datetime:
    """Muuntaa ISO-muotoisen aikaleiman datetime-olioksi."""
    if isinstance(aika_str, str) and len(aika_str) > 0:
        return datetime.fromisoformat(aika_str)
    else:
        # jos aikaleima puuttuu, palautetaan oletus
        return datetime(1900, 1, 1)

def wh_to_kwh(arvo_wh: str) -> float:
    """Muuntaa Wh-arvon kWh-arvoksi (float)."""
    if arvo_wh.strip() == "":
        return 0.0
    else:
        return float(arvo_wh) / 1000.0

def ryhmittele_paivittain(rivit: List[Dict]) -> Dict[date, Dict[str, float]]:
    """Ryhmittelee rivit päiväkohtaisesti ja laskee kulutuksen ja tuotannon vaiheittain."""
    paivat: Dict[date, Dict[str, float]] = defaultdict(lambda: defaultdict(float))
    for rivi in rivit:
        aika = muunna_aika(rivi["Aika"])
        paiva = aika.date()

        # if varmistaa että rivillä on oikea päivämäärä
        if paiva.year > 1900:
            # Kulutus
            if "Kulutus vaihe 1 Wh" in rivi:
                paivat[paiva]["kulutus1"] += wh_to_kwh(rivi["Kulutus vaihe 1 Wh"])
            if "Kulutus vaihe 2 Wh" in rivi:
                paivat[paiva]["kulutus2"] += wh_to_kwh(rivi["Kulutus vaihe 2 Wh"])
            if "Kulutus vaihe 3 Wh" in rivi:
                paivat[paiva]["kulutus3"] += wh_to_kwh(rivi["Kulutus vaihe 3 Wh"])
            # Tuotanto
            if "Tuotanto vaihe 1 Wh" in rivi:
                paivat[paiva]["tuotanto1"] += wh_to_kwh(rivi["Tuotanto vaihe 1 Wh"])
            if "Tuotanto vaihe 2 Wh" in rivi:
                paivat[paiva]["tuotanto2"] += wh_to_kwh(rivi["Tuotanto vaihe 2 Wh"])
            if "Tuotanto vaihe 3 Wh" in rivi:
                paivat[paiva]["tuotanto3"] += wh_to_kwh(rivi["Tuotanto vaihe 3 Wh"])
    return paivat

def muotoile_luku(arvo: float) -> str:
    """Muotoilee luvun kahden desimaalin tarkkuudella ja pilkulla desimaalierottimena."""
    if arvo < 0:
        arvo = 0.0  # varmistetaan ettei negatiivisia arvoja tulostu
    return f"{arvo:.2f}".replace(".", ",")

def viikonpaiva_suomeksi(paiva: date) -> str:
    """Palauttaa viikonpäivän suomeksi annetulle päivämäärälle."""
    nimet = ["maanantai", "tiistai", "keskiviikko", "torstai", "perjantai", "lauantai", "sunnuntai"]
    if 0 <= paiva.weekday() <= 6:
        return nimet[paiva.weekday()]
    else:
        return "tuntematon"

def tulosta_taulukko(paivat: Dict[date, Dict[str, float]]) -> None:
    """Tulostaa päiväkohtaiset kulutus- ja tuotantotiedot taulukkona käyttäjäystävällisessä muodossa."""
    print(f"{'Päivä':<12}{'Pvm':<12}{'Kulutus [kWh]':<28}{'Tuotanto [kWh]':<28}")
    print(f"{'':<12}{'(pv.kk.vvvv)':<12}{'v1':>8}{'v2':>8}{'v3':>8}{'':>4}{'v1':>8}{'v2':>8}{'v3':>8}")
    print("-" * 75)

    for paiva in sorted(paivat.keys()):
        viikonpaiva = viikonpaiva_suomeksi(paiva)
        pvm_str = f"{paiva.day}.{paiva.month}.{paiva.year}"

        # if varmistaa että päivällä on dataa
        if paivat[paiva]:
            print(f"{viikonpaiva:<12}{pvm_str:<12}"
                  f"{muotoile_luku(paivat[paiva]['kulutus1']):>8}"
                  f"{muotoile_luku(paivat[paiva]['kulutus2']):>8}"
                  f"{muotoile_luku(paivat[paiva]['kulutus3']):>8}"
                  f"{'':>4}"
                  f"{muotoile_luku(paivat[paiva]['tuotanto1']):>8}"
                  f"{muotoile_luku(paivat[paiva]['tuotanto2']):>8}"
                  f"{muotoile_luku(paivat[paiva]['tuotanto3']):>8}")
        else:
            print(f"{viikonpaiva:<12}{pvm_str:<12} Ei dataa")

def main() -> None:
    """Ohjelman pääfunktio: lukee datan, laskee yhteenvedot ja tulostaa raportin."""
    tiedoston_nimi = "viikko42.csv"
    rivit = lue_data(tiedoston_nimi)
    if len(rivit) == 0:
        print("Tiedosto on tyhjä tai ei sisältänyt dataa.")
    else:
        paivat = ryhmittele_paivittain(rivit)
        if len(paivat) > 0:
            tulosta_taulukko(paivat)
        else:
            print("Ei löytynyt päiväkohtaista dataa.")

if __name__ == "__main__":
    main()
