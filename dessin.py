from turtle import *
from os import remove

wn = Screen()
wn.tracer(0)

def bouge(x, y):
    """
        Permet de déplacer la tortue à un point donné
    """
    up()
    goto(x,y)
    down()

def offset(xoff, yoff):
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

def ecrire(x, y, texte, align='left', font=('Arial', 32, 'normal')):
    """
        Écrit les texte aux coordonnées x et y.
        (x,y) devra être le point en bas à gauche du texte.
    """
    bouge(x, y)
    write(texte, align=align, font=font)

def save_image(output="output.png"):
    from PIL import Image

    wn.update()
    getscreen().getcanvas().postscript(file='funaaimelesfraises.ps')
    image = Image.open("funaaimelesfraises.ps")
    image.convert("RGB").save("output.jpg", "JPEG")
    image.save("output.png", "PNG")
    remove("funaaimelesfraises.ps")
