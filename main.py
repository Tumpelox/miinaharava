import pyglet
from pyglet.gl import glEnable, GL_TEXTURE_2D
import json
import random as rn
import datetime
import haravasto

# # # # # # # # # # # # # # #
#                           #
#       Asetukset ja        #
#      tietorakenteet       #
#                           #
# # # # # # # # # # # # # # #

#Peliruudukon korkeus
#Peliruudukon leveys
#Pelikentän taustaväri
#Ikkunan nimi
#Tekstin väri
#Kansio jossa ruutujen kuvatiedostot on
#Tiedostonimi jonne tulokset tallennetaan
#Kohde jonne pelitiedot tallennetaan tulostiedostosta
#Väliaikainen lista tuloksille kun näytetään tilastoja
#Pelin yläosassa näytettävä naama
#Tuloslistan nykyinen sivu
#Valikon tila
aset = {
    "korkeus": 400,
    "leveys": 600,
	#(33, 150, 243, 255) sininen
    "taustavari": (0, 0, 0, 255),
    "nimi": "Miinaharava 2020",
    "korostus": (255, 255, 255, 255),
    "tausta": "img",
    "tulokset": "tulokset.json",
    "tilastot": [],
    "tuloslista": [],
    "animaatio": 0,
    "larvi": "(*_*)",
    "tuloslistasivu": 1,
    "valikko": True,
    "tulosruutu": False
}

#Pelikenttä ja miinojen paikat
#Pelaajalle näkyvä ilmakuva pelikentästä
#Tyhjät pelikentän ruudut
#Vaikeustaso
#Pelaajan avaamat ruudut
#Pelaajan liputtamat ruudut
#Aika
#Pelin lopputulos
#Pelin loppumisaika
#Pelin tila. Peli päättyy kun miina räjähtää.
tila = {
    "maa": [],
    "pinta": [],
    "tyhjat": [],
    "taso": 25,
    "avattu": [],
    "merkit": [],
    "aika": 0,
    "tulos": None,
    "lopetusaika": None,
    "paattynyt": False,
    "ihmetys": False
}

# # # # # # # # # # # # # # #
#                           #
#         Pääohjelma        #
#                           #
# # # # # # # # # # # # # # #

def main():
    """
    Lataa pelin grafiikat, luo peli-ikkunan ja asettaa siihen piirtokäsittelijän.
    """

    haravasto.lataa_kuvat(aset["tausta"])
    luo_ikkuna(aset["leveys"], aset["korkeus"] + 40, aset["taustavari"], aset["nimi"], "x")
    haravasto.aseta_hiiri_kasittelija(hiiri_kasittelija)
    haravasto.aseta_nappain_kasittelija(nappain_kasittelija)
    haravasto.aseta_piirto_kasittelija(piirra_kentta)
    haravasto.aseta_toistuva_kasittelija(paivitys_kasittelija, 1/60)
    haravasto.aloita()

def luo_ikkuna(leveys, korkeus, taustavari, nimi, ikoni):
    """
    Luo ikkunan ja tallentaa muuttujat haravaston sanakirjaan
    """
    haravasto.grafiikka["ikkuna"] = pyglet.window.Window(leveys, korkeus, nimi, resizable=True)
    haravasto.grafiikka["taustavari"] = taustavari
    haravasto.grafiikka["ikkuna"].set_icon(haravasto.grafiikka["kuvat"]["x"])
    haravasto.grafiikka["tausta"] = pyglet.sprite.Sprite(
        pyglet.image.SolidColorImagePattern(taustavari).create_image(leveys, korkeus)
    )


def hiiri_kasittelija(x, y, nappi, muokkausnapit):
    """
    Käsittelee hiiren klikkaukset ja tekee tarvittavat toimenpiteet
    """
    #Jos valikko ei ole avattuna, voidaan toimia pelikentän mukaan
    if not aset["valikko"]:
        if nappi == 1 and not aset["valikko"]:
            if aset["korkeus"] < y < aset["korkeus"] + 40 and aset["leveys"]/2 - 120 < x < aset["leveys"]/2 + 20:
                uusi_peli(tila["taso"])
            else:
                miinankaivaja(x//40, y//40)
        elif nappi == 4:
            liputus(x//40, y//40)
    #Jos valikko on avattuna, toiminnot ovat valikon mukaan
    elif aset["valikko"]:
        if aset["korkeus"] - aset["korkeus"]/3 - 15 > y > aset["korkeus"] - aset["korkeus"]/3 - 40:
            uusi_peli(10)
        if aset["korkeus"] - aset["korkeus"]/3 - 45 > y > aset["korkeus"] - aset["korkeus"]/3 - 75:
            uusi_peli(15)
        if aset["korkeus"] - aset["korkeus"]/3 - 75 > y > aset["korkeus"] - aset["korkeus"]/3 - 110:
            uusi_peli(25)
        if aset["korkeus"] - aset["korkeus"]/3 - 135 > y > aset["korkeus"] - aset["korkeus"]/3 - 170:
            #Sivunumeron alustus
            aset["tuloslistasivu"] = 1
            aset["tulosruutu"] = True
        if aset["korkeus"] - aset["korkeus"]/3 - 215 > y > aset["korkeus"] - aset["korkeus"]/3 - 245:
            haravasto.lopeta()

def nappain_kasittelija(symboli, muokkausnapit):
    """
    Käsittelee näppäinpainallukset sen mukaan että onko avattuna valikko, tulokset vai itse peli
    """
    if aset["tulosruutu"]:
        if symboli == 65307:
            aset["tulosruutu"] = False
        #Nuoli vasemmalle
        elif symboli == 65361:
            if aset["tuloslistasivu"] > 1 and len(aset["tuloslista"])/(aset["tuloslistasivu"] * 10) > -1:
                aset["tuloslistasivu"] -= 1
        #Nuoli oikealle
        elif symboli == 65363:
            if len(aset["tuloslista"])/(aset["tuloslistasivu"] * 10) > 1:
                aset["tuloslistasivu"] += 1
    elif aset["valikko"]:
        if symboli == 65307:
            haravasto.lopeta()
    else:
        if symboli == 65307:
            aset["valikko"] = True

def paivitys_kasittelija(kulunut_aika):
    """
    Käydään läpi 60 kertaa sekunnissa
    """
    tila["aika"] += kulunut_aika
    if tila["ihmetys"] and not tila["paattynyt"]:
        aset["larvi"] = "(o_o)"
        aset["animaatio"] += kulunut_aika
        if aset["animaatio"] > 0.4:
            tila["ihmetys"] = False
            aset["larvi"] = "(*_*)"
            aset["animaatio"] = 0

def aikakone():
    """
    Syöttää pyydettäessä ajankohdan joka on muotoa vv-kk-pp-tt:mm
    """
    a = datetime.datetime.now()

    aika = "{}-{}-{}-{}:{}".format(
    a.year, 
    a.strftime("%m"), 
    a.strftime("%d"), 
    a.strftime("%H"), 
    a.strftime("%M")
    )
    return aika    

def tallenna_tulos():
    """"
    Tuottaa tulokset halutussa muodossa ja avaa aiemmat pelitulokset, joihin tiedot syödetään.
    """
    #Muoto jolla tulokset tallennetaan.
    tallennus = {
        tila["pvm"]: [{
        "aika": tila["aika"],
        "taso": tila["taso"],
        "lopputulos": tila["tulos"]
        }]
    }
    try:
        #Tilastot avataan asetuksissa asetetun tiedostonimen perusteella
        with open(aset["tulokset"]) as taulukko:
            #Tallennetaan tilastot tilapäisesti muuttujaan
            aset["tilastot"] = json.load(taulukko)
    except (IOError, json.JSONDecodeError):
        print("Kohdetiedoston avaamisessa tapahtui virhe. Luotiin uusi tiedosto")
    try: 
        with open(aset["tulokset"], "w") as taulukko:
            #Lisätään tilapäiseen muuttujaa tulos
            aset["tilastot"].append(tallennus)
            #Tallennetaan tilapäinen muuttuja tulostiedostoon helposti ihmisen luettavassa muodossa
            json.dump(aset["tilastot"], taulukko, indent=3)
    except IOError:
        print("Kohdetiedoston tallennuksessa tapahtui virhe.")

def nouda_tilastot():
    """
    Pyytää tilastot JSON tiedostosta ja muokkaa ne merkkijonoiksi
    """
    try: 
        #Tilastot avataan asetuksissa asetetun tiedostonimen perusteella
        with open(aset["tulokset"]) as taulukko:
            #Tallennetaan tilastot tilapäisesti muuttujaan
            aset["tilastot"] = json.load(taulukko)
    except (IOError, json.JSONDecodeError):
        print("Kohdetiedoston avaamisessa tapahtui virhe. Luotiin uusi tiedosto")
    aset["tuloslista"] = []
    #Käy läpi JSON muotoisen tilaston ja tekee niistä listan jossa yksi listakohde on merkkijono muotoa ( ajankohta - aika - miinat - tulos )
    for i, _ in enumerate(aset["tilastot"]):
        tulokset = []
        for avain in aset["tilastot"][i]:
            tulokset.append(avain)
        for _ in enumerate(aset["tilastot"][i]):
            for tulos in aset["tilastot"][i][avain]:
                for tulos_avain in tulos:
                    tulokset.append(tulos[tulos_avain])
        #Aika näytetään muodossa mm:ss
        if tulokset[1] >= 59:
            tulokset[1] = str(round(tulokset[1]//60)) + "m" + str(round(tulokset[1]%60)) + "s"
        else:
            tulokset[1] = str(round(tulokset[1])) + "s"
        aset["tuloslista"].append(tulokset[0] + " - Aika: " + str(tulokset[1]) + " Miinoja: " + str(tulokset[2]) + " Tulos: " + tulokset[3])
        


# # # # # # # # # # # # # # #
#                           #
#      Valikon funktiot     #
#                           #
# # # # # # # # # # # # # # #

def uusi_peli(taso):
    """
    Tekee tarvittavat toimenpiteet uuden pelin aloittamiseksi
    """
    #Pelikentän alustaminen ja aloitusajan tallennus
    tila["pvm"] = aikakone()
    tila["maa"] = []
    tila["pinta"] = []
    tila["tyhjat"] = []
    tila["avattu"] = []
    tila["tulos"] = []
    tila["merkit"] = []
    tila["taso"] = taso
    tila["paattynyt"] = False
    aset["valikko"] = False
    aset["larvi"] = "(*_*)"
    #Kentän generoinnin ja miinoituksen kutsuminen
    generaattori()
    miinoita()
    #Nollaa ajastimen
    tila["aika"] = 0

def nayta_tilastot():
    """
    Pyytää tilastot tiedostosta ja tulostaa tilastot ruudulle
    """
    #Pyytää tilastoja
    nouda_tilastot()
    #Piirtää tilastot ruudulle 10 riviä kerrallaan
    #Piirtää ohjeistuksen ja sivunumeron
    haravasto.piirra_tekstia("Selaa painamalla nuolinäppäimiä sivuille ja ESC poistuaksesi", 10, aset["korkeus"] + 10 - 10*40, (255, 255, 255, 255), "serif", 12)
    haravasto.piirra_tekstia("(" + str(aset["tuloslistasivu"]) + "/" + str(len(aset["tuloslista"])//10 + 1) + ")", aset["leveys"] - 80, 10, (255, 255, 255, 180), "serif", 15)
    #Piirtää 10 riviä tuloksia
    for i in range(0, 10):
        #Muuttaa sivunumeron avulla listaindeksin oikeaan muotoon
        j = abs(i + 10 * (aset["tuloslistasivu"] - 1))
            #Jos listakohteita on vähemmän tai samanverran kuin uusi listaindeksi, lopetetaan suorittaminen
        if len(aset["tuloslista"]) <= j:
            return
            #Jos listakohteita on vähemmän tai yhtä paljon kuin indeksi, muokataan indeksistä muotoa listan pituus - 1 jotta siinä ei ole lisättynä numeroa 10
        elif j >= len(aset["tuloslista"]):
            j = len(aset["tuloslista"]) - 1
        #Tulostetaan tulosrivi indeksi on negatiivinen jotta viimeisin tulos näytetään
        haravasto.piirra_tekstia(aset["tuloslista"][-j - 1], 20, aset["korkeus"] + 10 - i*40, (255, 255, 255, 255), "serif", 15)
    return

# # # # # # # # # # # # # # #
#                           #
#    Pelikentän funktiot    #
#                           #
# # # # # # # # # # # # # # #

def digitaalikello(aika):
    """
    Muodostaa ajastimen raakamuodosta muotoa hh:mm:ss ja näyttää tunnit tarpeen mukaan. Parametrina aika.
    """
    #Jos tunti on vaihtumassa
    if round(aika) > 3598 and -1 < (aika - (round(aika/60) * 60)) <= 0:
        return str(round(aika//3600 + 1)).zfill(2) + ":" + str(0).zfill(2) + ":" + str(round(0)).zfill(2)
        #Jos peliä on kestänyt tunnin tai yli
    elif aika >= 3600:
        return str(round(aika//3600)).zfill(2) + ":" + str(round((aika - 3600)//60)).zfill(2) + ":" + str(round(aika%60)).zfill(2)
        #Ensimmäinen minuutti on tulossa täyteen
    elif 59 < round(aika) <= 60:
        return str(round(1)).zfill(2) + ":" + str(round(0)).zfill(2)
        #Jos tunti on vaihtumassa
    elif aika > 60 and -1 < (aika - (round(aika/60) * 60)) <= 0:
        return str(round(aika//60 + 1)).zfill(2) + ":" + str(round(0)).zfill(2)
        #Jos aikaa on kulunut tunnin tai yli
    elif aika >= 59:
        return str(round(aika//60)).zfill(2) + ":" + str(round(aika%60)).zfill(2)
    #Jos aikaa on kulunut alle minuutti
    return "00:" + str(round(aika%60)).zfill(2)

def kello():
    """
    Pyytää kellonajasta digitaalimuotoisen esityksen ja palauttaa sen. Jos peli on päättynyt, käytetään päättymisaikaa.
    """
    if not tila["paattynyt"]:
        return digitaalikello(tila["aika"])
    return digitaalikello(tila["lopetusaika"])

def miinankaivaja(x, y):
    """
    Tarkistaa pelaajan valitseman ruudun
    """
    #Jos peli ei ole päättynyt, käytetään tulvatäyttöä jos valittu piste ei ole miina. 
    #Jos piste on viimeinen avaamaton muu kuin miinaruutu, suoritetaan voittofunktio
    #Jos pisteessä on miina, suoritetaan pelin päättyminen
    if not tila["paattynyt"]:
        if not tila["maa"][y][x] == "x":
            tulvataytto(x, y)
            tila["ihmetys"] = True
            if tila["koko"] - tila["taso"] == len(tila["avattu"]):
                voittaja_voittaja_kanapaivallinen()
        else:
            itsgameoverboiii()

def liputus(x, y):
    """
    Asettaa merkkilipun pelaajan valitsemaan ruutuun
    """
    #Jos peli ei ole päättynyt ja valittu piste on tuntematon, asetetaan tai poistetaan lippu
    if not tila["paattynyt"]:
        if tila["pinta"][y][x] == " ":
            tila["merkit"].append((x, y))
        elif tila["pinta"][y][x] == "f":
            tila["merkit"].remove((x, y))

def generaattori():
    """
    Generoi pelikentän ikkunan koon perusteella
    """
    #Tallennetaan ruutujen määrä
    leveys, korkeus = round(aset["leveys"]/40), round(aset["korkeus"]/40)
    tila["koko"] = leveys * korkeus
    #Luodaan lista jossa yksi kohde edustaa yhtä peliruutua
    for sarake in range(0, korkeus):
        tila["maa"].append([])
        for rivi in range(0, leveys):
            tila["maa"][sarake].append(" ")
            tila["tyhjat"].append((rivi, sarake))

def miinoita():
    """
    Asettaa kentälle vaikeusasteen mukaan miinoja satunnaisiin paikkoihin.
    """
    #Käy miinoitussyklin läpi haluttavan määrän.
    for _ in range(tila["taso"]):
        miinoittamatta = True
        #Yksikkö joka sykkii niin kauan että jokainen miina on upotettu.
        while miinoittamatta:
            #Satunnaisia koordinaatteja miinoittajille.
            x_0 = int(rn.sample(range(0, round(aset["leveys"]/40 - 1)), 1)[0])
            y_0 = int(rn.sample(range(0, round(aset["korkeus"]/40 - 1)), 1)[0])
            #Käy läpi kaikki vapaat ruudut ja kokeilee että onko juuri generoitu koordinaatti vapaa.
            for vapaa in tila["tyhjat"]:
                kohde = (x_0 + 1, y_0 + 1)
                if vapaa == kohde:
                    #Miinoitustyö alkakoon.
                    tila["tyhjat"].remove(kohde)
                    tila["maa"][y_0][x_0] = "x"
                    miinoittamatta = False

def tulvataytto(x, y):
    """
    Tarkistaa ruudussa olevan kohteen sekä sen ympärillä olevat ruudut. 
    Leviää tyhjien ruutujen välityksellä mutta ei voi levitä numeroruuduista eteenpäin. 
    Jos alkuruudussa (x, y) on pommi, ei tehdä mitään ja jos alkuruudun
    ympärillä on pommeja, ei lisää ruutuja avata sen ympäriltä.
    """ 
    #Määritellään alkutilanteeksi seuraava
    jono = [(x, y)]
    while True:
        #Poistetaan käsiteltävien jonosta käsiteltävä piste (x, y)
        #ja lisätään se käsiteltyjen pisteiden listaan
        x, y = jono.pop(0)
        #Tarkistetaan että käsiteltävässä pisteessä (x, y) ei ole pommi
        if (x, y) not in tila["avattu"]:
            tila["avattu"].append((x, y))
            for sarake, pisteet in enumerate(tila["maa"]):
                if sarake in (y - 1, y, y + 1):
                    for rivi, piste in enumerate(pisteet): 
                        #Jos käsiteltävän pisteen ympärillä (x +- 1 / y +- 1 tai x / y) 
                        #tarkarkastettavan pisteen kohdalla 
                        #on miina, lisätään käsiteltävään pisteeseen 1
                        if piste == "x" and rivi in (x, x - 1, x + 1) and sarake in (y, y - 1, y + 1):
                            kohteita = 0
                            try:
                                kohteita = int(tila["maa"][y][x]) + 1
                            except ValueError:
                                kohteita += 1
                            tila["maa"][y][x] = str(kohteita)
            for sarake, pisteet in enumerate(tila["maa"]):
                if sarake in (y - 1, y, y + 1):
                    for rivi, piste in enumerate(pisteet): 
                        #Jos käsiteltävän pisteen (x, y) vieressä on tuntematonta aluetta eikä
                        #käsiteltävä pisteen ympärillä ole miinoja tai ruutua ei ole liputettu,
                        #muutetaan tarkastelussa olevan pisteen (rivi, sarake) tilaksi 0
                        if piste == " " and rivi in (x, x - 1, x + 1) and tila["maa"][y][x] in ("0", " ") and (rivi, sarake) not in tila["merkit"]:
                            tila["maa"][sarake][rivi] = "0"
        #Jos käsiteltävän pisteen (x, y) tila on 0, 
        #käydään läpi sen ympärillä olevat pisteet (x +- 1 / y +- 1 tai x / y) 
        if tila["maa"][y][x] == "0":
            for sarake, pisteet in enumerate(tila["maa"]):
                if sarake in (y - 1, y, y + 1):
                    for rivi, piste in enumerate(pisteet):
                        #Jos tarkastettava piste (rivi, sarake) ei ole vielä käsitelty 
                        #ja sen tila on 0 sekä se ei ole käsittelyssä oleva piste (x, y) tai liputettu ruutu,
                        #se lisätään jonoon
                        if (rivi, sarake) not in tila["avattu"] and (rivi, sarake) not in jono and (rivi, sarake) != (x, y) and piste == "0" and rivi in (x, x - 1, x + 1) and (x, y) not in tila["merkit"]:
                            jono.append((rivi, sarake))
        #Tarkistaa että onko jonossa pisteita, jos ei 
        #niin keskeyttää silmukan ja palauttaa ruudukon
        if not jono:
            return

def itsgameoverboiii():
    """
    Suorittaa pelin loppumiseen liittyvät toimenpiteet
    """
    #Näytetään pelikentällä olevat miinat ja poistetaan liput
    tila["lopetusaika"] = tila["aika"]
    tila["pinta"] = tila["maa"]
    tila["merkit"] = []
    #Pelikentän tilaksi päättynyt
    tila["paattynyt"] = True
    #Asetetaan pelikerran tulokseksi häviö ja tallennetaan pelikerran tiedot
    tila["tulos"] = "Häviö"
    aset["larvi"] = "x_x"
    tallenna_tulos()

def voittaja_voittaja_kanapaivallinen():
    """
    Suorittaa pelin voittoon liittyvät toimenpiteet
    """
    #Näytetään pelikentällä olevat miinat ja poistetaan liput
    tila["lopetusaika"] = tila["aika"]
    #Pelikentän tilaksi päättynyt
    tila["paattynyt"] = True
    #Asetetaan pelikerran tulokseksi häviö ja tallennetaan pelikerran tiedot
    tila["tulos"] = "Voitto"
    aset["larvi"] = "¯\\_(*_ *)_/¯"
    tallenna_tulos()
    

# # # # # # # # # # # # # # #
#                           #
#       Kentän piirto       #
#                           #
# # # # # # # # # # # # # # #

def muuntaja():
    """
    Tuottaa pelikentästä ilmakuvan jossa piilossa olevat miinat eivät näy.
    """
    #Käy pelikentän maanalaisen osan läpi ja muuttaa sen näytettävään muotoon
    tila["pinta"] = []
    for y, sarake in enumerate(tila["maa"]):
        tila["pinta"].append([])
        #Käy läpi sarakkeen jokaisen ruudun.
        for x, ruutu in enumerate(sarake):
            #Yhteensovittaa listaindeksin pelimoottorille luettavaan muotoon.
            #Syöttää käsiteltävän ruudun puskuriin.
            if ruutu == "x":   
                tila["pinta"][y].append(" ")
            else:
                tila["pinta"][y].append(ruutu)
            if tila["pinta"][y][x] == " " and (x, y) in tila["merkit"]:
                tila["pinta"][y][x] = "f"

def ruutudumper():
    """
    Pyytää pelikentästä "ilmakuvan" ja syöttää ruudut piirtoa varten puskuriin.
    """
    if not tila["paattynyt"]:
        muuntaja()
    elif tila["paattynyt"] and tila["tulos"] == "Voitto":
        muuntaja()
    #Käy läpi maan pinnalla näytettävät ruudut
    for y_1, sarake_0 in enumerate(tila["pinta"]):
        #Yhteensovittaa listaindeksin pelimoottorille luettavaan muotoon.
        y_1 = y_1*40
        #Käy läpi sarakkeen jokaisen ruudun.
        for x_1, ruutu_0 in enumerate(sarake_0):
            #Yhteensovittaa listaindeksin pelimoottorille luettavaan muotoon.
            x_1 = x_1*40
            #Syöttää käsiteltävän ruudun puskuriin.
            haravasto.lisaa_piirrettava_ruutu(ruutu_0, x_1, y_1)

def piirra_kentta():
    """
    Käsittelijäfunktio, joka piirtää kaksiulotteisena listana kuvatun miinakentän
    ruudut näkyviin peli-ikkunaan. Funktiota kutsutaan aina kun pelimoottori pyytää
    ruudun näkymän päivitystä.
    """
    haravasto.tyhjaa_ikkuna()
    haravasto.piirra_tausta()
    #Jos valikko on avattuna, tehdään ruudulle piirtäminen sen mukaan. Muulloin piirretään pelikenttä.
    if aset["tulosruutu"]:
        nayta_tilastot()
    elif aset["valikko"]:
        haravasto.piirra_tekstia("MIINAHARAVA", 50, aset["korkeus"] - aset["korkeus"]/10, (255, 255, 255, 255), "serif", 32)
        haravasto.piirra_tekstia("Pelaa valitsemalla vaikeustaso", 50, aset["korkeus"] - aset["korkeus"]/4, (255, 255, 255, 255), "serif", 20)
        haravasto.piirra_tekstia("Helppo", 50, aset["korkeus"] - aset["korkeus"]/3 - 40, (255, 255, 255, 255), "serif", 20)
        haravasto.piirra_tekstia("Keskitaso", 50, aset["korkeus"] - aset["korkeus"]/3 - 75, (255, 255, 255, 255), "serif", 20)
        haravasto.piirra_tekstia("Vaikea", 50, aset["korkeus"] - aset["korkeus"]/3 - 110, (255, 255, 255, 255), "serif", 20)
        haravasto.piirra_tekstia("Tilastoja", 50, aset["korkeus"] - aset["korkeus"]/3 - 170, (255, 255, 255, 255), "serif", 25)
        haravasto.piirra_tekstia("Lopeta tästä tai paina ESC", 50, aset["korkeus"] - aset["korkeus"]/3 - 240, (255, 255, 255, 255), "serif", 20)
    else:
        haravasto.aloita_ruutujen_piirto()
        ruutudumper()
        haravasto.piirra_ruudut()
        haravasto.piirra_tekstia(str(kello()), 10, aset["korkeus"] + 5, (255, 255, 255, 255), "serif", 20)
        haravasto.piirra_tekstia(aset["larvi"], aset["leveys"]/2 - 100, aset["korkeus"] + 5, (255, 255, 255, 255), "serif", 20)
        haravasto.piirra_tekstia("Miinoja jäljellä: " + str(tila["taso"] - len(tila["merkit"])).zfill(2), aset["leveys"] - 225, aset["korkeus"] + 5, (255, 255, 255, 255), "serif", 20)

# # # # # # # # # # # # # # #
#                           #
#  Pääohjelman kutsuminen   #
#                           #
# # # # # # # # # # # # # # #

main()