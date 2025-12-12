# Copyright (c) 2025 Oma Nimi
# License: MIT

import csv
from datetime import datetime, date
from typing import List, Dict, Tuple

def lue_data(tiedoston_nimi: str) -> List[Dict]:
    """Lukee CSV-tiedoston ja palauttaa rivit sanakirjoina listassa."""
    data = []
    with open(tiedoston_nimi, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for rivi in reader:
            rivi = {k.lower().strip(): v for k, v in rivi.items()}
            aika = datetime.fromisoformat(rivi["aika"])
            kulutus = float(rivi.get("kulutus (netotettu) kwh", rivi.get("kulutus", "0")).replace(",", "."))
            tuotanto = float(rivi.get("tuotanto (netotettu) kwh", rivi.get("tuotanto", "0")).replace(",", "."))
            lampotila = float(rivi.get("vuorokauden keskilämpötila", "0").replace(",", "."))
            data.append({
                "aika": aika,
                "kulutus": kulutus,
                "tuotanto": tuotanto,
                "lampotila": lampotila
            })
    return data

def nayta_paavalikko() -> str:
    print("\nValitse raporttityyppi:")
    print("1) Päiväkohtainen yhteenveto aikaväliltä")
    print("2) Kuukausikohtainen yhteenveto yhdelle kuukaudelle")
    print("3) Vuoden 2025 kokonaisyhteenveto")
    print("4) Lopeta ohjelma")
    return input("Valintasi: ")

def muotoile_luku(arvo: float) -> str:
    return f"{arvo:.2f}".replace(".", ",")

def muotoile_pvm(pvm: date) -> str:
    return f"{pvm.day}.{pvm.month}.{pvm.year}"

def luo_paivaraportti(data: List[Dict]) -> Tuple[List[str], date, date]:
    alku_str = input("Anna alkupäivä (pv.kk.vvvv): ")
    loppu_str = input("Anna loppupäivä (pv.kk.vvvv): ")
    alku = datetime.strptime(alku_str, "%d.%m.%Y").date()
    loppu = datetime.strptime(loppu_str, "%d.%m.%Y").date()

    kulutus_sum = 0.0
    tuotanto_sum = 0.0
    lampotilat = []

    for rivi in data:
        paiva = rivi["aika"].date()
        if alku <= paiva <= loppu:
            kulutus_sum += rivi["kulutus"]
            tuotanto_sum += rivi["tuotanto"]
            lampotilat.append(rivi["lampotila"])

    keski_lampo = sum(lampotilat) / len(lampotilat) if lampotilat else 0.0

    rivit = [
        "=== Päiväkohtainen yhteenveto ===",
        f"Aikaväli: {muotoile_pvm(alku)} - {muotoile_pvm(loppu)}",
        f"Kokonaiskulutus: {muotoile_luku(kulutus_sum)} kWh",
        f"Kokonaistuotanto: {muotoile_luku(tuotanto_sum)} kWh",
        f"Keskilämpötila: {muotoile_luku(keski_lampo)} °C"
    ]
    return rivit, alku, loppu

def luo_kuukausiraportti(data: List[Dict]) -> Tuple[List[str], int]:
    kuukausi = int(input("Anna kuukauden numero (1–12): "))
    kulutus_sum = 0.0
    tuotanto_sum = 0.0
    lampotilat = []

    for rivi in data:
        if rivi["aika"].month == kuukausi:
            kulutus_sum += rivi["kulutus"]
            tuotanto_sum += rivi["tuotanto"]
            lampotilat.append(rivi["lampotila"])

    keski_lampo = sum(lampotilat) / len(lampotilat) if lampotilat else 0.0

    rivit = [
        "=== Kuukausiyhteenveto ===",
        f"Kuukausi: {kuukausi}",
        f"Kokonaiskulutus: {muotoile_luku(kulutus_sum)} kWh",
        f"Kokonaistuotanto: {muotoile_luku(tuotanto_sum)} kWh",
        f"Keskilämpötila: {muotoile_luku(keski_lampo)} °C"
    ]
    return rivit, kuukausi

def luo_vuosiraportti(data: List[Dict]) -> List[str]:
    kulutus_sum = sum(r["kulutus"] for r in data)
    tuotanto_sum = sum(r["tuotanto"] for r in data)
    keski_lampo = sum(r["lampotila"] for r in data) / len(data)

    rivit = [
        "=== Vuoden 2025 yhteenveto ===",
        f"Kokonaiskulutus: {muotoile_luku(kulutus_sum)} kWh",
        f"Kokonaistuotanto: {muotoile_luku(tuotanto_sum)} kWh",
        f"Keskilämpötila: {muotoile_luku(keski_lampo)} °C"
    ]
    return rivit

def tulosta_raportti_konsoliin(rivit: List[str]) -> None:
    print("\n".join(rivit))

def kirjoita_raportti_tiedostoon(rivit: List[str], raporttityyppi: str, alku: date = None, loppu: date = None, kuukausi: int = None) -> None:
    """Kirjoittaa raportin rivit tiedostoon automaattisesti nimettynä."""
    aikaleima = datetime.now().strftime("%Y-%m-%d")
    if raporttityyppi == "paiva" and alku and loppu:
        tiedoston_nimi = f"raportti_paiva_{alku.day}-{alku.month}-{alku.year}_to_{loppu.day}-{loppu.month}-{loppu.year}_{aikaleima}.txt"
    elif raporttityyppi == "kuukausi" and kuukausi:
        tiedoston_nimi = f"raportti_kuukausi_{kuukausi:02d}_2025_{aikaleima}.txt"
    elif raporttityyppi == "vuosi":
        tiedoston_nimi = f"raportti_vuosi_2025_{aikaleima}.txt"
    else:
        tiedoston_nimi = f"raportti_{aikaleima}.txt"

    with open(tiedoston_nimi, "w", encoding="utf-8") as f:
        for rivi in rivit:
            f.write(rivi + "\n")
    print(f"Raportti kirjoitettu tiedostoon {tiedoston_nimi}.")

def nayta_jatkotoimet() -> str:
    print("\nMitä haluat tehdä seuraavaksi?")
    print("1) Kirjoita raportti tiedostoon (automaattinen nimi)")
    print("2) Luo uusi raportti")
    print("3) Lopeta")
    return input("Valintasi: ")

def main() -> None:
    data = lue_data("2025.csv")

    while True:
        valinta = nayta_paavalikko()
        if valinta == "1":
            raportti, alku, loppu = luo_paivaraportti(data)
            raporttityyppi = "paiva"
        elif valinta == "2":
            raportti, kuukausi = luo_kuukausiraportti(data)
            raporttityyppi = "kuukausi"
        elif valinta == "3":
            raportti = luo_vuosiraportti(data)
            raporttityyppi = "vuosi"
        elif valinta == "4":
            print("Ohjelma lopetetaan.")
            break
        else:
            print("Virheellinen valinta.")
            continue

        tulosta_raportti_konsoliin(raportti)

        jatko = nayta_jatkotoimet()
        if jatko == "1":
            if raporttityyppi == "paiva":
                kirjoita_raportti_tiedostoon(raportti, raporttityyppi, alku, loppu)
            elif raporttityyppi == "kuukausi":
                kirjoita_raportti_tiedostoon(raportti, raporttityyppi, kuukausi=kuukausi)
            else:
                kirjoita_raportti_tiedostoon(raportti, raporttityyppi)
        elif jatko == "2":
            continue
        elif jatko == "3":
            print("Ohjelma lopetetaan.")
            break
        else:
            print("Virheellinen valinta.")

if __name__ == "__main__":
    main()