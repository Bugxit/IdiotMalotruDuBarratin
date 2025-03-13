from rich.console import Console
from rich.table import Table
from rich.style import Style
from rich.progress import track
from rich.align import Align
import os
import time
import sqlite3
import operations
import logic



# Variables utilisés par les interfaces
danger = Style(color="red", blink=True, bold=True)
ascii_art ='''
 _______  _______  _______  _______  __   __  _______        ______   _______ 
|       ||   _   ||       ||       ||  | |  ||       |      |      | |  _    |
|       ||  |_|  ||       ||_     _||  | |  ||  _____|      |  _    || |_|   |
|       ||       ||       |  |   |  |  |_|  || |_____       | | |   ||       |
|      _||       ||      _|  |   |  |       ||_____  |      | |_|   ||  _   | 
|     |_ |   _   ||     |_   |   |  |       | _____| |      |       || |_|   |
|_______||__| |__||_______|  |___|  |_______||_______|      |______| |_______|

🌵 🌵 🌵
'''

# Initialisation de la console et de l'interface riche 
os.system("clear")
console = Console()


def loader(num=1000):
    """
    Fonction illisible qui génère la boucle de chargement.

    num: int -> Quantité en NanoTickS de boucles
    """
    os.system("clear")
    console.print(ascii_art, justify="center", style="bold green")
    tasks = [f"task {n}" for n in range(1, num)]
    with console.status("[bold green]", spinner = 'point') as status:
        while tasks:
            console.print("", justify="center", end="")
            task = tasks.pop(0)
            time.sleep(0.001)
    os.system("clear")

class Menu:
    
    """
    Classe princpal de l'application

    Enfants :
    - search(name) : affiche les résultats de la rcherche dans la db IMDB pour l'agument name
    - image(id) : affiche une boucle de chargement et génère l'image de la série id.
    """

    def __init__(self, data=None):
        # Style
        os.system("clear")
        console.print(ascii_art, justify="center", style="bold green")
        if data:
            console.print(data, justify="center", style=green_bold)
        console.print('🔍 Film que vous cherchez', justify="center")
        print()
        # Demande un titre de film.
        # Si l'input contient id=, le programme cherche directement l'image pour cet identifiant.
        a = input("     > ")
        if a[:3] == "id=":
            self.image(a[3:])
        else:
            self.search(a)

    def search(self, name):
        # le TRY gère le timeout de la base de donnée. L'IMDB c'est pas mal grand.
        try:
            # Affiche une animation pendant que la bdd travaille
            with console.status("[bold green]", spinner = 'dots12') as status:
                result = operations.db.lookup(name)
            # Crée un tableau pour mettre toute les données
            table = Table(show_header=True, header_style="bold green", expand=True)
            table.add_column("🎬 Nom du Film", style="dim", width=50, justify="center")
            table.add_column("🆔 Identifiant", style="dim", width=20, justify="center")
            for line in result:
                table.add_row(
                    str(line[1]),
                    str(line[0]),
                )
            # Style
            os.system("clear")
            console.print(ascii_art, justify="center", style="bold green")
            console.print(table, justify="center")
            print()
            console.print('🆔 Identifiant du film', justify="center")
            print()
            a = input("     > ")
            self.image(a)
        except RuntimeError or operations.TimeoutException:
            # Affiche une erreur en cas de Timeout sur la bdd
            os.system("clear")
            console.print(ascii_art, justify="center", style="bold green")
            console.print('🔥 Timeout - Requete trop longue!', justify="center",style=danger)
    
    def image(self, id):
        # Affiche une animation de chargement pendant la génération
        with console.status("[bold green]", spinner = 'dots12') as status:
            # Cherche & Trouve
            path = f"/var/www/html/images/{id}"
            query_res = operations.db.episodeList(id)
            name, rating = logic.format_ratings_name(query_res)
            logic.generate_image_series(rating, name, path)
        # Ouvre l'image dans Firefox. Merci Linux.
        os.system(f"firefox /var/www/html/images/{id}.png")

loader()
Menu()
