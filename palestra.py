from typing import Dict
from objects import TrainingClass, Member, Trainer, ObjectTable


def main(members_list, trainers_list, training_class_list):
    pass


    
def old():    
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
    members_list = ObjectTable()
    trainers_list = ObjectTable()
    training_class_list = ObjectTable()
    main(members_list, trainers_list, training_class_list)
