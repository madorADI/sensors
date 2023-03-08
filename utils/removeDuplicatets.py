import os
import photohash
from PIL import Image

hashes = set()

def removeDuplicates(dir):
    for img in os.listdir(dir):
        path = os.path.join(dir, img)
        currHash = photohash.average_hash(path)

        for hash in hashes:
            if img in os.listdir(dir):
                if photohash.hashes_are_similar(hash , currHash):
                    os.remove(path)

        if currHash not in hashes:
            hashes.add(currHash)

# removeDuplicates("C:/Users/u9092788/Downloads/smaller_photos/new_photos")