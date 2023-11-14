import unittest
import os
import shutil
from tdta.tdt_export import export_cas_data

TEST_DATA_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "./test_data/")
TEST_OUTPUT = os.path.join(TEST_DATA_FOLDER, "cas_output.json")
TEST_DB = os.path.join(TEST_DATA_FOLDER, "nanobot.db")


class CASExportTests(unittest.TestCase):
    def setUp(self):
        if os.path.exists(TEST_OUTPUT):
            shutil.rmtree(TEST_OUTPUT)

    def test_export(self):
        cas = export_cas_data(TEST_DB, TEST_OUTPUT)
        # self.assertTrue(os.path.isfile(TEST_OUTPUT))

        self.assertTrue(cas)
        result = cas.to_dict()

        # self.assertTrue("author_name" in cas)
        # self.assertEqual("Test User", cas["author_name"])
        #
        # self.assertTrue("labelsets" in cas)
        # self.assertEqual(4, len(cas["labelsets"]))
        # # print(cas["labelsets"])

        self.assertTrue("annotations" in result)
        self.assertEqual(354, len(result["annotations"]))
        print(result["annotations"][:3])

        test_annotation = [x for x in result["annotations"] if x["cell_label"] == "1_MSN"][0]
        self.assertTrue("marker_gene_evidence" in test_annotation)
        self.assertEqual(3, len(test_annotation["marker_gene_evidence"]))
        self.assertTrue("EPYC" in test_annotation["marker_gene_evidence"])
        self.assertTrue("RELN" in test_annotation["marker_gene_evidence"])
        self.assertTrue("GULP1" in test_annotation["marker_gene_evidence"])

        self.assertTrue("user_annotations" in test_annotation)
        print(test_annotation["user_annotations"])
        self.assertEqual(6, len(test_annotation["user_annotations"]))