"""
Ohjelma joka lukee tiedostossa olevat varaustiedot
ja tulostaa ne konsoliin. Alla esimerkkitulostus:

Varausnumero: 123
Varaaja: Anna Virtanen
Päivämäärä: 31.10.2025
Aloitusaika: 10.00
Tuntimäärä: 2
Tuntihinta: 19.95 €
Kokonaishinta: 39.9 €
Maksettu: Kyllä
Kohde: Kokoustila A
Puhelin: 0401234567
Sähköposti: anna.virtanen@example.com

"""
def main():
    
    tiedosto = "varaukset.txt"

    with open(tiedosto, "r", encoding="utf-8") as f:
        for rivi in f:   # käydään tiedosto rivi kerrallaan
            osat = rivi.strip().split("|")
            aloitusaika = osat[3]

            if ":" in aloitusaika:
                tunti, minuutti = aloitusaika.split(":")
            elif "." in aloitusaika:
                tunti, minuutti = aloitusaika.split(".")
            else:
                continue

            tunti = int(tunti)
            minuutti = int(minuutti)

            
            if 8 <= tunti <= 12:
                print(f"Varausnumero: {osat[0]}")
                print(f"Varaaja: {osat[1]}")
                print(f"Päivämäärä: {osat[2]}")
                print(f"Aloitusaika: {osat[3]}")
                print(f"Tuntimäärä: {osat[4]}")
                print(f"Tuntihinta: {osat[5]} €")
                print(f"Kokonaishinta: {osat[6]} €")
                print(f"Maksettu: {osat[7]}")
                print(f"Kohde: {osat[8]}")
                print(f"Puhelin: {osat[9]}")
                print(f"Sähköposti: {osat[10]}")
                print("-" * 40)




if __name__ == "__main__":
    main()