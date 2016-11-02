
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
import os
import glob


def GetTestImage(imagefile, mode='simple'):
    """ Prepear image file for tests """

    IMG_ROOT = os.path.join(settings.BASE_DIR, 'apps/hello/static/img/')

    if (mode == 'simple'):
        photo = open(IMG_ROOT + imagefile, 'rb')
        return SimpleUploadedFile(photo.name, photo.read())

    elif (mode == 'PIL'):
        if isinstance(imagefile, basestring):
            return Image.open(IMG_ROOT + imagefile)
        else:
            return Image.open(imagefile)


def RemoveTestImages():
    path = os.path.join(os.path.dirname(settings.BASE_DIR),
                        'uploads', 'photo', '*.png')

    for f in glob.glob(path):
        filename = os.path.basename(f)
        if filename.startswith("test"):
            os.remove(f)
