import unittest
from id_extractor import scan_id
import os

pictures = os.listdir(r"C:\Users\u9162190\Desktop\MODULES\some_ids")


class test_id_extractor(unittest.TestCase):
    def test_get_10_ids(self):
        length = 100
        ids = []
        for x in range(length):
            ids.append(scan_id(f"some_ids/{pictures[x]}"))

        captureErrors = 0
        for id in ids:
            for prop in id.values():
                if prop == "captureError":
                    captureErrors += 1
        
        print(f"TEST STATUS: captured {len(ids) * 4} with {captureErrors} captureErrors")
        self.assertEqual(len(ids), length)


unittest.main()
