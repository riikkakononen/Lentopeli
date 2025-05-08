import mysql.connector
import time
import json
import random
import math
from weather_service import get_weather_for_country


class Pelaaja:
    def __init__(self, nimi, nykyinen_maa="Suomi", tähdet=0, vieraillut_maat=None):
        if vieraillut_maat is None:
            vieraillut_maat = []
        self.nimi = nimi
        self.nykyinen_maa = nykyinen_maa
        self.tähdet = tähdet
        self.vieraillut_maat = vieraillut_maat

    def lisää_tähdet(self, määrä):
        self.tähdet += määrä

    def vähennä_tähdet(self, määrä):
        self.tähdet -= määrä

    def lisää_vieraillut_maa(self, maa):
        if maa not in self.vieraillut_maat:
            self.vieraillut_maat.append(maa)

    def __str__(self):
        return f"Player: {self.nimi}, Tähdet: {self.tähdet}, Nykyinen Maa: {self.nykyinen_maa}"


class Kysmys:
    def __init__(self, kysymys, vaihtoehdot, oikea_vastaus):
        self.kysymys = kysymys
        self.vaihtoehdot = json.loads(vaihtoehdot)  # Assuming it's a JSON string
        self.oikea_vastaus = oikea_vastaus

    def esita_kysymys(self):
        print(f"\n{self.kysymys}")
        for key, value in self.vaihtoehdot.items():
            print(f"{key}. {value}")

    def tarkista_vastaus(self, vastaus):
        return vastaus == self.oikea_vastaus


class CO2Manager:
    CO2_THRESHOLD = 3600  # kilogrammoina

    def __init__(self):
        self.total_emissions = 0

    def update_emissions(self, amount):
        self.total_emissions += amount

    def get_total_emissions(self):
        return self.total_emissions

    def is_over_limit(self):
        return self.total_emissions > self.CO2_THRESHOLD

    def increase_threshold(self, amount):
        self.CO2_THRESHOLD += amount



class Peli:
    def __init__(self, pelaaja, yhteys):
        self.pelaaja = pelaaja
        self.yhteys = yhteys
        self.cursor = self.yhteys.cursor()
        self.co2_manager = CO2Manager()  # Instantiate CO2Manager

    def intro(self, text):
        for i in text:
            print(i, end="")
            time.sleep(0.030)
        print()
        time.sleep(len(text) / 1000)

    def aloita(self):
        self.intro("Tervetuloa Lennä ja tiedä! -peliin, jossa opit lisää eri Euroopan maista!")
        self.intro("Tässä pelissä saat tähtiä oikein vastatuista kysymyksistä eri maista, joihin olet lentämässä.")
        self.intro("Pelin lopussa sinulle kerrotaan montako tähteä, eli pistettä, olet kerännyt. Maksimi pistemäärä on 30.")
        self.intro("Oletko ymmärtänyt ohjeet? Paina enter aloittaaksesi!")
        input("")
        self.intro("Olet Helsinki-Vantaan lentokentällä. Olet saanut tarpeeksesi Suomen kylmyydestä ja haluat vaihtaa maisemaa.")
        self.alusta_peli()

    def alusta_peli(self):
        # Poistetaan vanhat pelit ennen uuden aloittamista
        self.cursor.execute("Delete FROM player_state")
        sql = "INSERT INTO player_state (nykyinen_maa, tähdet, vieraillut_maat) VALUES (%s, %s, %s)"
        arvot = ("Suomi", 0, "[]")
        self.cursor.execute(sql, arvot)
        self.yhteys.commit()

        while True:
            self.play_round()


    def play_round(self):
        self.cursor.execute("SELECT vieraillut_maat FROM player_state")
        result = self.cursor.fetchone()

        if result:
            self.pelaaja.vieraillut_maat = json.loads(result[0])

        self.cursor.execute("SELECT id, maa FROM airports")
        tulos = self.cursor.fetchall()

        saatavilla_maat = sorted([x for x in tulos if x[1] not in self.pelaaja.vieraillut_maat],
                                 key=lambda x: x[0])

        if not saatavilla_maat:
            self.pelaaja_loppu()

        print('\nValitse seuraava kohdemaa.')
        for x in saatavilla_maat:
            print(x)

        maa_id = int(input('\nAnna kohdemaata vastaava numero: '))
        self.cursor.execute("SELECT maa, nimi FROM airports WHERE id = %s", (maa_id,))
        rivit = self.cursor.fetchall()

        if rivit:
            kohdemaa, nimi = rivit[0]
            print(f'Olet matkalla maahan {kohdemaa}, kentälle {nimi}.')

            kysymykset_query = "SELECT kysymys, vaihtoehdot, oikea_vastaus FROM questions WHERE maa = %s"
            self.cursor.execute(kysymykset_query, (kohdemaa,))
            questions = self.cursor.fetchall()

            random.shuffle(questions)
            questions = questions[:3]

            oikeat_vastaukset = 0
            for kysymys, vaihtoehdot, oikea_vastaus in questions:
                kysymys_obj = Kysmys(kysymys, vaihtoehdot, oikea_vastaus)
                kysymys_obj.esita_kysymys()

                while True:
                    vastaus = input("Valitse oikea vaihtoehto (A/B/C): ").strip().upper()
                    if vastaus in kysymys_obj.vaihtoehdot:
                        break
                    else:
                        print("Virheellinen syöte, yritä uudelleen.")

                if kysymys_obj.tarkista_vastaus(vastaus):
                    print("Vastaus oikein!")
                    oikeat_vastaukset += 1
                else:
                    print("Vastaus väärin.")

            if oikeat_vastaukset > 0:
                print(f"Hyvin meni! Sait {oikeat_vastaukset} tähteä.")
                self.pelaaja.lisää_tähdet(oikeat_vastaukset)
                self.pelaaja.lisää_vieraillut_maa(kohdemaa)
                self.tallenna_tilanne(oikeat_vastaukset, kohdemaa)

                self.co2_manager.update_emissions(300)

                if self.co2_manager.is_over_limit():
                    self.kasittele_paastorajan_ylitys()
            else:
                print("\nEt vastannut yhteenkään kysymykseen oikein.")

                from weather_service import get_weather_for_country
                saa = get_weather_for_country(kohdemaa)

                if saa == "hyvä":
                    print("Sää on hyvä – palaat edelliseen maahan ja voit valita uuden kohteen.")
                    self.co2_manager.update_emissions(300)
                    if self.co2_manager.is_over_limit():
                        self.kasittele_paastorajan_ylitys()
                else:
                    print("Sää on huono – paluu ei onnistu. Yrität uudelleen samaan maahan.")
                    self.co2_manager.update_emissions(300)
                    if self.co2_manager.is_over_limit():
                        self.kasittele_paastorajan_ylitys()

    def tallenna_tilanne(self, oikeat_vastaukset, kohdemaa):
        update_query = "UPDATE player_state SET tähdet = tähdet + %s"
        self.cursor.execute(update_query, (oikeat_vastaukset,))
        self.yhteys.commit()

        update_query = "UPDATE player_state SET nykyinen_maa = %s"
        self.cursor.execute(update_query, (kohdemaa,))
        self.yhteys.commit()

        self.cursor.execute("SELECT vieraillut_maat FROM player_state")
        result = self.cursor.fetchone()

        if result:
            vieraillut_maat = json.loads(result[0])
        else:
            vieraillut_maat = []

        if kohdemaa not in vieraillut_maat:
            vieraillut_maat.append(kohdemaa)
            update_query = "UPDATE player_state SET vieraillut_maat = %s"
            self.cursor.execute(update_query, (json.dumps(vieraillut_maat),))
            self.yhteys.commit()

    def pelaaja_loppu(self):
        print("\nOnneksi olkoon! Olet vieraillut kaikissa maissa ja suorittanut pelin loppuun!")
        self.cursor.execute("SELECT tähdet FROM player_state")
        tulos = self.cursor.fetchone()
        kokonaistähdet = tulos[0] if tulos else 0
        print(f'Kokonaispistemääräsi: {kokonaistähdet} tähteä!')
        print(f"Yhteensä CO2 päästöjä: {self.co2_manager.get_total_emissions():.2f}g")
        self.cursor.close()
        self.yhteys.close()
        exit()

    def kasittele_paastorajan_ylitys(self):
        print("\n⚠️ CO2-raja ylitetty!")
        print(
            f"Nykyiset päästöt: {self.co2_manager.get_total_emissions()} kg / {self.co2_manager.CO2_THRESHOLD} kg")
        print(f"Sinulla on {self.pelaaja.tähdet} tähteä.")

        if self.pelaaja.tähdet == 0:
            print("Sinulla ei ole yhtään tähteä – peli päättyy.")
            exit()

        print("\nVoit jatkaa peliä käyttämällä tähtiä nostaaksesi CO2-rajaa:")
        vaihtoehdot = []
        if self.pelaaja.tähdet >= 1:
            vaihtoehdot.append(("1", 1, 300))
        if self.pelaaja.tähdet >= 3:
            vaihtoehdot.append(("2", 3, 900))
        if self.pelaaja.tähdet >= 5:
            vaihtoehdot.append(("3", 5, 1500))

        for koodi, tähdet, lisäys in vaihtoehdot:
            print(f"{koodi}. Käytä {tähdet} tähteä → lisää {lisäys} kg päästötilaa")

        print("0. Lopeta peli")

        valinta = input("Valintasi: ").strip()

        if valinta == "0":
            print("Peli päättyy. Kiitos pelaamisesta!")
            exit()

        for koodi, tähdet, lisäys in vaihtoehdot:
            if valinta == koodi:
                self.pelaaja.vähennä_tähdet(tähdet)
                self.co2_manager.increase_threshold(lisäys)
                print(f"CO2-rajaa nostettiin {lisäys} kg. Uusi raja: {self.co2_manager.CO2_THRESHOLD} kg.")
                return

        print("Virheellinen valinta. Peli päättyy.")
        exit()

try:
    yhteys = mysql.connector.connect(
        host='localhost',
        database='lentopeli',
        user='user',
        password='password',
        autocommit=True,
        collation='utf8mb4_unicode_ci'
    )

    pelaaja = Pelaaja("Player1")
    peli = Peli(pelaaja, yhteys)
    peli.aloita()

except mysql.connector.Error as err:
    print(f"Virhe tietokantaoperaatiossa: {err}")
except Exception as e:
    print(f'Virhe pelin aikana: {e}')