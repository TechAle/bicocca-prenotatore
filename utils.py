import requests
from bs4 import BeautifulSoup

# Il nostro url
url = "https://gestioneorari.didattica.unimib.it/PortaleStudentiUnimib/index.php?view=prenotalezione&include=prenotalezione&_lang=it"

# L'header che dobbiamo passare al sito web
header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:93.0) Gecko/20100101 Firefox/93.0",
          "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
          "Accept-Language": "it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3",
          "Accept-Encoding": "gzip, deflate, br",
          "Referer": "https://gestioneorari.didattica.unimib.it/PortaleStudentiUnimib/index.php?view=homepage&include=&_lang=it&login=1",
          "DNT": "1",
          "Connection": "keep-alive",
          "Cookie": "",
          "Upgrade-Insecure-Requests": "1",
          "Sec-Fetch-Dest": "document",
          "Sec-Fetch-Mode": "navigate",
          "Sec-Fetch-Site": "same-origin",
          "Sec-Fetch-User": "?1"}


# Funzione per creare le prenotazioni
def creaPrenotazione(idLezione, CF):
    result = requests.get(
        "https://gestioneorari.didattica.unimib.it/PortaleStudentiUnimib/call_ajax.php?mode=salva_prenotazioni&"
        "codice_fiscale=" + CF + "&id_entries="
                                 "[" + idLezione + "]&id_btn_element=" + idLezione,
        # Teoricamente non serve autenticarsi per fare una prenotazione però, credo che prima o poi fixeranno questo bug.
        headers=header)
    if result.status_code == 200:
        if result.text.__contains__("Success"):
            return True
    return False


def cancellaLezione(idLezione, CF):
    # Non metto l'header siccome questo funzione proprio perchè non controllano i cookie/sessione
    result = requests.get(
        "https://gestioneorari.didattica.unimib.it/PortaleStudentiUnimib/call_ajax.php?mode=cancella_prenotazioni&codice_fiscale=" + CF + "&id_entries=[" + idLezione + "]&id_btn_element=" + idLezione)
    if result.status_code == 200:
        if result.text.__contains__("Success"):
            return True
    return False


# Funzione per prendere le varie lezioni prenotabili
def getListaPrenotazioni():
    # Prendiamo il codice sorgente
    soup = BeautifulSoup(requests.get(url, headers=header).text, features="lxml")

    for script in soup.find_all('script'):
        # Prendiamo la sezione dove si trovano le nostre lezioni
        if str(script).__contains__("var lezioni_prenotabili"):
            return script
    return ""
