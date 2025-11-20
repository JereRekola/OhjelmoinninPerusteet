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
def hae_varausnumero(varaus):
    return varaus[0]

def hae_varaaja(varaus):
    return varaus[1]

def hae_paiva(varaus):
    return varaus[2]

def hae_aloitusaika(varaus):
    return varaus[3]

def hae_tuntimaara(varaus):
    return int(varaus[4])

def hae_tuntihinta(varaus):
    # Muutetaan desimaalipilkku pisteeksi, jotta float toimii
    return float(varaus[5].replace(",", "."))

def laske_kokonaishinta(varaus):
    return hae_tuntimaara(varaus) * hae_tuntihinta(varaus)

def hae_maksettu(varaus):
    return varaus[7]

def hae_kohde(varaus):
    return varaus[8]

def hae_puhelin(varaus):
    return varaus[9]

def hae_sahkoposti(varaus):
    return varaus[10]


def main():
    tiedosto = "varaukset.txt"

    with open(tiedosto, "r", encoding="utf-8") as f:
        for rivi in f:
            osat = rivi.strip().split("|")

            # Varmistetaan että kenttiä on tarpeeksi
            if len(osat) < 11:
                print("Virheellinen rivi, kenttiä liian vähän:", osat)
                continue

            aloitusaika = hae_aloitusaika(osat)

            if ":" in aloitusaika:
                tunti, minuutti = aloitusaika.split(":")
            elif "." in aloitusaika:
                tunti, minuutti = aloitusaika.split(".")
            else:
                continue

            tunti = int(tunti)
            minuutti = int(minuutti)

            if 8 <= tunti <= 12:
                print(f"Varausnumero: {hae_varausnumero(osat)}")
                print(f"Varaaja: {hae_varaaja(osat)}")
                print(f"Päivämäärä: {hae_paiva(osat)}")
                print(f"Aloitusaika: {hae_aloitusaika(osat)}")
                print(f"Tuntimäärä: {hae_tuntimaara(osat)}")
                print(f"Tuntihinta: {f'{hae_tuntihinta(osat):.2f}'.replace('.', ',')} €")
                print(f"Kokonaishinta: {f'{laske_kokonaishinta(osat):.2f}'.replace('.', ',')} €")
                print(f"Maksettu: {hae_maksettu(osat)}")
                print(f"Kohde: {hae_kohde(osat)}")
                print(f"Puhelin: {hae_puhelin(osat)}")
                print(f"Sähköposti: {hae_sahkoposti(osat)}")
                print("-" * 40)



if __name__ == "__main__":
    main()
