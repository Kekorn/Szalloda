import os
from abc import ABC
from datetime import *

os.system("color")


def szinez(string: str, szin: int):
    feher = "\033[0m"  # alapértelmezett szín
    piros = "\033[31m"  # figyelmeztetés színe
    zold = "\033[32m"  # nyugtázás
    sarga = "\033[33m"  # menü színe
    if szin == 1:
        return piros + string + feher
    elif szin == 2:
        return zold + string + feher
    else:
        return sarga + string + feher


# Osztályok Létrehozása
#   ● Hozz létre egy Szoba absztrakt osztályt, amely alapvető attribútumokat definiál (ár, szobaszám). (5 pont)
#   ● Hozz létre az Szoba osztályból EgyagyasSzoba és KetagyasSzoba származtatott osztályokat, amelyek különböző
#     attributumai vannak, és az áruk Is különböző.(5 pont)
#   ● Hozz létre egy Szalloda osztályt, ami ezekből a Szobákból áll, és van saját attributuma is (név pl.) (10 pont)
#   ● Hozz létre egy Foglalás osztályt, amelybe a Szálloda szobáinak foglalását tároljuk (elég itt, ha egy foglalás
#     csak egy napra szól) (10 pont)
#
# Foglalások Kezelése
#   ● Implementálj egy metódust, ami lehetővé teszi szobák foglalását dátum alapján, visszaadja annak árát. (15 pont)
#   ● Implementálj egy metódust, ami lehetővé teszi a foglalás lemondását. (5 pont)
#   ● Implementálj egy metódust, ami listázza az összes foglalást. (5 pont)
#
# Felhasználói Interfész és adatvalidáció
#   ● Készíts egy egyszerű felhasználói interfészt, ahol a felhasználó kiválaszthatja a kívánt műveletet (pl. foglalás,
#     lemondás, listázás). (20 pont)
#   ● A foglalás létrehozásakor ellenőrizd, hogy a dátum érvényes (jövőbeni) és a szoba elérhető-e akkor. (10 pont)
#   ● Biztosítsd, hogy a lemondások csak létező foglalásokra lehetségesek. (5 pont)
#   ● Töltsd fel az futtatás után a rendszert 1 szállodával, 3 szobával és 5 foglalással, mielőtt a felhasználói
#     adatbekérés megjelenik. (10 pont)


class Szoba(ABC):
    AGYAK_SZAMA = 1
    ALAP_FELSZERELTSEG = "Ágy, asztal, TV"

    def __init__(self, szobaszam: str, ar: int = 8700, felszereltseg: str = None):
        self.szobaszam = szobaszam
        self.ar = ar * type(self).AGYAK_SZAMA
        self.felszereltseg = type(self).ALAP_FELSZERELTSEG
        if felszereltseg:
            self.felszereltseg += ", " + felszereltseg


class EgyAgyasSzoba(Szoba):
    AGYAK_SZAMA = 1

    def __init__(self, szoba_szam: str, ar: int = 8700, felszereltseg: str = None):
        super().__init__(szoba_szam, ar, felszereltseg)

    def __str__(self):
        return "Szobaszám:".ljust(15) + "{:>29}\n".format(self.szobaszam) + "Ár:".ljust(15) + "{:>25} HUF\n".format(
            self.ar) + "Felszereltség:".ljust(15) + "{:>29}\n".format(self.felszereltseg)


class KetAgyasSzoba(Szoba):
    AGYAK_SZAMA = 2

    def __str__(self):
        return "Szobaszám:".ljust(15) + "{:>29}\n".format(self.szobaszam) + "Ár:".ljust(15) + "{:>25} HUF\n".format(
            self.ar) + "Felszereltség:".ljust(15) + "{:>29}\n".format(self.felszereltseg)

    def __init__(self, szoba_szam: str, ar: int = 8700, felszereltseg: str = None):
        super().__init__(szoba_szam, ar, felszereltseg)


class Szalloda:
    def __init__(self, nev: str, cim: str, elerhetoseg: str):
        self.nev = nev
        self.cim = cim
        self.elerhetoseg = elerhetoseg
        self.szobak = []
        self.foglalasok = []

    def __str__(self):
        return "{}\n{}\n{}\n".format(self.nev, self.cim, self.elerhetoseg)

    def szoba_hozzaadas(self, szoba):
        self.szobak.append(szoba)

    def szoba_lista(self):
        for szoba in self.szobak:
            print(szoba)

    def foglalast_rogzit(self, Foglalas):
        for szoba in self.szobak:
            if szoba.szobaszam == Foglalas.szobaszam:
                Foglalas.ar = szoba.ar

        if Foglalas.ar and Foglalas.datum:

            if Foglalas.datum and Foglalas.datum > datetime.today().date():
                if Foglalas not in self.foglalasok:
                    self.foglalasok.append(Foglalas)
                    self.foglalasok = sorted(self.foglalasok, key=lambda x: (x.szobaszam, x.datum))
                    return 1
                else:
                    print(szinez("Erre a dátumra már van foglalás a szobára!", 1))
            if Foglalas.datum <= datetime.today().date():
                print(szinez("Érvénytelen foglalás! Csak jövőbeli időpontra lehet foglalni!", 1))
        elif Foglalas.ar and not Foglalas.datum:
            print(szinez("Érvénytelen foglalás! Hibás dátum!", 1))
        elif not Foglalas.ar and Foglalas.datum:
            print(szinez("Érvénytelen foglalás! Hibás szobaszám!", 1))
        else:
            print(szinez("Érvénytelen foglalás! Hibás dátum és szobaszám!", 1))

    def foglalast_listaz(self):
        for foglalas in self.foglalasok:
            print(foglalas)

    def foglalast_torol(self, Foglalas):

        if Foglalas in self.foglalasok:
            self.foglalasok.remove(Foglalas)
            print(szinez("A foglalás törölve!", 2))
        else:
            print(szinez("Ilyen foglalás nincs a rendszerünkben!", 1))


class Foglalas:
    def __init__(self, szobaszam: str, datum: str, ar=None):
        self.szobaszam = szobaszam

        try:
            self.datum = datetime.strptime(datum, "%Y-%m-%d").date()
        except ValueError:
            print(szinez("Foglalas -> Érvénytelen dátum!", 1))
            self.datum = None

        self._ar = ar

    def __str__(self):
        return "Szobaszám: {} {:>15} {:>10} HUF ".format(self.szobaszam, str(self.datum), self._ar)

    def __lt__(self, other):
        return self.szobaszam < other.szobaszam and self.datum < other.datum

    def __le__(self, other):
        return self.szobaszam <= other.szobaszam and self.datum <= other.datum

    def __gt__(self, other):
        return self.szobaszam > other.szobaszam and self.datum > other.datum

    def __ge__(self, other):
        return self.szobaszam >= other.szobaszam and self.datum >= other.datum

    def __eq__(self, other):
        return self.szobaszam == other.szobaszam and self.datum == other.datum

    @property
    def ar(self):
        return self._ar

    @ar.setter
    def ar(self, uj_ar):
        self._ar = uj_ar


def main():
    KiserHotel = Szalloda("Kisér Hotel", "5200 Kisér, Zsufka utca 14.",
                          "tel:+36 48 665 124, email: recepcio@kiserhotel.hu, web: kiserhotel.hu")
    KiserHotel.szoba_hozzaadas(EgyAgyasSzoba("E1"))
    KiserHotel.szoba_hozzaadas(KetAgyasSzoba("K1"))
    KiserHotel.szoba_hozzaadas(KetAgyasSzoba("K2", 10900, "Klíma"))
    KiserHotel.foglalast_rogzit(Foglalas("K1", "2029-01-01"))
    KiserHotel.foglalast_rogzit(Foglalas("E1", "2025-01-01"))
    KiserHotel.foglalast_rogzit(Foglalas("E1", "2029-01-01"))
    KiserHotel.foglalast_rogzit(Foglalas("E1", "2028-01-01"))
    KiserHotel.foglalast_rogzit(Foglalas("K2", "2025-11-01"))

    def teszt_esetek():
        KiserHotel.foglalast_rogzit(Foglalas("E1", "2025-01-01"))
        KiserHotel.foglalast_rogzit(Foglalas("K1", "2029-01-01"))
        KiserHotel.foglalast_rogzit(Foglalas("K1", "2025-01-01"))
        KiserHotel.foglalast_rogzit(Foglalas("E1", "2025-01-01"))
        KiserHotel.foglalast_rogzit(Foglalas("E1", "2029-01-01"))
        KiserHotel.foglalast_rogzit(Foglalas("E1", "2028-01-01"))
        KiserHotel.foglalast_rogzit(Foglalas("P1", "2025-01-01"))
        KiserHotel.foglalast_rogzit(Foglalas("P1", "2025-xx/xx"))
        KiserHotel.foglalast_rogzit(Foglalas("E1", "2028xdafg"))
        KiserHotel.foglalast_rogzit(Foglalas("K1", "2024-01-01"))
        KiserHotel.foglalast_rogzit(Foglalas("E1", "2023-01-01"))
        KiserHotel.foglalast_rogzit(Foglalas("K1", "2023-01-01"))
        KiserHotel.foglalast_rogzit(Foglalas("K2", "2025-11-01"))
        KiserHotel.foglalast_listaz()
        KiserHotel.foglalast_torol(Foglalas("E1", "2028-01-01"))
        KiserHotel.foglalast_listaz()

    menu = (szinez("Kérem válasszon az alábbi menüpontok közül:\n"
                   "\t1) Szálloda adatai\n"
                   "\t2) Szobák listája\n"
                   "\t3) Foglalások listája\n"
                   "\t4) Foglalást rögzít\n"
                   "\t5) Foglalást töröl\n"
                   "\t6) Foglalási tesztek\n"
                   "\t0) Kilépés\n", 3) +
            "Választás:")

    menu_egysor = (szinez("Kérem válasszon az alábbi menüpontok közül: "
                          "1) Szálloda adatai "
                          "2) Szobák listája "
                          "3) Foglalások listája "
                          "4) Foglalást rögzít "
                          "5) Foglalást töröl "
                          "6) Foglalási tesztek "
                          "0) Kilépés\n", 3) +
                   "Választás:")

    valasztas = input(menu)
    while valasztas != "0":
        if valasztas == "1":
            print("Hotel adatai:")
            print(KiserHotel)
        elif valasztas == "2":
            print("Szobák listája:")
            KiserHotel.szoba_lista()
        elif valasztas == "3":
            print("Foglalások listája:")
            KiserHotel.foglalast_listaz()
        elif valasztas == "4":
            print("Szoba foglalás:")
            if KiserHotel.foglalast_rogzit(
                    Foglalas(input("Kérem a szobaszámot:"), input("Kérem az időpontot (éééé-hh-nn):"))) == 1:
                print(szinez("A foglalás létrehozva:", 2))
        elif valasztas == "5":
            print("Foglalás törlése:")
            KiserHotel.foglalast_torol(
                Foglalas(input("Kérem a szobaszámot:"), input("Kérem az időpontot (éééé-hh-nn):")))
        elif valasztas == "6":
            teszt_esetek()
        else:
            print(szinez("\nKérem adjon meg érvényes értéket (0-6)", 1))
        valasztas = input(menu_egysor)


main()
print(szinez("Köszönjük, hogy felkereste hotelünket!\n\nViszontlátásra!", 2))
time.sleep(5)
