from pygame_functions import *
screenSize(1000,500)
setBackgroundImage("kitchen_background.jpg")

snail = makeSprite("snail.gif")
showSprite(snail)
transformSprite(snail,0,0.15)

endWait()