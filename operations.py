import mysql.connector

class DBBIGBOSS:
    def __init__(self):
        self.conn = mysql.connector.connect(host="localhost",user="elevelocal", database="imdb")
    def lookup(self, name):
        cursor = self.conn.cursor()
        query = "\
        SELECT work_basics.id_work, primaryTitle\
        FROM work_basics\
        JOIN work_ratings ON work_ratings.id_work = work_basics.id_work\
        WHERE worktype LIKE 'tvSeries' AND primaryTitle LIKE %s\
        ORDER BY work_ratings.numVotes DESC\
        LIMIT 20;\
        "
        cursor.execute(query, (f"%{name}%",))
        lignes = cursor.fetchall()
        return lignes
        
    def episodeList(self, idd):
        print(idd)
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
