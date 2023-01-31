# TF for image classification model

import tensorflow
import numpy
from PIL import Image

model = tensorflow.saved_model.load('./')
classes = ["gauzy", "meshed", "cracked", "stratified", "scaly", "swirly", "perforated", "pleated", "flecked", "fibrous",
           "polka-dotted", "chequered", "blotchy", "stained", "crystalline", "porous", "banded", "lacelike",
           "sprinkled", "bubbly", "lined", "veined", "bumpy", "paisley", "potholed", "waffled", "pitted", "frilly",
           "spiralled", "knitted", "grooved", "dotted", "interlaced", "crosshatched", "wrinkled", "smeared", "striped",
           "braided", "freckled", "cobwebbed", "honeycombed", "woven", "matted", "zigzagged", "marbled", "studded",
           "grid", ]

img = Image.open("image.jpg").convert('RGB')
img = img.resize((300, 300 * img.size[1] // img.size[0]), Image.ANTIALIAS)
inp_numpy = numpy.array(img)[None]

inp = tensorflow.constant(inp_numpy, dtype='float32')

class_scores = model(inp)[0].numpy()

print("")
print("class_scores", class_scores)
print("Class : ", classes[class_scores.argmax()])
