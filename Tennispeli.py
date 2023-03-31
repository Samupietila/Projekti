##############################################################################
#MODUULIT

import mysql.connector
import datetime
import random

##############################################################################
#FUNKTIOT

def kayttajanvalinta():#Määritetään käyttäjä pelin aluksi
    global nimi
    kursori = yhteys.cursor()
    while True:
        print("Oletko uusi vai vanha käyttäjä?")
        kayttaja = input("Valitse vaihtoehto käyttäen numeroa: 1. Vanha käyttäjä 2. Uusi käyttäjä\n")
        if kayttaja == "1":
            nimi = input("Syötä nimesi:\n")
            haekayttaja = "SELECT screenname, `date`, funds FROM kayttaja WHERE screenname ='" + nimi + "'"
            kursori.execute(haekayttaja)
            tulos1 = kursori.fetchall()
            if kursori.rowcount == 0:
                print("Käyttäjää ei löytynyt, tarkista oikeinkirjoitus. Vai haluatko luoda uuden käyttäjän?")
            elif kursori.rowcount > 0:
                for rivi in tulos1:
                    print(f"Käyttäjänimesi: {rivi[0]} \nPelipäivä: {rivi[1]} \nPelitilin saldo: {rivi[2]} €")
                break
        elif kayttaja == "2":
            nimi = input("Syötä nimesi:\n")
            #Tarkistetaan, onko nimi jo olemassa tietokannassa
            #Jos nimi löytyy, ei tallenneta
            nimitulos = nimentarkistus()
            if nimitulos:
                print(f'Nimi "{nimi}" on jo käytössä, ole hyvä ja kokeile toista nimeä. Vai haluatko käyttää jo luotua '
                      f'käyttäjää?')
                print()
            else:
                luokayttaja = "INSERT INTO kayttaja (`screenname`,`date`,`funds`, usedfunds)VALUES ('" + nimi + "','03.01.2022','1000','0.0')"
                kursori.execute(luokayttaja)
                naytatiedot = "SELECT screenname, `date`, funds FROM kayttaja WHERE screenname ='" + nimi + "'"
                kursori.execute(naytatiedot)
                tulos2 = kursori.fetchall()
                for rivi in tulos2:
                    print(f"Käyttäjänimesi: {rivi[0]} \nPelipäivä: {rivi[1]} \nPelitilin saldo: {rivi[2]} €")
                break
        else:
            print(f"Virheellinen vastaus, ole hyvä ja yritä uudelleen.")
    return nimi



def saldontarkistus():#Hakee käyttäjän pelisaldon
    kursori = yhteys.cursor()
    tarkistus = "SELECT funds FROM kayttaja WHERE screenname ='" + nimi + "'"
    kursori.execute(tarkistus)
    saldo = kursori.fetchall()
    for i in saldo:
        rahat = (f"{i[0]}")
        rahat = float(rahat)
    return rahat

def isfloat(num):#Tarkistaa onko str-syöte liukuluku
    try:
        float(num)
        return True
    except ValueError:
        return False

def panoksentarkistus():#Kysyy panoksen suuruuden ja tarkistaa syötteen sopivuuden, päivittää lyötyjen vetojen summan
    cursor = yhteys.cursor()
    tarkistus = "SELECT funds FROM kayttaja WHERE screenname ='" + nimi + "'"
    cursor.execute(tarkistus)
    tulos = cursor.fetchall()
    for i in tulos:
        tili = i[0]
    while True:
        if tili < 25:
            panos = tili
            print("Varasi ovat alle 25 €, joten panokseksi asetetaan "+str(tili)+"€")
            break
        panos = (input(f"Valitse panoksesi suuruus euroina (maksimipanoksesi on {str(tili)} €):\n"))
        if isfloat(panos) == True:
            panos = float(panos)
            if panos >= 25:
                if panos <= tili:
                    sql = "UPDATE kayttaja set usedfunds = '" + str(panos) + "'+ usedfunds where screenname = '" + nimi + "';"
                    cursor.execute(sql)
                    break
                elif panos > tili:
                    print("Riittämättömät varat, saldosi on: "+str(tili))
            else:
                print("Minimipanos on 25 €, ole hyvä ja yritä uudelleen.")
        else:
            print("Virheellinen vastaus, yritä uudelleen.")
    return panos



def pvmmuuttaja():#Muuttaa pelaajan päivämäärän seuraavaan pelipäivään ja päivittää uuden päivämäärän tietokantaan
    A = True
    x = kayttajanhaku(nimi)
    for i in x:
        pvm_1a = (f"{i[1]}")
    pvm_1a = datetime.datetime.strptime(pvm_1a, "%d.%m.%Y")
    pvm_1a = pvm_1a + datetime.timedelta(days=+1)
    pvm_1b = pvm_1a.strftime("%d.%m.%Y")
    while True:
        cursor = yhteys.cursor()
        sql = "SELECT date from turnaus where date = '" + pvm_1b + "'"
        cursor.execute(sql)
        tulos = cursor.fetchall()
        if tulos == []:
            pvm_1a = pvm_1a + datetime.timedelta(days=+1)
            pvm_1b = pvm_1a.strftime("%d.%m.%Y")
        else:
            cursor = yhteys.cursor()
            sql = "UPDATE kayttaja SET date = '"+pvm_1b+"' where screenname = '"+nimi+"'"
            cursor.execute(sql)
            break
        if pvm_1a > datetime.datetime(2022, 11, 20):
            sql = "UPDATE kayttaja SET date = '21.11.2022' where screenname = '"+nimi+"'"
            cursor.execute(sql)
            A = False
            break
    return A

def kayttajanhaku(nimi):#Hakee tietokannasta kaikki tiedot pelaajasta ID:tä lukuunottamatta
    cursor = yhteys.cursor()
    kayttajanimi = "Select screenname, date, funds from kayttaja where screenname ='"+nimi+"';"
    cursor.execute(kayttajanimi)
    tulos = cursor.fetchall()
    return tulos


def aamutervehdys():#Kertoo pelaajalle päivämäärän sekä pelitilin saldon
    tiedot = kayttajanhaku(nimi)#Käyttää hyväksi toista funktiota, joka hakee jo käyttäjäntiedot
    for i in tiedot:
        print(f"Huomenta {i[0]}! Päivämäärä tänään on {i[1]} ja pelitilisi saldo on {i[2]}€")
    return



def kierratystarkistus():#Tarkistaa onko kierrätysehto toteutunut
    cursor = yhteys.cursor()
    tarkistus = "SELECT usedfunds FROM kayttaja WHERE screenname ='" + nimi + "'"
    cursor.execute(tarkistus)
    tulos = cursor.fetchall()
    for i in tulos:
        pelatutrahat = (f"{i[0]}")
        pelatutrahat = str(pelatutrahat)
    return pelatutrahat



def turnaushaku():#Hakee nykyisenä päivänä käynnissä olevat turnaukset
    cursor = yhteys.cursor()
    x = kayttajanhaku(nimi)
    for i in x:
        pvm = (f"{i[1]}")
    sql = f"select tournament, series, ATP from turnaus where date = '"+pvm+"';"
    cursor.execute(sql)
    tulos = cursor.fetchall()
    lista = []
    for i in tulos:
        lista.append(f"({i[2]}) {i[0]}, {i[1]}")
    numero = 0
    printti = lista[numero]
    while numero < len(lista):
        if printti == lista[numero]:
            numero += 1
        elif printti != lista[numero]:
            print(printti)
            printti = lista[numero]
    print(printti)
    lista.clear()
    return



def otteluhaku(kehote):#Hakee valitun turnauksen ja päivän ottelut ja satunnaistaa esittämisjärjestyksen
    cursor = yhteys.cursor()
    sql1 = f"SELECT winner, wrank, avgw, loser, lrank, avgl, game.gameid FROM game,turnaus,kayttaja " \
           f"WHERE game.gameid = turnaus.gameid AND turnaus.date = kayttaja.date AND kayttaja.screenname = " \
           f"'"+nimi+"' " "and atp = '"+kehote+"';"
    cursor.execute(sql1)
    tulos = cursor.fetchall()
    for i in tulos:
        pelaaja1 = (f" (Sijoitus {i[1]}) Pelaaja {i[0]} [Kerroin {i[2]}]")
        pelaaja2 = (f" (Sijoitus {i[4]}) Pelaaja {i[3]} [Kerroin {i[5]}]")
        numero = random.randint(0,1)
        if numero == 0:
            print(f"[{i[6]}] {pelaaja1} {pelaaja2}")
        if numero != 0:
            print(f"[{i[6]}] {pelaaja2} {pelaaja1}")
    return tulos



def pelihaku(ottelunumero,kehote):#Hakee valitun ottelun pelaajat, satunnaistaa esittämisjärjestyksen ja kysyy ketä veikataan
    cursor = yhteys.cursor()
    sql = f"SELECT winner, wrank, avgw, loser, lrank, avgl, game.gameid FROM game,turnaus,kayttaja " \
           f"WHERE game.gameid = turnaus.gameid AND turnaus.date = kayttaja.date AND kayttaja.screenname = " \
           f"'"+nimi+"' " "and atp = '"+kehote+"' and game.gameid ='"+ottelunumero+"';"
    cursor.execute(sql)
    tulos = cursor.fetchall()
    while True:
        if tulos == []:
            veikattupelaaja = []
        else:
            for i in tulos:
                pelaaja1 = f"   Rank {i[1]} Player {i[0]} voittokerroin on: ({i[2]})"
                pelaaja2 = f"   Rank {i[4]} Player {i[3]} voittokerroin on: ({i[5]})"
                numero = random.randint(0,1)
                if numero == 0:
                    print("(1)"+pelaaja1)
                    print("(2)"+pelaaja2)
                    print()
                    while True:
                        voittajaveikkaus = input("Valitse pelaaja jonka voiton puolesta haluat veikata syöttämällä"
                                                 " pelaajaa vastaava numero:\n")
                        if voittajaveikkaus.isnumeric() == True:
                            if voittajaveikkaus == '1':
                                veikattupelaaja = tulos[0][0]
                                break
                            elif voittajaveikkaus == '2':
                                veikattupelaaja = tulos[0][3]
                                break
                            else:
                                print('Virheellinen vastaus, yritä uudelleen.')
                        else:
                            print('Virheellinen vastaus, yritä uudelleen.')
                elif numero !=0:
                    print("(1)"+pelaaja2)
                    print("(2)"+pelaaja1)
                    while True:
                        voittajaveikkaus = input("Valitse pelaaja jonka voiton puolesta haluat veikata syöttämällä "
                                                 "pelaajaa vastaava numero:\n")
                        if voittajaveikkaus.isnumeric() == True:
                            if voittajaveikkaus == "1":
                                veikattupelaaja = tulos[0][3]
                                break
                            elif voittajaveikkaus == "2":
                                veikattupelaaja = tulos[0][0]
                                break
                            else:
                                print('Virheellinen vastaus, yritä uudelleen.')
                        else:
                            print('Virheellinen vastaus, yritä uudelleen.')
        return veikattupelaaja



def veikkaus(ottelunumero,panos,voittajaveikkaus,kehote):#laskee voitetut/hävityt rahat
    kursori = yhteys.cursor()
    sql = "Select winner, wrank, avgw, game.gameid FROM game,turnaus,kayttaja Where game.gameid = turnaus.gameid"
    sql += " and turnaus.date = kayttaja.date and kayttaja.screenname ='"+nimi+"' and atp ='"+kehote+"'"
    sql += "AND turnaus.gameid ='"+ottelunumero+"' ;"
    kursori.execute(sql)
    tulos = kursori.fetchall()
    for i in tulos:
        if i[0][0] == voittajaveikkaus:
            kerroin = i[2]
            kerroin2 = kerroin.replace(",",".")
            voitto = float(panos) * float(kerroin2)
            voitto = round(voitto, 2)
            print("Onnittelut! Voitit "+str(voitto)+" €")
            rahat = saldontarkistus()
            uusisaldo = float(voitto) + rahat - float(panos)
            print("Uusi saldosi on " + str(round(uusisaldo,2)) + " €")
        else:
            print('Valitettavasti veikkauksesi meni väärin. Hävisit', panos, "€.")
            rahat = saldontarkistus()
            uusisaldo = rahat - float(panos)
            if uusisaldo != 0:
                print("Uusi saldosi on " + str(round(uusisaldo,2)) + " €")
    sql = "UPDATE kayttaja set funds = '"+ str(uusisaldo) +"' where screenname = '" + nimi + "';"
    kursori.execute(sql)
    return uusisaldo



def nimentarkistus():#Tarkistaa onko syötetty käyttäjänimi vapaana
    kursori = yhteys.cursor()
    nimihaku = "SELECT * FROM kayttaja WHERE screenname = '" + nimi + "'"
    kursori.execute(nimihaku)
    tulos = kursori.fetchone()
    return tulos



def charity(saldo): #Tallentaa pelaajan nykyisen saldon hyväntekeväisyyteen. saldo = charity(saldo)
    kursori = yhteys.cursor()
    sql = "SELECT name,id,website from charity"
    kursori.execute(sql)
    tulos = kursori.fetchall()
    print("Mihin hyväntekeväisyyteen haluat lahjoittaa rahasi?")
    for i in tulos:
        print(f"{i[1]}. {i[0]}, {i[2]}")
    valinta = input("Valintasi: ")
    while True:
        if valinta == "1":
            break
        elif valinta == "2":
            break
        elif valinta == "3":
            break
        elif valinta == "4":
            break
        elif valinta == "5":
            break
        else:
            print("Virheellinen vastaus, yritä uudelleen.")
            for i in tulos:
                print(f"{i[1]}. {i[0]}")
            valinta = input("Valintasi: ")
    sql = "SELECT name from charity where id = '" + valinta + "'"
    kursori.execute(sql)
    tulos1 = kursori.fetchall()
    valinta = tulos1[0][0]
    sql = "UPDATE charity "
    sql += "SET funds = funds + " + saldo + " "
    sql += "WHERE name = '" + valinta + "'"
    kursori.execute(sql)
    saldo = "0.0"
    return saldo

def gameover():#Lopettaa pelin ja poistaa käyttäjän kun rahat loppuvat kesken
    print('"Annan toisten mä talletella suuret setelit..." Pelisaldosi on näköjään tyhjä. Noh, parempi onni ensi '
          'kerralla. Kiitos pelaamisesta!')
    print("GAME OVER")
    kursori = yhteys.cursor()
    sql = "DELETE from kayttaja where screenname = '" + nimi + "'"
    kursori.execute(sql)
    return

def gameover2(nimi):#Lopettaa pelin ja poistaa käyttäjän kun rahat on lahjoitettu rahansa hyväntekeväisyyteen
    kursori = yhteys.cursor()
    sql = "SELECT name,funds,website from charity"
    kursori.execute(sql)
    tulos = kursori.fetchall()
    print("Kiitos paljon lahjoituksestasi!")
    print()
    print("Tällä hetkellä näihin hyväntekeväisyyksiin on lahjoitettu tämän verran rahaa:")
    for c in tulos:
        print(f"{c[0]} = {c[1]}")
    sql = "DELETE from kayttaja where screenname = '" + nimi + "'"
    kursori.execute(sql)
    print()
    print("Kiitos pelaamisesta!")
    return

##############################################################################
#PÄÄOHJELMA
#Yhteys MySQL:ään
yhteys = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='tennispeli',
    user='root',
    password='cussword',
    autocommit=True
    )
pelilopetus = False
print("Tervetuloa tenniksen vedonlyöntipeliin!")
print()
input('(Jatka painamalla Enter-näppäintä)\n')
print('Tennispeli on vedonlyöntisimulaattori, jossa lyöt vetoa vuoden aikana pelattavista miesten ATP-liiton kaksinpelin'
      ' tennisotteluiden voittajista.\nPelin alussa saat 1000 € saldoa pelitilillesi. Sinun tulee lyödä joka pelipäivänä '
      'vetoa yhdestä haluamastasi ottelusta.\nKun olet käyttänyt alussa saamasi rahasumman kymmenkertaisesti, sinulla on '
      'jokaisen pelipäivän alussa mahdollisuus lahjoittaa\npelitilisi varat johonkin valitsemistamme hyväntekeväisyyskohteis'
      'ta, ja lopettaa peli!\nVoit myös halutessasi pelata läpi koko vuoden pelipäivät, mutta muista että jos pelitililt'
      'äsi loppuvat varat, häviät pelin.')
print()
input('(Jatka painamalla Enter-näppäintä)\n')
print('Tennispelissä navigoit valitsemalla pelin esittämistä vaihtoehdoista haluamasi syöttämällä vaihtoehtoa vastaavan'
      ' numeron tekstikenttään,\nja painamalla sen jälkeen Enter-näppäintä.\nOttelua valitessasi peli esittää sinulle pel'
      'aajien sen hetkiset maailmanlistansijoitukset (Rank),\nsekä ottelukohtaiset voittokertoimet (Factor).\nPelitilisi '
      'saldon ollessa alle 25 €, panostat seuraavaan kohteeseen kaikki jäljellä olevat pelivarasi.')
print()
input('Aloita peli painamalla Enter-näppäintä!\n')
print()

nimi = kayttajanvalinta()
while True:
        pelisaldo = saldontarkistus()
        pelisaldo = str(pelisaldo)
        if pelisaldo == "0.0":
            gameover()
            break
        kierratys = kierratystarkistus()
        kierratys = float(kierratys)
        if kierratys >= 10000.0:
            while True:
                kierratysvalinta = input("Olet kierrättänyt vaaditun rahamäärän.\n(1) Jatka vielä pelaamista "
                                         "\n(2) Lahjoita rahasi (" + str(pelisaldo) + " €) haluamaasi hyväntekeväisyyteen ja lopeta peli\n")
                if kierratysvalinta == "1":
                    print("Selvä, jatketaan siis voittamista!")
                    print()
                    break
                elif kierratysvalinta == "2":
                    charity(pelisaldo)
                    print('')
                    gameover2(nimi)
                    pelilopetus = True
                    break
                else:
                    print('Virheellinen vastaus, yritä uudelleen.')
        if pelilopetus == True:
            break
        aamutervehdys()
        print()
        print("Tänään ovat käynnissä nämä turnaukset: ")
        while True:
            turnaushaku()
            print()
            turnausnumero = input("Valitse turnaus josta haluat lyödä vetoa syöttämällä turnausta vastaava numero:\n")
            ottelu = otteluhaku(turnausnumero)
            if ottelu == []:
                print("Virheellinen vastaus, yritä uudelleen.")
            else:
                print()
                print(f'Kiitos! Yllä tämän päivän kohteet.')
                while True:
                    ottelunumero = input('Valitse kohde josta haluat lyödä vetoa syöttämällä ottelua vastaava numero:\n')
                    if ottelunumero.isnumeric() == True:
                        pelaajat = pelihaku(ottelunumero, turnausnumero)
                        if pelaajat == []:
                            print("Virheellinen vastaus, yritä uudelleen.")
                        else:
                            break
                    else:
                        print('Virheellinen vastaus, yritä uudelleen.')
                break
        tarkistettu_panos = panoksentarkistus()
        saldo = veikkaus(ottelunumero,tarkistettu_panos,pelaajat[0],turnausnumero)
        pelisaldo = saldontarkistus()
        pelisaldo = str(pelisaldo)
        if pelisaldo == "0.0":
            gameover()
            break
            print()
        input('Jatka seuraavaan päivään painamalla Enter-näppäintä\n')
        pvm = pvmmuuttaja()
        if pvm == False:
            print()
            print('Olet pelannut vuoden 2022 turnaukset loppuun! Onneksi olkoon!')
            print('Nyt voit lahjoittaa hankkimat rahasi mieleiseen hyväntekeväisyyskohteeseen!')
            charity(pelisaldo)
            gameover2(nimi)
            break