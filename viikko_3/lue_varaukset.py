"""
Ohjelma joka lukee tiedostossa olevat varaustiedot
ja tulostaa ne konsoliin. Alla esimerkkitulostus:

Varausnumero: 123
Varaaja: Anna Virtanen
Päivämäärä: 31.10.2025
Aloitusaika: 10.00
Tuntimäärä: 2
Tuntihinta: 19,95 €
Kokonaishinta: 39,90 €
Maksettu: Kyllä
Kohde: Kokoustila A
Puhelin: 0401234567
Sähköposti: anna.virtanen@example.com

"""
from datetime import datetime

def hae_varausnumero(varaus):
    return int(varaus[0]) 

def hae_varaaja(varaus):
    return varaus[1].strip()  

def hae_paiva(varaus):
    paiva_str = varaus[2].strip()
    try:
        return datetime.strptime(paiva_str, "%d.%m.%Y").date()
    except ValueError:
        return datetime.strptime(paiva_str, "%Y-%m-%d").date()

def hae_aloitusaika(varaus):
    aika_str = varaus[3].strip()
    if ":" in aika_str:
        return datetime.strptime(aika_str, "%H:%M").time()
    elif "." in aika_str:
        return datetime.strptime(aika_str, "%H.%M").time()
    return None

def hae_tuntimaara(varaus):
    return int(varaus[4])  

def hae_tuntihinta(varaus):
    return float(varaus[5].replace(",", "."))  

def laske_kokonaishinta(varaus):
    return hae_tuntimaara(varaus) * hae_tuntihinta(varaus)

def hae_maksettu(varaus):
    return varaus[6].strip().lower() in ["kyllä", "yes", "true", "1"]

def hae_kohde(varaus):
    return varaus[7].strip()

def hae_puhelin(varaus):
    return varaus[8].strip()

def hae_sahkoposti(varaus):
    return varaus[9].strip()


def main():
    tiedosto = "varaukset.txt"

    with open(tiedosto, "r", encoding="utf-8") as f:
        for rivi in f:
            osat = rivi.strip().split("|")

            if len(osat) < 10:
                print("Virheellinen rivi, kenttiä liian vähän:", osat)
                continue

            aloitusaika = hae_aloitusaika(osat)
            if aloitusaika is None:
                continue

            tunti = aloitusaika.hour
            minuutti = aloitusaika.minute

            if 8 <= tunti <= 12:
                print(f"Varausnumero: {hae_varausnumero(osat)}")
                print(f"Varaaja: {hae_varaaja(osat)}")
                print(f"Päivämäärä: {hae_paiva(osat).strftime('%d.%m.%Y')}")
                print(f"Aloitusaika: {aloitusaika.strftime('%H.%M')}")
                print(f"Tuntimäärä: {hae_tuntimaara(osat)}")
                print(f"Tuntihinta: {f'{hae_tuntihinta(osat):.2f}'.replace('.', ',')} €")
                print(f"Kokonaishinta: {f'{laske_kokonaishinta(osat):.2f}'.replace('.', ',')} €")
                print(f"Maksettu: {'Kyllä' if hae_maksettu(osat) else 'Ei'}")
                print(f"Kohde: {hae_kohde(osat)}")
                print(f"Puhelin: {hae_puhelin(osat)}")
                print(f"Sähköposti: {hae_sahkoposti(osat)}")
                print("-" * 40)


if __name__ == "__main__":
    main()


