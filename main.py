import dessin

def scale_function(x1, x2, y1, y2):
    return lambda x : (y2 - y1) / (x2 - x1) * (x - x2) + y2

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

def draw(rating_tab, number_of_season, season_average, max_episode_number, lowest_rated, highest_rated):
    square_size = max(number_of_season * 175 + 250, 50 * max_episode_number + 225)
    dessin.wn.setup(square_size, square_size)
    dessin.wn.setworldcoordinates(0, square_size, square_size, 0)
    #dessin.ht()

    bg_color_f = scale_function(0, square_size, 250, 100)
    for y in range(square_size):
        dessin.color(f"#DC{hex(int(bg_color_f(y)))[2:]}28")
        dessin.ligne(0, y, square_size, y)
    dessin.color("black")

    dessin.rect_fill(25, 375, number_of_season * 125 - 25, 50, col="white")

    draw_x, draw_y = 25, 0

    max_avg, min_avg = max(season_average), min(season_average)
    height_f = scale_function(min_avg, max_avg, 100, 200)
    color_f = scale_function(min_avg, max_avg, 200, 100)
    for s_avg in season_average:
        graph_height = height_f(s_avg)
        graph_color  = hex(int(color_f(s_avg)))

        dessin.rect_fill(draw_x, 325, 100, graph_height, f"#00{str(graph_color[2:])}00")
        dessin.ecrire(draw_x + 10, 365 - graph_height, s_avg)

        draw_x += 125

    draw_x, draw_y = number_of_season * 125 + 200, 125
    color_f = scale_function(lowest_rated[0][1], highest_rated[0][1], 200, 100)

    dessin.rect_fill(draw_x - 50, 175, 50, 50, "#000000")
    for s_num in range(number_of_season):
        dessin.rect_fill(draw_x, 175, 50, 50,"#000000")
        dessin.ecrire(draw_x + 10, 165, s_num+1, col="white")
        draw_y = 225
        for e_num, e_rating in enumerate(rating_tab[s_num]):
            dessin.rect_fill(number_of_season * 125 + 150, draw_y, 50, 50,"#000000")
            dessin.ecrire(number_of_season * 125 + 152, draw_y - 10, e_num+1, col="white")

            graph_color = hex(int(color_f(e_rating)))
            dessin.rect_fill(draw_x, draw_y, 50, 50, f"#00{str(graph_color[2:])}00")
            dessin.ecrire(draw_x + 12, draw_y - 15, e_rating,font=('Arial', 20, 'bold'))
            draw_y += 50
        draw_x += 50


    dessin.rect_fill(25, 570, number_of_season * 125 - 25, 30, f"#000000")
    dessin.ecrire(27, 567, "Pos", col="white", font=("Arial", 20, "normal"))
    dessin.ecrire(90, 567, "N°S", col="white", font=("Arial", 20, "normal"))
    dessin.ecrire(150, 567, "N°E", col="white", font=("Arial", 20, "normal"))
    dessin.ecrire(210, 567, "/10", col="white", font=("Arial", 20, "normal"))
    dessin.ecrire(280, 567, "Title", col="white", font=("Arial", 20, "normal"))

    draw_y = 600

    for letter, arr in [("H", highest_rated), ("L", lowest_rated)]:
        for index, e in enumerate(arr):
            graph_color = hex(int(color_f(e[1])))
            dessin.rect_fill(25, draw_y, number_of_season * 125 - 25, 30, f"#00{str(graph_color[2:])}00")

            dessin.ecrire(27, draw_y, f"{letter}#{index+1}", font=("Arial", 20, "normal"))
            dessin.ecrire(90, draw_y, str(e[0][0]+1), font=("Arial", 20, "normal"))
            dessin.ecrire(150, draw_y, str(e[0][1]+1), font=("Arial", 20, "normal"))
            dessin.ecrire(210, draw_y, str(e[1]), font=("Arial", 20, "normal"))
            dessin.ecrire(280, draw_y, e[2], font=("Arial", 20, "normal"))

            draw_y += 30

    dessin.save_image()
    print(number_of_season, season_average, max_episode_number, lowest_rated, highest_rated, sep="\n")


t = [[9.1,8.7,8.8,8.3,8.4,9.3,8.9],
    [8.7,9.3,8.4,8.3,8.4,8.9,8.7,9.2,9.2,8.6,8.9,9.3,9.3],
    [8.6,8.7,8.5,8.3,8.7,9.3,9.6,8.8,8.5,7.8,8.5,9.5,9.7],
    [9.2,8.3,8.1,8.7,8.7,8.5,8.9,9.3,8.9,9.6,9.7,9.5,9.9],
    [9.3,8.9,8.9,8.9,9.7,9.1,9.6,9.6,9.5,9.2,9.6,9.2,9.8,10,9.7,9.9]]

d = [["1.1","1.2","1.3","1.4","1.5","1.6","1.7"],
    ["2.1","2.2","2.3","2.4","2.5","2.6","2.7","2.8","2.9","2.10","2.11","2.12","2.13"],
    ["3.1","3.2","3.3","3.4","3.5","3.6","3.7","3.8","3.9","3.10","3.11","3.12","3.13"],
    ["4.1","4.2","4.3","4.4","4.5","4.6","4.7","4.8","4.9","4.10","4.11","4.12","4.13"],
    ["5.1","5.2","5.3","5.4","5.5","5.6","5.7","5.8","5.9","5.10","5.11","5.12","5.13","5.14","5.15","5.16"]]

number_of_season, season_average, max_episode_number, lowest_rated, highest_rated = get_infos(t, d)
draw(t, number_of_season, season_average, max_episode_number, lowest_rated, highest_rated)
