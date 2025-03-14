import dessin
import colorsys

WORST_GRADE = (0, 0, 0)
BEST_GRADE = (10, 10, 10)
WORST_GRADE_RGB = (217, 249, 157)
BEST_GRADE_RGB = (26, 46, 16)

def hsl_to_rgb(h, s, l):
    r, g, b = colorsys.hls_to_rgb(h/360, l/100, s/100)
    return (int(r*255), int(g*255), int(b*255))

def note_to_rgb(note):
    return hsl_to_rgb(note*10, 100, 40)

def affine_function(x1, x2, y1, y2):
    # returns an affine function which goes through (x1, y1) & (x2, y2)
    return lambda x : (y2 - y1) / (x2 - x1) * (x - x2) + y2

def color_function(startABS, endABS, startIMG, endIMG):
    # returns an affine function which goes throught (startABS, endABS) & (startIMG, endIMG)
    slope_0 = ( endIMG[0] - startIMG[0] ) / ( endABS[0] - startABS[0] )
    slope_1 = ( endIMG[1] - startIMG[1] ) / ( endABS[1] - startABS[1] )
    slope_2 = ( endIMG[2] - startIMG[2] ) / ( endABS[2] - startABS[2] )
    return lambda x1 : (slope_0 * (x1 - startABS[0]) + startIMG[0], slope_1 * (x1 - startABS[1]) + startIMG[1], slope_2 * (x1 - startABS[2]) + startIMG[2])

def rgb_dec_hex(r=0, g=0, b=0):
    # converts rgb to text using "#RRGGBB" hex formating
    r_hex = str(hex(int(r)))[2:4] + ("0" if r < 16 else "")
    g_hex = str(hex(int(g)))[2:4] + ("0" if g < 16 else "")
    b_hex = str(hex(int(b)))[2:4] + ("0" if b < 16 else "")

    return f"#{r_hex}{g_hex}{b_hex}"

def draw_background(image_size):
    # Changes the color ever row of the image
    bg_color_f = color_function((0, 0, 0), (image_size, image_size, image_size), (200, 250, 40), (200, 100, 40))
    for y in range(image_size):
        r, g, b = bg_color_f(y)
        row_color = rgb_dec_hex(r, g, b)
        dessin.color(row_color)
        dessin.ligne(0, y, image_size, y)

    dessin.color("black")

def draw_season_average(number_of_season, season_average):
    # Draws bases (name, rectange)
    x_text = number_of_season * 62.5
    dessin.ecrire(x_text, 100, "Season average", align="center", font_size=40, font_type="bold")
    dessin.rect_fill(25, 375, number_of_season * 125 - 25, 50, col="white")

    draw_x = 25

    # Make sure no division by 0 occures 
    max_avg, min_avg = max(season_average), min(season_average)
    if max_avg == min_avg:
        max_avg += .1
    height_f = affine_function(min_avg, max_avg, 100, 200)
    color_f = color_function(WORST_GRADE, BEST_GRADE, WORST_GRADE_RGB, BEST_GRADE_RGB)

    # Draws for every season
    for s_avg in season_average:
        graph_height = height_f(s_avg)
        r, g, b = note_to_rgb(s_avg)
        graph_color = rgb_dec_hex(r, g, b)

        dessin.rect_fill(draw_x, 325, 100, graph_height, graph_color)
        dessin.ecrire(draw_x + 50, 365 - graph_height, s_avg, align="center")

        draw_x += 125

def draw_rating_per_episode(rating_tab, number_of_season, lowest_rated, highest_rated):
    draw_x, draw_y = number_of_season * 125 + 200, 125
    color_f = color_function(WORST_GRADE, BEST_GRADE, WORST_GRADE_RGB, BEST_GRADE_RGB)

    # Draws every episode / season in squares
    dessin.rect_fill(draw_x - 50, 175, 50, 50, "black")
    for s_num in range(number_of_season):
        # Make sure season number is on top
        dessin.rect_fill(draw_x, 175, 50, 50,"black")
        dessin.ecrire(draw_x + 10, 165, s_num+1, col="white")
        draw_y = 225
        # Draws every episode of the season
        for e_num, e_rating in enumerate(rating_tab[s_num]):
            # Make sure episode number is on the left
            dessin.rect_fill(number_of_season * 125 + 150, draw_y, 50, 50,"black")
            dessin.ecrire(number_of_season * 125 + 152, draw_y - 10, e_num+1, col="white")

            r, g, b = note_to_rgb(e_rating)
            graph_color = rgb_dec_hex(r, g, b)

            dessin.rect_fill(draw_x, draw_y, 50, 50, graph_color)
            dessin.ecrire(draw_x + 12, draw_y - 15, e_rating, font_size=20, font_type="bold")
            draw_y += 50
        draw_x += 50
    
def draw_best_worst_5(number_of_season, lowest_rated, highest_rated):
    x_text = number_of_season * 62.5
    dessin.ecrire(x_text, 500, "Best & Worst 5 episodes", align="center", font_size=40, font_type="bold")

    # Draws the outline
    dessin.rect_fill(25, 570, number_of_season * 125 - 25, 30, "black")
    dessin.ecrire(27, 567, "Pos", col="white", font_size=20)
    dessin.ecrire(90, 567, "N°S", col="white", font_size=20)
    dessin.ecrire(150, 567, "N°E", col="white", font_size=20)
    dessin.ecrire(210, 567, "/10", col="white", font_size=20)
    dessin.ecrire(280, 567, "Title", col="white", font_size=20)

    draw_y = 600
    color_f = color_function(WORST_GRADE, BEST_GRADE, WORST_GRADE_RGB, BEST_GRADE_RGB)

    # For every best & worst episode write it in the board
    for letter, arr in [("H", highest_rated), ("L", lowest_rated)]:

        for index, e in enumerate(arr):

            # get bg row color
            r, g, b = note_to_rgb(e[1])
            graph_color = rgb_dec_hex(r, g, b)
            dessin.rect_fill(25, draw_y, number_of_season * 125 - 25, 30, graph_color)

            dessin.ecrire(27, draw_y, f"{letter}#{index+1}", font_size=20)
            dessin.ecrire(90, draw_y, e[0][0]+1, font_size=20)
            dessin.ecrire(150, draw_y, e[0][1]+1, font_size=20)
            dessin.ecrire(210, draw_y, e[1], font_size=20)
            dessin.ecrire(280, draw_y, e[2], font_size=20)

            draw_y += 30

def get_infos(rating_tab, name_tab):
    # Gives back every essential info from the ratings and names
    number_of_season = len(rating_tab)
    season_average = list(map(lambda l : round(sum(l) / len(l), 2), rating_tab))
    max_episode_number = len(max(rating_tab, key=len))

    # t = tab of all episodes
    t = [((i,j), rating_tab[i][j], name_tab[i][j]) for i in range(len(rating_tab)) for j in range(len(rating_tab[i]))]
    t.sort(key=lambda e : e[1])

    lowest_rated = t[:5]
    highest_rated = t[-5:]
    highest_rated.reverse()

    return number_of_season, season_average, max_episode_number, lowest_rated, highest_rated

def draw(rating_tab, number_of_season, season_average, max_episode_number, lowest_rated, highest_rated, output_path="output"):
    # Make sure everything fits 
    image_size = max(number_of_season * 175 + 250, 50 * max_episode_number + 225, 1000)

    # Sets (0, 0) to the top left of the screen
    dessin.wn.setup(image_size, image_size)
    dessin.wn.setworldcoordinates(0, image_size, image_size, 0)
    dessin.ht()

    draw_background(image_size)
    draw_season_average(number_of_season, season_average)
    draw_rating_per_episode(rating_tab, number_of_season, lowest_rated, highest_rated)
    draw_best_worst_5(number_of_season, lowest_rated, highest_rated)

    dessin.save_image(output_path)

def generate_image_series(rating_tab, name_tab, output_path="output"):

    number_of_season, season_average, max_episode_number, lowest_rated, highest_rated = get_infos(rating_tab, name_tab)
    draw(rating_tab, number_of_season, season_average, max_episode_number, lowest_rated, highest_rated, output_path)

def format_ratings_name(query_result):
    rating_tab = [[]]
    name_tab = [[]]

    prob_season = 1
    for work_snum, work_rating, work_title in query_result:
        work_snum, work_rating = int(work_snum), float(work_rating)
        # Check if the query changed season
        if work_snum == prob_season + 1:
            prob_season += 1
            rating_tab.append([])
            name_tab.append([])

        # Make sure query did not skip a season
        if work_snum != prob_season:
            break

        rating_tab[work_snum - 1].append(work_rating)
        name_tab[work_snum - 1].append(work_title)

    return name_tab, rating_tab
