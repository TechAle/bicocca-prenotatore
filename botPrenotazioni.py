import requests
from bs4 import BeautifulSoup
import re
import json
import time

data = json.load(open("data.json", "r"))

url = "https://gestioneorari.didattica.unimib.it/PortaleStudentiUnimib/index.php?view=prenotalezione&include=prenotalezione&_lang=it"

header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:93.0) Gecko/20100101 Firefox/93.0",
          "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
          "Accept-Language": "it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3",
          "Accept-Encoding": "gzip, deflate, br",
          "Referer": "https://gestioneorari.didattica.unimib.it/PortaleStudentiUnimib/index.php?view=homepage&include=&_lang=it&login=1",
          "DNT": "1",
          "Connection": "keep-alive",
          "Cookie": data["cookie"],
          "Upgrade-Insecure-Requests": "1",
          "Sec-Fetch-Dest": "document",
          "Sec-Fetch-Mode": "navigate",
          "Sec-Fetch-Site": "same-origin",
          "Sec-Fetch-User": "?1"}

debug = True


def creaprenotazione(idLezione):
    result = requests.get(
        "https://gestioneorari.didattica.unimib.it/PortaleStudentiUnimib/call_ajax.php?mode=salva_prenotazioni&"
        "codice_fiscale=" + data['CF'] + "&id_entries="
                                         "[" + idLezione + "]&id_btn_element=" + idLezione)
    if result.status_code == 200:
        if result.text.__contains__("Success"):
            return True
    return False


if __name__ == "__main__":

    while True:
        soup = BeautifulSoup(requests.get(url, headers=header).text, features="lxml")

        lista = ""

        for script in soup.find_all('script'):
            if str(script).__contains__("var lezioni_prenotabili"):
                lista = script
                break

        if lista.__len__() > 0:
            posti = re.compile('JSON.parse\(.*\)').search(str(lista)).group(0)
            for lezione in posti.split("nome")[1:]:
                nome = lezione[3:lezione[3:].find('"') + 3].strip()
                if debug:
                    print("Lezione: " + nome, end='. ')
                if data["lezioni"].__contains__(nome):
                    prenotata = lezione.split("prenotata")[1][:8].__contains__("true")
                    if not prenotata:
                        disponibilita = lezione.split("prenotabile")[1][:8].__contains__("true")
                        if disponibilita:
                            idString = lezione.split("entry_id")[1]
                            idPrenotazione = idString[2:idString.find(',')]
                            if debug:
                                print("Prenotazione in corso, id = " + idPrenotazione, end='. ')
                            if creaprenotazione(idPrenotazione):
                                if debug:
                                    print("Prenotazione avvenuta con successo", end='')
                                else:
                                    print("Prenotazione avvenuta alla lezione " + nome + " con id " + str(id))
                            elif debug:
                                print("Si è riscontrato un errore durante la prenotazione", end='')
                            else:
                                print(
                                    "E' stato riscontrato un problema durante la prenotazione della lezione " + nome + " con id " + str(
                                        id))
                        elif debug:
                            print("Lezione piena", end='')
                    elif debug:
                        print("Lezione già prenotata", end='')
                elif debug:
                    print("Lezione scartata", end='')
                print()

            print("Iterazione finita, pausa")
            time.sleep(data["delay"])
