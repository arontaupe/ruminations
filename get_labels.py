# using OS
import os
# using pathlib
import pathlib
from glob import glob
labels = []
names = glob("datasets/dtd/images/*/", recursive = True)

for name in names:
    path = pathlib.PurePath(name)
    labels.append(path.name)
    #print(path.name)

print(labels)
