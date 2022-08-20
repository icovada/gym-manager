import itertools
from operator import iconcat

# GLOBALI
LISTA_ISCRITTI = []
LISTA_TRAINER = []
LISTA_CORSI = []


class Corso(object):
    id = itertools.count()

    def __init__(self, nome, prezzo, max_iscritti):
        self.id = next(self.id)
        self.nome = nome
        self.trainer = []
        self.prezzo = prezzo
        self.max_iscritti = max_iscritti
        self.iscritti = []

    def visualizza(self):
        print("Nome del corso: ", self.nome)
        print("Prezzo: ", self.prezzo)
        print("Elenco trainer: ", self.trainer)
        print("Numero massimo di iscritti: ", self.max_iscritti)
        print("posti disponibili: ", self.max_iscritti-len(self.iscritti))

    def agg_iscritto(self, ogg_iscritto):
        self.iscritti.append(ogg_iscritto.id)
        ogg_iscritto.corsi.append(self.id)

    def agg_trainer(self, ogg_trainer):
        self.trainer.append(ogg_trainer.id)
        ogg_trainer.corsi.append(self.id)

    def rimuovi_iscritto(self, ogg_iscritto):
        self.iscritti.remove(ogg_iscritto.id)
        ogg_iscritto.corsi.remove(self.id)

    def rimuovi_trainer(self, ogg_trainer):
        self.trainer.remove(ogg_trainer.id)
        ogg_trainer.corsi.remove(self.id)


class Iscritto(object):
    id = itertools.count()

    def __init__(self, nome, cognome, numero, eta):
        self.id = next(self.id)
        self.nome = nome
        self.cognome = cognome
        self.numero = numero
        self.eta = eta
        self.corsi = []

    def visualizza(self):
        print("Nome iscritto: ", self.nome, self.cognome)
        print("Numero di telefono: ", self.numero)
        print("Età: ", self.eta)
        print("Frequenta i corsi: ", self.corsi)  # lista dei corsi?

    def agg_corso(self, corso):
        # passare se stesso all'oggetto corso scelto sfruttado la sua funzione
        corso.agg_iscritto(self)

    def rimuovi_corso(self, corso):
        corso.rimuovi_iscritto(self)


class Trainer(object):
    id = itertools.count()

    def __init__(self, nome, cognome, numero):
        self.id = next(self.id)
        self.nome = nome
        self.cognome = cognome
        self.numero = numero
        self.corsi = []

    def visualizza(self):
        print("Nome Trainer: ", self.nome, self.cognome)
        print("Numero di telefono: ", self.numero)
        print("Gestisce i corsi: ", self.corsi)

    def agg_corso(self, corso):
        # passare se stesso all'oggetto corso scelto sfruttado la sua funzione
        corso.agg_trainer(self)

    def rimuovi_corso(self, corso):
        corso.rimuovi_trainer(self)


def table_corso():
    print("ID".rjust(4), "NOME".ljust(15))
    for i in LISTA_CORSI:
        print(str(i.id).rjust(4), i.nome.ljust(15))


def table_trainer():
    print("ID".rjust(4), "NOME".ljust(
        15),  "COGNOME".ljust(15))
    for i in LISTA_TRAINER:
        print(str(i.id).rjust(4), i.nome.ljust(
            15), i.cognome.ljust(15))


def table_iscritto():
    print("ID".rjust(4), "NOME".ljust(
        15),  "COGNOME".ljust(15))
    for i in LISTA_ISCRITTI:
        print(str(i.id).rjust(4), i.nome.ljust(
            15), i.cognome.ljust(15))


def trova_oggetto(id, lista):
    obj = None
    for i in lista:
        if i.id == int(id):
            obj = i
            break
    return obj


def main():
    while True:
        domanda = input('''
                    __________________________________________________
                                    PYTHON FIT
                    __________________________________________________

                            Benvenuto su PYTHON FIT!

                            Ecco cosa puoi fare:
                            #quando io creo un trainer, non gli assegno già un corso???
                            1. Inserire nuova utenza nel database
                            2. Modifica dati utenza
                            3. Cancella dati
                            4. Iscrivere a corso
                            5. Aggiungere organizzatore corso
                            6. uscire

                            COSA SCEGLI? ''')
        if domanda == "1":  # Inserimento dati
            finito = False
            while not finito:
                # come mettere a capo?
                answer = input(
                    """Cosa vuoi agiungere al database?
                    A -> ISCRITTO
                    B -> TRAINER
                    C -> CORSO
                    D -> ESCI

-> """)

                if answer.lower() == "a":
                    nome = input("Inserisci nome iscritto: ")
                    cognome = input("Inserisci cognome iscritto: ")
                    numero = input("Inserisci numero iscritto: ")
                    eta = int(input("Inserisci età iscritto: "))
                    istanza = Iscritto(nome, cognome, numero, eta)
                    LISTA_ISCRITTI.append(istanza)

                elif answer.lower() == "b":
                    nome = input("Inserisci nome trainer: ")
                    cognome = input("Inserisci cognome trainer: ")
                    numero = input("Inserisci numero trainer: ")
                    istanza = Trainer(nome, cognome, numero)
                    LISTA_TRAINER.append(istanza)

                elif answer.lower() == "c":
                    nome = input("Inserisci nome del nuovo corso: ")
                    prezzo = input("Inserisci prezzo lezione: ")
                    n_max = int(
                        input("Inserire numero massimo delle partecipazioni: "))
                    istanza = Corso(nome, prezzo, n_max)
                    LISTA_CORSI.append(istanza)

                elif answer.lower() == "d":
                    finito = True

        if domanda == "2":  # Modifica dati
            finito = False
            while not finito:
                # come mettere a capo?
                answer = input(
                    """Cosa vuoi modificare del database?
                    A -> ISCRITTO
                    B -> TRAINER
                    C -> CORSO
                    D -> esci

-> """)
                if answer.lower() == "a":
                    table_iscritto()

                    local_id = int(
                        input("Inseriire ID dell'iscritto da modificare "))

                    iscritto = trova_oggetto(local_id, LISTA_ISCRITTI)

                    if iscritto is None:
                        print("Iscritto non esistente")
                        continue

                    new_name = input(
                        "Inserisci nome modificato, altrimenti * ")
                    if new_name != "*":
                        iscritto.nome = new_name

                    new_surn = input(
                        "Inserisci cognome modificato, altrimenti * ")
                    if new_surn != "*":
                        iscritto.cognome = new_surn

                    new_numb = input(
                        "Inserisci numeoro modificato, altrimenti * ")
                    if new_numb != "*":
                        iscritto.numero = new_numb

                    new_age = input(
                        "Inserisci età, altrimenti * ")
                    if new_age != "*":
                        iscritto.eta = new_age

                elif answer.lower() == "b":
                    table_trainer()

                    local_id = int(
                        input("Inseriire ID del trainer da modificare "))
                    trainer = trova_oggetto(local_id, LISTA_TRAINER)

                    if trainer is None:
                        print("Utenza non esistente")
                        continue

                    new_name = input(
                        "Inserisci nome modificato, altrimenti * ")
                    if new_name != "*":
                        trainer.nome = new_name

                    new_surn = input(
                        "Inserisci cognome modificato, altrimenti * ")
                    if new_surn != "*":
                        trainer.cognome = new_surn

                elif answer.lower() == "c":
                    table_corso()

                    local_id = int(
                        input("Inseriire ID del corso da modificare "))
                    corso = trova_oggetto(local_id, LISTA_CORSI)

                    if corso is None:
                        print("Corso non esistente")
                        continue

                    new_name = input(
                        "Inserisci nome modificato, altrimenti * ")
                    if new_name != "*":
                        corso.nome = new_name

                    new_price = input(
                        "Inserisci prezzo modificato, altrimenti * ")
                    if new_price != "*":
                        corso.prezzo = new_price

                    new_sub = input(
                        "Inserisci iscritti massimi, altrimenti * ")
                    if new_sub != "*":
                        corso.max_iscritti = int(new_sub)
                elif answer.lower() == "d":
                    finito = True

        if domanda == "3":
            finito = False
            while not finito:

                answer = input(
                    """Cosa vuoi cancellare del database?
                    A -> ISCRITTO
                    B -> TRAINER
                    C -> CORSO
                    D -> esci

-> """)
                if answer.lower() == "a":
                    table_iscritto()

                    local_id = int(
                        input("Inseriire ID dell'iscritto da cancellare "))

                    iscritto = trova_oggetto(local_id, LISTA_ISCRITTI)

                    if iscritto is None:
                        print("Iscritto non esistente")
                        continue

                    for id_corso in iscritto.corsi:
                        ogg_corso = trova_oggetto(id_corso, LISTA_CORSI)
                        ogg_corso.rimuovi_iscritto(iscritto)

                    LISTA_ISCRITTI.remove(iscritto)

                elif answer.lower() == "b":
                    table_trainer()

                    local_id = int(
                        input("Inseriire ID del trainer da cancellare "))

                    trainer = trova_oggetto(local_id, LISTA_TRAINER)

                    if trainer is None:
                        print("Trainer non esistente")
                        continue

                    for id_corso in trainer.corsi:
                        ogg_corso = trova_oggetto(id_corso, LISTA_CORSI)
                        ogg_corso.rimuovi_trainer(trainer)

                    LISTA_TRAINER.remove(trainer)

                elif answer.lower() == "c":
                    table_corso()

                    local_id = int(
                        input("Inseriire ID del corso da cancellare "))

                    corso = trova_oggetto(local_id, LISTA_CORSI)

                    if corso is None:
                        print("Corso non esistente")
                        continue

                    for i in corso.iscritti:
                        iscritto = trova_oggetto(i, LISTA_ISCRITTI)
                        iscritto.rimuovi_corso(corso)

                    for i in corso.trainer:
                        trainer = trova_oggetto(i, LISTA_TRAINER)
                        trainer.rimuovi_corso(corso)

                    LISTA_CORSI.remove(corso)

                elif answer.lower() == "d":

                    finito = True

        if domanda == "4":
            table_iscritto()
            sub_id = input("Inserire ID dell'utente da iscrivere ")
            sub_obj = trova_oggetto(sub_id, LISTA_ISCRITTI)

            table_corso()
            corso_id = input("Inserire ID corso ")
            corso_obj = trova_oggetto(corso_id, LISTA_CORSI)

            corso_obj.agg_iscritto(sub_obj)

        if domanda == "5":
            table_corso()
            corso_id = input("Inserire ID corso ")
            corso_obj = trova_oggetto(corso_id, LISTA_CORSI)

            table_trainer()
            trainer_id = input("Inserire ID del trainer da aggiungere ")
            trainer_obj = trova_oggetto(trainer_id, LISTA_TRAINER)

            corso_obj.agg_trainer(trainer_obj)

        if domanda == "6":
            print("Ciao e grazie per essere stato con PYTHON FIT! A presto!")
            # TODO: Salvare i dati
            break


if __name__ == "__main__":
    main()
