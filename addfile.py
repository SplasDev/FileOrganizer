# STEP 2

# Importo i 4 pacchetti

import os
import shutil
import csv
import argparse

# Mi assicuro di essere nel giusto path

path = os.path.abspath('files')
os.chdir(path)


# Fisso le varie estensioni possibili
type_docs = [".txt", ".odt", ".doc", ".docx", ".pdf"]
type_images = [".png", ".jpg", ".jpeg", ".jpe"]
type_audio = [".mp3", ".wav"]

# Funzione che collega l'estensione al tipo di file
def check_tipo(type):
    if type in type_docs:
        return "doc"
    elif type in type_images:
        return "image"
    elif type in type_audio:
        return "audio"
    else:
        return "altro"


# Creo le varie directory e file recap, se non esistono prima
if not os.path.isdir("docs"):
    os.mkdir("docs")

if not os.path.isdir("audio"):
    os.mkdir("audio")

if not os.path.isdir("images"):
    os.mkdir("images")

if not os.path.isfile("recap.csv"):
    with open('recap.csv', 'w', newline='') as csvfile:
        fieldnames = ['name', 'type', 'size(B)']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()


# Creo la "CLI" aggiungendo il parametro obbligatorio file
parser = argparse.ArgumentParser(description="Piccolo script che sposta un singolo file nella sottocartella di competenza")
parser.add_argument("file", type=str, help="Nome del file da spostare, estensione compresa")
args = parser.parse_args()


cartella, sottocartelle, files = next(os.walk(path))
file = args.file
message = f"Il file {file} è stato spostato correttamente"
if file in files:
    file_size = os.path.getsize(f"{cartella}\\{file}")
    nome, estensione = os.path.splitext(os.path.basename(file))
    tipo = check_tipo(estensione)
# Eseguo spostamento
    if tipo == "doc":
        shutil.move(f"{path}\\{file}", f"{path}\\docs")
        print(message)
    elif tipo == "audio":
        shutil.move(f"{path}\\{file}", f"{path}\\audio")
        print(message)
    elif tipo == "image":
        shutil.move(f"{path}\\{file}", f"{path}\\images")
        print(message)

# Aggiorno il file di recap
    with open('recap.csv', 'a', newline='') as csvfile:
        fieldnames = ['name', 'type', 'size(B)']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'name': nome, 'type': tipo, 'size(B)': file_size})
else:
    print(f"File {file} non trovato")
