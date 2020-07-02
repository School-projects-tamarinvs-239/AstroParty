from math import sqrt
def open_file (self, name = 'map1.txt'):
    f = open (name, 'r')
    textmap = f.read()
    f.close()
    l = len (textmap)

    return textmap, l

