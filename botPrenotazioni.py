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

            for date in posti.split("data")[1:]:
                dataLezione = date[3:date.find(',') - 1].replace("\\", "")

                if not (data["giorno"].__len__() == 0 or data["giorno"].__contains__(dataLezione)):
                    continue

                for lezione in date.split("nome")[1:]:
                    if data["debug"]:
                        print()
                    # Prendiamo il nome
                    nome = lezione[3:lezione[3:].find('"') + 3].strip()
                    if data["debug"]:
                        print("Lezione: " + nome, end='. ')

                    # Nome lezione
                    if not (data["lezioni"].__len__() == 0 or data["lezioni"].__contains__(nome)):
                        if data["debug"]:
                            print("Lezione scartata", end='')
                        continue

                    prenotata = lezione.split("prenotata")[1][:8].__contains__("true")

                    # Se è stata prenotata
                    if prenotata:
                        if data["debug"]:
                            print("Lezione già prenotata", end='')
                        continue

                    disponibile = lezione.split("prenotabile")[1][:8].__contains__("true")

                    # Se è disponibile
                    if not disponibile:
                        if data["debug"]:
                            print("Lezione non disponibile", end='')
                        continue

                    # Ricaviamo l'id della prenotazione
                    idString = lezione.split("entry_id")[1]
                    idPrenotazione = idString[2:idString.find(',')]
                    if data["debug"]:
                        print("Prenotazione in corso, id = " + idPrenotazione, end='. ')

                    # Creiamo la prenotazione, ritorna true se è avvenuta con successo
                    if creaPrenotazione(idPrenotazione, data["CF"]):
                        if data["debug"]:
                            print("Prenotazione avvenuta con successo", end='')
                        else:
                            print("Prenotazione avvenuta alla lezione " + nome + " con id " + str(id))
                    # Errore prenotazione
                    elif data["debug"]:
                        print("Si è riscontrato un errore durante la prenotazione", end='')
                    else:
                        print("E' stato riscontrato un problema durante la prenotazione della lezione " + nome + " con id " + str(id))


            print("\nIterazione finita, pausa")
            time.sleep(data["delay"])
        else:
            print("Nessuna lezione trovata, forse il cookie è sbagliato (?)")
            break
