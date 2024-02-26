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
            os.remove(TEST_OUTPUT)

    def test_export(self):
        cas = export_cas_data(TEST_DB, TEST_OUTPUT, TEST_DATA_FOLDER)
        self.assertTrue(os.path.exists(TEST_OUTPUT))

        self.assertTrue(cas)
        result = cas.to_dict()

        self.assertTrue("author_name" in result)
        self.assertEqual("Nelson Johansen", result["author_name"])
        self.assertFalse("orcid" in result)
        self.assertFalse("cellannotation_schema_version" in result)

        self.assertTrue("labelsets" in result)
        self.assertEqual(4, len(result["labelsets"]))
        test_labelset = [x for x in result["labelsets"] if x["name"] == "Cluster"][0]
        self.assertEqual("0", test_labelset["rank"])
        self.assertEqual(1, len([x for x in result["labelsets"] if x["name"] == "Subclass"]))
        test_labelset = [x for x in result["labelsets"] if x["name"] == "Subclass"][0]
        self.assertEqual("1", test_labelset["rank"])

        self.assertTrue("annotations" in result)
        self.assertEqual(355, len(result["annotations"]))
        # print(result["annotations"][:3])
        test_annotation = [x for x in result["annotations"] if x["cell_label"] == "1_MSN"][0]
        self.assertEqual("D1-Matrix", test_annotation["parent_cell_set_name"])
        self.assertEqual("AIT115_300", test_annotation["parent_cell_set_accession"])
        self.assertFalse("marker_gene_evidence" in test_annotation)
        # self.assertEqual(3, len(test_annotation["marker_gene_evidence"]))
        # self.assertTrue("EPYC" in test_annotation["marker_gene_evidence"])
        # self.assertTrue("RELN" in test_annotation["marker_gene_evidence"])
        # self.assertTrue("GULP1" in test_annotation["marker_gene_evidence"])
        self.assertFalse("transferred_annotations" in test_annotation)
        self.assertFalse("rationale_dois" in test_annotation)

        self.assertTrue("user_annotations" in test_annotation)
        self.assertEqual(12, len(test_annotation["user_annotations"]))
        self.assertTrue({'labelset': 'Cluster size', 'cell_label': '16393'} in test_annotation["user_annotations"])
        self.assertTrue({'labelset': 'region.info _Frequency_', 'cell_label': 'PuR(0.52) | CaH(0.39)'} in test_annotation["user_annotations"])
