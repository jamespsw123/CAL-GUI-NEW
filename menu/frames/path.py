# path test

import os
imagesPath = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
print imagesPath
photo = os.path.join(imagesPath, 'impages/add.png')
print photo


