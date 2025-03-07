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

os.system("clear")
console = Console()

def loader(num=1000):
    """
    Fonction illisible qui génère le spinner.
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
    - create() qui permet d'ajouter un contact
    - delete() qui permet de supprimer un contact
    - show() qui affiche tout les contacts
    - search() qi fonctionne comme show mais avec un argument
    """

    def __init__(self, data=None):
        os.system("clear")
        console.print(ascii_art, justify="center", style="bold green")
        if data:
            console.print(data, justify="center", style=green_bold)
        console.print('🔍 Film que vous cherchez', justify="center")
        print()
        a = input("     > ")
        self.search(a)

    def search(self, name):
        try:
            with console.status("[bold green]", spinner = 'dots12') as status:
                result = operations.db.lookup(name)
            table = Table(show_header=True, header_style="bold green", expand=True)
            table.add_column("🎬 Nom du Film", style="dim", width=50, justify="center")
            table.add_column("🆔 Identifiant", style="dim", width=20, justify="center")
            for line in result:
                table.add_row(
                    str(line[1]),
                    str(line[0]),
                )
            os.system("clear")
            console.print(ascii_art, justify="center", style="bold green")
            console.print(table, justify="center")
            print()
            console.print('🆔 Identifiant du film', justify="center")
            print()
            a = input("     > ")
            self.image(a)
        except RuntimeError or operations.TimeoutException:
            os.system("clear")
            console.print(ascii_art, justify="center", style="bold green")
            console.print('🔥 Timeout - Requete trop longue!', justify="center",style=danger)
    
    def image(self, id):
        with console.status("[bold green]", spinner = 'dots12') as status:
            path = f"/var/www/html/images/{id}"
            query_res = operations.db.episodeList(id)
            name, rating = logic.format_ratings_name(query_res)
            logic.generate_image_series(rating, name, path)

        os.system(f"firefox /var/www/html/images/{id}.png")

loader()
Menu()
