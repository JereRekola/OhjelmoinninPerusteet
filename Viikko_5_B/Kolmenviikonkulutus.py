# Copyright (c) 2025 Jere Rekola
# License: MIT

from datetime import datetime, date
from typing import List, Dict, Tuple
import csv
from collections import defaultdict

def lue_data(tiedoston_nimi: str) -> List[Dict[str, str]]:
    """Lukee CSV-tiedoston ja palauttaa listan riveistä sanakirjoina."""
    rivit: List[Dict[str, str]] = []
    with open(tiedoston_nimi, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for rivi in reader:
            if rivi and rivi.get("Aika"):  # if: ohitetaan tyhjät rivit
                rivit.append({k.strip(): v.strip() for k, v in rivi.items()})
    return rivit

def muunna_aika(aika_str: str) -> datetime:
    """Muuntaa ISO-muotoisen aikaleiman datetime-olioksi."""
    return datetime.fromisoformat(aika_str)

def wh_to_kwh(arvo_wh: str) -> float:
    """Muuntaa Wh-arvon kWh-arvoksi (float)."""
    try:
        return float(arvo_wh) / 1000.0
    except ValueError:
        return 0.0

def muotoile_luku(arvo: float) -> str:
    """Muotoilee luvun kahden desimaalin tarkkuudella ja pilkulla desimaalierottimena."""
    return f"{arvo:.2f}".replace(".", ",")

def viikonpaiva_suomeksi(paiva: date) -> str:
    """Palauttaa viikonpäivän suomeksi annetulle päivämäärälle."""
    nimet = ["maanantai", "tiistai", "keskiviikko", "torstai", "perjantai", "lauantai", "sunnuntai"]
    return nimet[paiva.weekday()]

def ryhmittele_paivittain(rivit: List[Dict[str, str]]) -> Dict[date, Dict[str, float]]:
    """Ryhmittelee rivit päiväkohtaisesti ja laskee kulutuksen ja tuotannon vaiheittain."""
    paivat: Dict[date, Dict[str, float]] = defaultdict(lambda: defaultdict(float))
    for rivi in rivit:
        aika = muunna_aika(rivi["Aika"])
        paiva = aika.date()
        # Kulutus
        paivat[paiva]["kulutus1"] += wh_to_kwh(rivi["Kulutus vaihe 1 Wh"])
        paivat[paiva]["kulutus2"] += wh_to_kwh(rivi["Kulutus vaihe 2 Wh"])
        paivat[paiva]["kulutus3"] += wh_to_kwh(rivi["Kulutus vaihe 3 Wh"])
        # Tuotanto
        paivat[paiva]["tuotanto1"] += wh_to_kwh(rivi["Tuotanto vaihe 1 Wh"])
        paivat[paiva]["tuotanto2"] += wh_to_kwh(rivi["Tuotanto vaihe 2 Wh"])
        paivat[paiva]["tuotanto3"] += wh_to_kwh(rivi["Tuotanto vaihe 3 Wh"])
    return paivat

def muodosta_viikko_otsikko(viikkonro: int) -> str:
    """Muodostaa otsikon annetulle viikkonumerolle."""
    return f"Viikon {viikkonro} sähkönkulutus ja -tuotanto (kWh, vaiheittain)"

def muodosta_taulukon_otsikot() -> List[str]:
    """Palauttaa taulukon otsikkorivit raporttiin."""
    r1 = f"{'Päivä':<12}{'Pvm':<12}{'Kulutus [kWh]':<28}{'Tuotanto [kWh]':<28}"
    r2 = f"{'':<12}{'(pv.kk.vvvv)':<12}{'v1':>8}{'v2':>8}{'v3':>8}{'':>4}{'v1':>8}{'v2':>8}{'v3':>8}"
    r3 = "-" * 75
    return [r1, r2, r3]

def muodosta_viikon_raporttirivit(paivat: Dict[date, Dict[str, float]]) -> List[str]:
    """Muodostaa yhden viikon taulukkorivit raporttiin päiväkohtaisista summista."""
    rivit: List[str] = []
    for paiva in sorted(paivat.keys()):
        pvm_str = f"{paiva.day}.{paiva.month}.{paiva.year}"
        viikonpaiva = viikonpaiva_suomeksi(paiva)
        data = paivat[paiva]
        rivi = (
            f"{viikonpaiva:<12}{pvm_str:<12}"
            f"{muotoile_luku(data['kulutus1']):>8}"
            f"{muotoile_luku(data['kulutus2']):>8}"
            f"{muotoile_luku(data['kulutus3']):>8}"
            f"{'':>4}"
            f"{muotoile_luku(data['tuotanto1']):>8}"
            f"{muotoile_luku(data['tuotanto2']):>8}"
            f"{muotoile_luku(data['tuotanto3']):>8}"
        )
        rivit.append(rivi)
    return rivit

def laske_viikkosummat(paivat: Dict[date, Dict[str, float]]) -> Tuple[float, float]:
    """Laskee viikon kokonaiskulutuksen ja -tuotannon."""
    kokonais_kulutus = 0.0
    kokonais_tuotanto = 0.0
    for data in paivat.values():
        kokonais_kulutus += data["kulutus1"] + data["kulutus2"] + data["kulutus3"]
        kokonais_tuotanto += data["tuotanto1"] + data["tuotanto2"] + data["tuotanto3"]
    return kokonais_kulutus, kokonais_tuotanto

def kirjoita_raportti(tiedoston_nimi: str, viikkojen_raportit: List[str]) -> None:
    """Kirjoittaa raportin tiedostoon with-rakenteella."""
    with open(tiedoston_nimi, "w", encoding="utf-8") as f:
        for rivi in viikkojen_raportit:
            f.write(rivi + "\n")

def main() -> None:
    """Ohjelman pääfunktio: lukee datan, laskee viikkoyhteenvedot ja kirjoittaa raportin tiedostoon."""
    # Lue datat
    viikko41 = lue_data("viikko41.csv")
    viikko42 = lue_data("viikko42.csv")
    viikko43 = lue_data("viikko43.csv")

    # Laske päiväkohtaiset summat
    paivat41 = ryhmittele_paivittain(viikko41)
    paivat42 = ryhmittele_paivittain(viikko42)
    paivat43 = ryhmittele_paivittain(viikko43)

    raportti_rivit: List[str] = []

    for viikkonro, paivat in [(41, paivat41), (42, paivat42), (43, paivat43)]:
        raportti_rivit.append(muodosta_viikko_otsikko(viikkonro))
        raportti_rivit.extend(muodosta_taulukon_otsikot())
        raportti_rivit.extend(muodosta_viikon_raporttirivit(paivat))
        vk_kulutus, vk_tuotanto = laske_viikkosummat(paivat)
        raportti_rivit.append("-" * 75)
        raportti_rivit.append(
            f"{'Yhteensä viikon ' + str(viikkonro):<24}"
            f"{'':<12}"
            f"{muotoile_luku(vk_kulutus):>12}"
            f"{'':>16}"
            f"{muotoile_luku(vk_tuotanto):>12}"
        )
        raportti_rivit.append("")

    kirjoita_raportti("yhteenveto.txt", raportti_rivit)

if __name__ == "__main__":
    main()
