from PIL import Image

img = Image.open("task.png")
pix = img.load()
d={'+':(0,255,0),'[':(255,255,0),']':(128,128,0),'-':(0,128,0),'>':(255,0,0),'<':(128,0,0),'.':(0,0,255)}
code = ""
for i in range(359):
    for j in d:
        if d[j] == pix[i, 0]:
            code += j

print(code)