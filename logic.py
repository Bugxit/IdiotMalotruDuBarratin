import dessin

def affine_function(x1, x2, y1, y2):
    return lambda x : (y2 - y1) / (x2 - x1) * (x - x2) + y2

def g_to_hex_color(g, f):
    e = int(f(g))
    str_hex = str(hex(e))[2:4]
    return f"#00{str_hex}00"

def draw_background(image_size):
    bg_color_f = affine_function(0, image_size, 250, 100)
    for y in range(image_size):
        row_color = f"#DC{hex(int(bg_color_f(y)))[2:]}28"
        dessin.color(row_color)
        dessin.ligne(0, y, image_size, y)

    dessin.color("black")

def draw_season_average(number_of_season, season_average):
    x_text = number_of_season * 62.5
    dessin.ecrire(x_text, 100, "Season average", align="center", font_size=40, font_type="bold")
    dessin.rect_fill(25, 375, number_of_season * 125 - 25, 50, col="white")

    draw_x = 25

    max_avg, min_avg = max(season_average), min(season_average)
    height_f = affine_function(min_avg, max_avg, 100, 200)
    color_f = affine_function(min_avg, max_avg, 200, 100)

    for s_avg in season_average:
        graph_height = height_f(s_avg)
        graph_color  = g_to_hex_color(s_avg, color_f)

        dessin.rect_fill(draw_x, 325, 100, graph_height, graph_color)
        dessin.ecrire(draw_x + 50, 365 - graph_height, s_avg, align="center")

        draw_x += 125

def draw_rating_per_episode(rating_tab, number_of_season, lowest_rated, highest_rated):
    draw_x, draw_y = number_of_season * 125 + 200, 125
    color_f = affine_function(lowest_rated[0][1], highest_rated[0][1], 200, 100)

    dessin.rect_fill(draw_x - 50, 175, 50, 50, "black")
    for s_num in range(number_of_season):
        dessin.rect_fill(draw_x, 175, 50, 50,"black")
        dessin.ecrire(draw_x + 10, 165, s_num+1, col="white")
        draw_y = 225
        for e_num, e_rating in enumerate(rating_tab[s_num]):
            dessin.rect_fill(number_of_season * 125 + 150, draw_y, 50, 50,"black")
            dessin.ecrire(number_of_season * 125 + 152, draw_y - 10, e_num+1, col="white")

            graph_color = g_to_hex_color(e_rating, color_f)
            dessin.rect_fill(draw_x, draw_y, 50, 50, graph_color)
            dessin.ecrire(draw_x + 12, draw_y - 15, e_rating, font_size=20, font_type="bold")
            draw_y += 50
        draw_x += 50
    
def draw_best_worst_5(number_of_season, lowest_rated, highest_rated):
    x_text = number_of_season * 62.5
    dessin.ecrire(x_text, 500, "Best & Worst 5 episodes", align="center", font_size=40, font_type="bold")

    dessin.rect_fill(25, 570, number_of_season * 125 - 25, 30, "black")
    dessin.ecrire(27, 567, "Pos", col="white", font_size=20)
    dessin.ecrire(90, 567, "N°S", col="white", font_size=20)
    dessin.ecrire(150, 567, "N°E", col="white", font_size=20)
    dessin.ecrire(210, 567, "/10", col="white", font_size=20)
    dessin.ecrire(280, 567, "Title", col="white", font_size=20)

    draw_y = 600
    color_f = affine_function(lowest_rated[0][1], highest_rated[0][1], 200, 100)

    for letter, arr in [("H", highest_rated), ("L", lowest_rated)]:

        for index, e in enumerate(arr):

            graph_color = g_to_hex_color(e[1], color_f)
            dessin.rect_fill(25, draw_y, number_of_season * 125 - 25, 30, graph_color)

            dessin.ecrire(27, draw_y, f"{letter}#{index+1}", font_size=20)
            dessin.ecrire(90, draw_y, e[0][0]+1, font_size=20)
            dessin.ecrire(150, draw_y, e[0][1]+1, font_size=20)
            dessin.ecrire(210, draw_y, e[1], font_size=20)
            dessin.ecrire(280, draw_y, e[2], font_size=20)

            draw_y += 30

def get_infos(rating_tab, name_tab):
    number_of_season = len(rating_tab)
    season_average = list(map(lambda l : round(sum(l) / len(l), 2), rating_tab))
    max_episode_number = len(max(rating_tab, key=len))

    t = [((i,j), rating_tab[i][j], name_tab[i][j]) for i in range(len(rating_tab)) for j in range(len(rating_tab[i]))]
    t.sort(key=lambda e : e[1])

    lowest_rated = t[:5]
    highest_rated = t[-5:]
    highest_rated.reverse()

    return number_of_season, season_average, max_episode_number, lowest_rated, highest_rated

def draw(rating_tab, number_of_season, season_average, max_episode_number, lowest_rated, highest_rated, output_path="output"):
    image_size = max(number_of_season * 175 + 250, 50 * max_episode_number + 225, 1000)

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
        if work_snum == prob_season + 1:
            prob_season += 1
            rating_tab.append([])
            name_tab.append([])

        if work_snum != prob_season:
            break

        rating_tab[work_snum - 1].append(work_rating)
        name_tab[work_snum - 1].append(work_title)

    return name_tab, rating_tab
