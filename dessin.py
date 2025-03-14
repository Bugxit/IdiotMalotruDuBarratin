from turtle import *
from os import remove

wn = Screen()
wn.tracer(0)
wn.cv._rootwindow.withdraw()

def bouge(x, y):
    """
        Permet de déplacer la tortue à un point donné
    """
    up()
    goto(x,y)
    down()

def offset(xoff, yoff):
    """
        Déplace la tortue de xoff et yoff à partir de la position actuelle
    """
    cur_x, cur_y = pos()
    bouge(cur_x + xoff, cur_y + yoff)

def ligne(x1, y1, x2, y2):
    """
        Trace une ligne entre les deux points (x1, y1) et (x2, y2)
    """
    bouge(x1, y1)
    goto(x2, y2)

def rect(x, y, width, height):
    """
        Trace un rectangle de coin bas gauche (x, y),
        de largeur width et de hauteur height.
    """
    bouge(x, y)
    goto(x + width, y)
    goto(x + width, y - height)
    goto(x, y - height)
    goto(x, y)

def rect_fill(x, y, width, height, col):
    bouge(x, y)
    fillcolor(col)
    begin_fill()
    rect(x, y, width, height)
    end_fill()

def cercle(x, y, r):
    """
        Trace un cercle de centre (x, y) et de rayon r
    """

    bouge(x, y-r)
    circle(r)

def ecrire(x, y, texte, col="black", align='left', font='Arial', font_size=32, font_type="normal"):
    """
        Écrit les texte aux coordonnées x et y.
        (x,y) devra être le point en bas à gauche du texte.
    """
    bouge(x, y)
    color(col)
    write(texte, align=align, font=(font, font_size, font_type))
    color("black")

def save_image(output="output"):
    # Imported here because ratio (to prove we did not cheat)
    from PIL import Image

    # Update the screen
    wn.update()
    # Get EPS file
    getscreen().getcanvas().postscript(file='funaaimelesfraises.ps')
    image = Image.open("funaaimelesfraises.ps")
    # Convert & save it to JPG and PNG
    image.convert("RGB").save(output + ".jpg", "JPEG")
    image.save(output + ".png", "PNG")
    # Clear the useless EPS file
    remove("funaaimelesfraises.ps")
