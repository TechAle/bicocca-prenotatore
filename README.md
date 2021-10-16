# Bicocca Prenotatore
Un bot per prenotare automaticamente le lezioni
## Perchè?
Siccome le lezioni della pini sono impossibili da prenotare; se ritardi anche solamente di 2 minuti tutti i 90 posti vengono occupati istantaneamente.<br>
## Come utilizzarlo
1) installare python 3.9
2) Scaricare la repository
3) pip install requirements.txt
4) Aprire gestioneorari, fare il login e dopo, (firefox) click destro -> analizza -> rete cercare il pacchetto index.php (dovrebbe essere il primo) e, nel suo header, copiare l'attributo Cookie.
5) Incollare il Cookie nel file data.json insieme al tuo codice fiscale nella rispettiva riga.
6) python botPrenotazioni.py<br>
N.b. le lezioni di default in data.json sono di informatica T1 triennale quindi, ameno che non ti interessano, cambiale con quelle desiderate.