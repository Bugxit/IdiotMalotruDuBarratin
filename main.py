import logic
import operations

import sys

if __name__ == "__main__":
    argc = len(sys.argv)
    if argc < 2: exit(1)
    
    id = sys.argv[1]

    path = f"/var/www/html/images/{id}"
    
    query_res = operations.db.episodeList(id)
    name, rating = logic.format_ratings_name(query_res)
    logic.generate_image_series(rating, name, path)

"""
Vert : #3f6212
Orange: #f97316
Jaune: #fde047
""" 
