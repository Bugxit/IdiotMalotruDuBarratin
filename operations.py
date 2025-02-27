import mysql.connector


class DBBIGBOSS:
    def __init__():
        self.conn = mysql.connector.connect(host="localhost",user="elevelocal", database="imdb")
    def getMovieDataByName(name):
        cursor = self.conn
        cursor.execute("SELECT originalTitle, startYear, numVotes FROM work_basics JOIN work_ratings USING (id_work) WHERE worktype LIKE 'movie' AND originalTitle = '?' ORDER BY numVotes DESC LIMIT 10;", (name))
        lignes = cursor.fetchall()
        for ligne in lignes:
            print(ligne)
        conn.close()
    def getMovieData(idée):
        cursor = self.conn
        cursor.execute("SELECT originalTitle, startYear, numVotes FROM work_basics JOIN work_ratings USING (id_work) WHERE worktype LIKE 'movie' AND idWork = '?' ORDER BY numVotes DESC LIMIT 10;", (idée))
        lignes = cursor.fetchall()
        for ligne in lignes:
            print(ligne)
        conn.close()