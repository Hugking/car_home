import fontforge

F = fontforge.open("autohome.ttf")
for name in F:
    filename = "img/" + name + ".png"
    F[name].export(filename)
