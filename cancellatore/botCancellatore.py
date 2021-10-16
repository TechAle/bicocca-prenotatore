# Librerie
import re
import json
import time
from utils import *


# I dati del nostor file dati.json
data = json.load(open("dati.json", "r"))
header["Cookie"] = data["cookie"]

if __name__ == "__main__":

    while True:

        lista = getListaPrenotazioni()

        # Se abbiamo delle lezioni
        if lista.__len__() > 0:
            # Prendiamo tutto ciò che è fra le parentesi
            posti = re.compile('JSON.parse\(.*\)').search(str(lista)).group(0)
            # Facciamo uno split per ogni "nome" -> Le varie lezioni
            for lezione in posti.split("nome")[1:]:
                idString = lezione.split("entry_id")[1]
                idPrenotazione = idString[2:idString.find(',')]
                if cancellaLezione(idPrenotazione, data["CF"]):
                    print("Cancellata lezione " + " id = " + idPrenotazione )
        else:
            print("Nessuna lezione trovata, forse il cookie è sbagliato (?)")
            break
