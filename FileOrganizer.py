# Importo tutti i pacchetti necessari

import os
import shutil
import csv
import numpy as np
from PIL import Image
from tabulate import tabulate
import argparse

########## Inizio STEP 1 ##########

path = os.path.abspath('files')
os.chdir(path)
# Mi assicuro di essere nel giusto path

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
        return None

# Creo le varie directory e file recap, se non esistono prima
for sottocartella in ['audio', 'images', 'docs']:
    if not os.path.isdir(sottocartella):
        os.mkdir(sottocartella)

if not os.path.isfile("recap.csv"):
    with open('recap.csv', 'w', newline='') as csvfile:
        fieldnames = ['name', 'type', 'size(B)']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()


# Inizio il ciclo sulla cartella files
cartella, sottocartelle, files = next(os.walk(path))
print("File spostati:\n")

# Apro il file recap
with open('recap.csv', 'a', newline='') as csvfile:
    fieldnames = ['name', 'type', 'size(B)']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    for file in files:
        file_size = os.path.getsize(f"{cartella}\\{file}")
        nome, estensione = os.path.splitext(os.path.basename(file))
        tipo = check_tipo(estensione)

# A mano a mano che vengono spostati, stampo le reletive info
        if tipo == "doc":
            shutil.move(f"{path}\\{file}", f"{path}\\docs")
            print(f"name: {nome} \t type: {tipo} \t size: {file_size}B")
        elif tipo == "audio":
            shutil.move(f"{path}\\{file}", f"{path}\\audio")
            print(f"name: {nome} \t type: {tipo} \t size: {file_size}B")
        elif tipo == "image":
            shutil.move(f"{path}\\{file}", f"{path}\\images")
            print(f"name: {nome} \t type: {tipo} \t size: {file_size}B")
        else:
            print(f"Il file {file} presenta un'estensione non supportata, non verrà quindi spostato")

# Aggiorno il file di recap
        writer.writerow({'name': nome, 'type': tipo, 'size(B)': file_size})

########## Fine STEP 1 ##########

########## STEP 2 in addfile.py ##########

########## Inizio STEP 3 ##########

# Cambio il path su cui lavorare

path = os.path.abspath('images')
os.chdir(path)

cartella, sottocartelle, files = next(os.walk(path))

# Inizio col definire la table dove verranno inseriti i vari record da stampare
table = {"Name": [], "Height": [], "Width": [], "Grayscale": [], "R": [], "G": [], "B": [], "ALPHA": []}

for image in files:
    nome, estensione = os.path.splitext(os.path.basename(image))
    img = Image.open(image)
    np_img = np.array(img)
    shape = np_img.shape
    dim = np_img.ndim
# Di default tutte le immagini hanno un nome e le due grandezze base x altezza
    table["Name"].append(nome)
    table["Height"].append(shape[0])
    table["Width"].append(shape[1])
# Aggiungo i restanti dati in base al tipo di immagine
    if dim == 2:
        media_colore = round(np.mean(np_img),2)
        table["Grayscale"].append(media_colore)
        table["R"].append(0)
        table["G"].append(0)
        table["B"].append(0)
        table["ALPHA"].append(0)
    else:
        if shape[2] == 3:
            table["Grayscale"].append(0)
            rgb = [round(x,2) for x in (np.mean(np.mean(np_img, axis=0), axis=0))]
            table["R"].append(rgb[0])
            table["G"].append(rgb[1])
            table["B"].append(rgb[2])
            table["ALPHA"].append(0)
        elif shape[2] == 4:
            table["Grayscale"].append(0)
            rgba = [round(x,2) for x in (np.mean(np.mean(np_img, axis=0), axis=0))]
            table["R"].append(rgba[0])
            table["G"].append(rgba[1])
            table["B"].append(rgba[2])
            table["ALPHA"].append(rgba[3])
        else:
            print(f"L'immagine {image} presenta una scala di colori non supportata")
# Stampo la tabella che prende come "riferimento" le chiavi del dizionario sopra creato
print(tabulate(table, headers='keys', tablefmt='fancy_grid'))

########## Fine STEP 3 ##########
