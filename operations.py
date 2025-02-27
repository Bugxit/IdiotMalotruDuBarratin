import mysql.connector


class DBBIGBOSS:
    def __init__():
        self.conn = mysql.connector.connect(host="localhost",user="elevelocal", database="imdb")
    def getMovieData(movie):
        cursor = self.conn
        cursor.execute("SELECT originalTitle, startYear, numVotes FROM work_basics JOIN work_ratings USING (id_work) WHERE worktype LIKE 'movie' AND originalTitle = '?' ORDER BY numVotes DESC LIMIT 10;", (movie))
        lignes = cursor.fetchall()
        for ligne in lignes:
            print(ligne)
        conn.close()