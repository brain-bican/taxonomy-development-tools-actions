import unittest
import os
import shutil
from tdta.purl_publish import publish_to_purl

TEST_DATA_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "./test_data/")


class PurlPublishingTests(unittest.TestCase):
    def setUp(self):
        os.environ["GH_TOKEN"] = ""

        purl_folder = os.path.join(TEST_DATA_FOLDER, "purl")
        for item in os.listdir(purl_folder):
            if not os.path.isfile(os.path.join(purl_folder, item)):
                shutil.rmtree(os.path.join(purl_folder, item))

    # def test_purl_publish(self):
    #     publish_to_purl(TEST_DATA_FOLDER, "CCN20230001", "hkir-dev")
