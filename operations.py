import mysql.connector


class DBBIGBOSS:
    def __init__(self):
        self.conn = mysql.connector.connect(host="localhost",user="elevelocal", database="imdb")
    def getMovieDataByName(self, name):
        cursor = self.conn.cursor()
        cursor.execute("SELECT originalTitle, startYear, numVotes FROM work_basics JOIN work_ratings USING (id_work) WHERE worktype LIKE 'movie' AND originalTitle = '?' ORDER BY numVotes DESC LIMIT 10;", (name))
        lignes = cursor.fetchall()
        for ligne in lignes:
            print(ligne)
    def getMovieDataById(self, idd):
        print(idd)
        cursor = self.conn.cursor()
        query = "SELECT originalTitle, startYear, numVotes FROM work_basics JOIN work_ratings USING (id_work) WHERE worktype LIKE 'movie' AND id_work = %s ORDER BY numVotes DESC LIMIT 10;"
        cursor.execute(query, (idd,))
        lignes = cursor.fetchall()
        for ligne in lignes:
            print(ligne)
        self.conn.commit()
    def episodeList(self, idd):
        print(idd)
        reponse = []
        cursor = self.conn.cursor()
        query = "\
        SELECT work_episode.seasonNumber, work_episode.episodeNumber, work_ratings.averageRating, work_akas.title\
        FROM work_basics JOIN work_episode ON work_basics.id_work = work_episode.id_work_parent\
        JOIN work_ratings ON work_ratings.id_work = work_episode.id_work_parent\
        JOIN work_akas ON work_akas.id_work = work_episode.id_work\
        WHERE worktype LIKE 'tvSeries' AND work_akas.isOriginalTitle = 1 AND work_basics.id_work = %s;\
        "
        cursor.execute(query, (idd,))
        lignes = cursor.fetchall()
        for ligne in lignes:
            reponse.append(ligne)
        print(reponse)
        self.conn.commit()
        return reponse
db = DBBIGBOSS()
db.episodeList("0903747")