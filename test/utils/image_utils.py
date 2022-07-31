import io

from PIL import Image
import imagehash


def compare_images(standard, current):
    standard_hash = imagehash.average_hash(Image.open(io.BytesIO(standard)))
    current_hash = imagehash.average_hash(Image.open(io.BytesIO(current)))
    cutoff = 5
    if standard_hash - current_hash < cutoff:
        return True
    else:
        return False
