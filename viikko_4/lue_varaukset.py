"""
Ohjelma joka tulostaa tiedostosta luettujen varausten alkiot ja niiden tietotyypit

varausId | nimi | sähköposti | puhelin | varauksenPvm | varauksenKlo | varauksenKesto | hinta | varausVahvistettu | varattuTila | varausLuotu
------------------------------------------------------------------------
201 | Muumi Muumilaakso | muumi@valkoinenlaakso.org | 0509876543 | 2025-11-12 | 09:00:00 | 2 | 18.50 | True | Metsätila 1 | 2025-08-12 14:33:20
int | str | str | str | date | time | int | float | bool | str | datetime
------------------------------------------------------------------------
202 | Niiskuneiti Muumilaakso | niisku@muumiglam.fi | 0451122334 | 2025-12-01 | 11:30:00 | 1 | 12.00 | False | Kukkahuone | 2025-09-03 09:12:48
int | str | str | str | date | time | int | float | bool | str | datetime
------------------------------------------------------------------------
203 | Pikku Myy Myrsky | myy@pikkuraivo.net | 0415566778 | 2025-10-22 | 15:45:00 | 3 | 27.90 | True | Punainen Huone | 2025-07-29 18:05:11
int | str | str | str | date | time | int | float | bool | str | datetime
------------------------------------------------------------------------
204 | Nipsu Rahapulainen | nipsu@rahahuolet.me | 0442233445 | 2025-09-18 | 13:00:00 | 4 | 39.95 | False | Varastotila N | 2025-08-01 10:59:02
int | str | str | str | date | time | int | float | bool | str | datetime
------------------------------------------------------------------------
205 | Hemuli Kasvikerääjä | hemuli@kasvikeraily.club | 0463344556 | 2025-11-05 | 08:15:00 | 2 | 19.95 | True | Kasvitutkimuslabra | 2025-10-09 16:41:55
int | str | str | str | date | time | int | float | bool | str | datetime
------------------------------------------------------------------------
"""

from datetime import datetime

def muunna_varaustiedot(varaus: list) -> list:
    muutettu_varaus = []

    # 1) varausId: str -> int
    muutettu_varaus.append(int(varaus[0]))

    # 2) nimi: str
    muutettu_varaus.append(str(varaus[1]))

    # 3) sähköposti: str
    muutettu_varaus.append(str(varaus[2]))

    # 4) puhelin: str
    muutettu_varaus.append(str(varaus[3]))

    # 5) varauksenPvm: "2025-11-12" -> datetime.date
    muutettu_varaus.append(datetime.strptime(varaus[4], "%Y-%m-%d").date())

    # 6) varauksenKlo: "09:00:00" -> datetime.time
    muutettu_varaus.append(datetime.strptime(varaus[5], "%H:%M").time())

    # 7) varauksenKesto: str -> int
    muutettu_varaus.append(int(varaus[6]))

    # 8) hinta: str -> float
    muutettu_varaus.append(float(varaus[7]))

    # 9) varausVahvistettu: "True"/"False" -> bool
    muutettu_varaus.append(varaus[8].strip().lower() == "true")

    # 10) varattuTila: str
    muutettu_varaus.append(str(varaus[9]))

    # 11) varausLuotu: "2025-08-12 14:33:20" -> datetime.datetime
    muutettu_varaus.append(datetime.strptime(varaus[10], "%Y-%m-%d %H:%M:%S"))

    return muutettu_varaus

def hae_varaukset(varaustiedosto: str) -> list:
    # HUOM! Tälle funktioille ei tarvitse tehdä mitään!
    # Jos muutat, kommentoi miksi muutit
    varaukset = []
    varaukset.append(["varausId", "nimi", "sähköposti", "puhelin", "varauksenPvm", "varauksenKlo", "varauksenKesto", "hinta", "varausVahvistettu", "varattuTila", "varausLuotu"])
    with open(varaustiedosto, "r", encoding="utf-8") as f:
        for varaus in f:
            varaus = varaus.strip()
            varaustiedot = varaus.split('|')
            varaukset.append(muunna_varaustiedot(varaustiedot))
    return varaukset

def main():
    # HUOM! seuraaville riveille ei tarvitse tehdä mitään osassa A!
    # Osa B vaatii muutoksia -> Esim. tulostuksien (print-funktio) muuttamisen.
    # Kutsutaan funkioita hae_varaukset, joka palauttaa kaikki varaukset oikeilla tietotyypeillä
    varaukset = hae_varaukset("varaukset.txt")
    
    data = varaukset[1:]

    print("1) Vahvistetut varaukset")
    for v in data:
        varaus_id, nimi, sahkoposti, puhelin, paiva, aloitusaika, kesto, hinta, vahvistettu, kohde, luotu = v
        if vahvistettu:
            print(f"- {nimi}, {kohde}, {paiva.strftime('%d.%m.%Y')} klo {aloitusaika.strftime('%H.%M')}")
    print()

    print("2) Pitkät varaukset (≥ 3 h)")
    for v in data:
        nimi, paiva, aloitusaika, kesto, kohde = v[1], v[4], v[5], v[6], v[9]
        if kesto >= 3:
            print(f"- {nimi}, {paiva.strftime('%d.%m.%Y')} klo {aloitusaika.strftime('%H.%M')}, kesto {kesto} h, {kohde}")
    print()

    print("3) Varausten vahvistusstatus")
    for v in data:
        nimi, vahvistettu = v[1], v[8]
        status = "Vahvistettu" if vahvistettu else "EI vahvistettu"
        print(f"{nimi} → {status}")
    print()

    print("4) Yhteenveto vahvistuksista")
    vahvistetut = sum(1 for v in data if v[8])
    ei_vahvistetut = sum(1 for v in data if not v[8])
    print(f"- Vahvistettuja varauksia: {vahvistetut} kpl")
    print(f"- Ei-vahvistettuja varauksia: {ei_vahvistetut} kpl")
    print()

    print("5) Vahvistettujen varausten kokonaistulot")
    kokonaistulot = sum(v[6] * v[7] for v in data if v[8])  # kesto * tuntihinta
    print(f"Vahvistettujen varausten kokonaistulot: {kokonaistulot:.2f}".replace(".", ",") + " €")

if __name__ == "__main__":
    main()
