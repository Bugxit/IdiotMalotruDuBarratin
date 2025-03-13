"""
FICHIER DE GESTION DE LA BDD IMDB

Classe principale : BDDBIGBOSS
"""

import mysql.connector
import signal

class TimeoutException(Exception):
    """
    Classe vide qui crée une Exception "personalisé" pour gérer le timeout
    """
    pass

def timeout_handler(signum, frame):
    """
    Fonction qui appelle la classe d'Exception custom si trop long
    """
    raise TimeoutException("Database lookup took too long")

class DBBIGBOSS:
    """
    Classe principale qui gère la connexion et les requetes à la BDD
    """
    def __init__(self):
        # 
        self.conn = mysql.connector.connect(host="localhost",user="elevelocal", database="imdb")
        
    def lookup(self, name):
        """
        Fonction qui permet de trouver des couples id - titres selon un titre
        Trié par similarité et nombres de votes
        """
        # Génère un signal, appel qui lance le timeout
        signal.signal(signal.SIGALRM, timeout_handler)
        # Met le temps de timeout à 10 secondes
        signal.alarm(10)

        try:
            # Boucle TRY pour tester le timeout
            cursor = self.conn.cursor()
            query = """
            SELECT work_basics.id_work, primaryTitle
            FROM work_basics
            JOIN work_ratings ON work_ratings.id_work = work_basics.id_work
            WHERE worktype LIKE 'tvSeries' AND primaryTitle LIKE %s
            ORDER BY work_ratings.numVotes DESC
            LIMIT 10;
            """
            cursor.execute(query, (f"%{name}%",))
            lignes = cursor.fetchall()
            return lignes
        except TimeoutException as e:
            # Timeout
            raise RuntimeError("Lookup timed out") from e
        finally:
            # Réinistialise le TO
            signal.alarm(0)
        
    def episodeList(self, idd):
        """
        Fonction qui permet de récupérer toutes les données de votes à partir d'un identifitant IMDB
        """
        reponse = []
        cursor = self.conn.cursor()
        query = "\
        SELECT work_episode.seasonNumber, work_ratings.averageRating, work_akas.title\
        FROM work_basics JOIN work_episode ON work_basics.id_work = work_episode.id_work_parent\
        JOIN work_ratings ON work_ratings.id_work = work_episode.id_work\
        JOIN work_akas ON work_akas.id_work = work_episode.id_work\
        WHERE worktype LIKE 'tvSeries' AND work_akas.isOriginalTitle = 1 AND work_basics.id_work = %s\
        ORDER BY work_episode.seasonNumber, work_episode.episodeNumber\
        "
        cursor.execute(query, (idd,))
        lignes = cursor.fetchall()
        for ligne in lignes:
            reponse.append(ligne)
        self.conn.commit()
        return reponse

db = DBBIGBOSS()
