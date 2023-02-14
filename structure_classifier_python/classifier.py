# TF for image classification model
import tensorflow
import numpy
from PIL import Image

def classify():
    model = tensorflow.saved_model.load('structure_classifier_python/.')
    classes = ["gauzy", "meshed", "cracked", "stratified", "scaly", "swirly", "perforated", "pleated", "flecked", "fibrous",
               "polka-dotted", "chequered", "blotchy", "stained", "crystalline", "porous", "banded", "lacelike",
               "sprinkled", "bubbly", "lined", "veined", "bumpy", "paisley", "potholed", "waffled", "pitted", "frilly",
               "spiralled", "knitted", "grooved", "dotted", "interlaced", "crosshatched", "wrinkled", "smeared", "striped",
               "braided", "freckled", "cobwebbed", "honeycombed", "woven", "matted", "zigzagged", "marbled", "studded",
               "grid", ]

    img = Image.open("structure_classifier_python/image.png").convert('RGB')
    img = img.resize((300, 300 * img.size[1] // img.size[0]), Image.ANTIALIAS)
    inp_numpy = numpy.array(img)[None]

    inp = tensorflow.constant(inp_numpy, dtype='float32')

    class_scores = model(inp)[0].numpy()
    img.show()
    print("")
    print("class_scores", class_scores)
    result = classes[class_scores.argmax()]
    print("Class : ", result)
    return result
