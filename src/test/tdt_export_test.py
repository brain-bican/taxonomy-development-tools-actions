import unittest
import os
from typing import List, Optional
from tdta.tdt_export import export_cas_data, is_list

TEST_DATA_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "./test_data/")
TEST_OUTPUT = os.path.join(TEST_DATA_FOLDER, "cas_output.json")
TEST_DB = os.path.join(TEST_DATA_FOLDER, "nanobot.db")
TEST_DB_SILETTI = os.path.join(TEST_DATA_FOLDER, "nanobot_siletti_nn.db")
TEST_WMB_FOLDER = os.path.join(TEST_DATA_FOLDER, "wmb_curation_tables")


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
        self.assertTrue("orcid" in result)
        self.assertEqual("https://orcid.org/0000-0002-4436-969X", result["orcid"])
        self.assertTrue("cellannotation_schema_version" in result)
        self.assertEqual("0.2b0", result["cellannotation_schema_version"])

        self.assertTrue("labelsets" in result)
        self.assertEqual(4, len(result["labelsets"]))
        test_labelset = [x for x in result["labelsets"] if x["name"] == "Cluster"][0]
        self.assertEqual(0, test_labelset["rank"])
        self.assertEqual(1, len([x for x in result["labelsets"] if x["name"] == "Subclass"]))
        test_labelset = [x for x in result["labelsets"] if x["name"] == "Subclass"][0]
        self.assertEqual(1, test_labelset["rank"])

        self.assertTrue("annotations" in result)
        self.assertEqual(355, len(result["annotations"]))
        # print(result["annotations"][:3])
        test_annotation = [x for x in result["annotations"] if x["cell_label"] == "1_MSN"][0]
        self.assertEqual("AIT115_300", test_annotation["parent_cell_set_accession"])
        self.assertFalse("parent_cell_set_name" in test_annotation)
        self.assertFalse("marker_gene_evidence" in test_annotation)
        # self.assertEqual(3, len(test_annotation["marker_gene_evidence"]))
        # self.assertTrue("EPYC" in test_annotation["marker_gene_evidence"])
        # self.assertTrue("RELN" in test_annotation["marker_gene_evidence"])
        # self.assertTrue("GULP1" in test_annotation["marker_gene_evidence"])
        self.assertFalse("transferred_annotations" in test_annotation)
        self.assertFalse("rationale_dois" in test_annotation)

        self.assertTrue("author_annotation_fields" in test_annotation)
        print(test_annotation["author_annotation_fields"])
        self.assertEqual(11, len(test_annotation["author_annotation_fields"]))
        self.assertEqual('16393', test_annotation["author_annotation_fields"]['Cluster size'])
        self.assertEqual('PuR(0.52) | CaH(0.39)', test_annotation["author_annotation_fields"]['region.info _Frequency_'])

        self.assertFalse("reviews" in test_annotation)
        # self.assertTrue("reviews" in test_annotation)
        # self.assertEqual(1, len(test_annotation["reviews"]))
        # self.assertEqual('hkir-dev', test_annotation["reviews"][0]['reviewer'])
        # self.assertEqual('Disagree', test_annotation["reviews"][0]['review'])
        # self.assertEqual('incorrect', test_annotation["reviews"][0]['explanation'])
        # print(test_annotation["reviews"][0]['datestamp'])
        # self.assertEqual('2024-05-29T08:10:11.126Z', test_annotation["reviews"][0]['datestamp'])

    def test_export_siletti_nn(self):
        cas = export_cas_data(TEST_DB_SILETTI, TEST_OUTPUT, TEST_DATA_FOLDER)
        self.assertTrue(os.path.exists(TEST_OUTPUT))

        self.assertTrue(cas)
        result = cas.to_dict()

        self.assertTrue("annotations" in result)
        test_annotation = [x for x in result["annotations"] if x["cell_label"] == "VendC_15"][0]
        self.assertEqual("CS202210140_16", test_annotation["cell_set_accession"])
        self.assertTrue("marker_gene_evidence" in test_annotation)
        print(test_annotation["marker_gene_evidence"])
        self.assertEqual(4, len(test_annotation["marker_gene_evidence"]))
        self.assertTrue("FLT1" in test_annotation["marker_gene_evidence"])
        self.assertTrue("CLDN5" in test_annotation["marker_gene_evidence"])
        self.assertTrue("PECAM1" in test_annotation["marker_gene_evidence"])
        self.assertTrue("MFSD2A" in test_annotation["marker_gene_evidence"])

    def test_list_instance(self):
        samples = AttributeSamples()

        import inspect
        members = inspect.getmembers(samples)

        for name, value in members:
            if not name.startswith('__'):  # Skip built-in attributes
                print(name, value, type(value))

        self.assertTrue(is_list(samples, "field1"))
        self.assertTrue(is_list(samples, "field2"))
        self.assertTrue(is_list(samples, "field3"))
        self.assertTrue(is_list(samples, "field4"))
        self.assertTrue(is_list(samples, "field5"))
        self.assertTrue(is_list(samples, "field6"))
        self.assertTrue(is_list(samples, "field7"))

        self.assertFalse(is_list(samples, "field8"))
        self.assertFalse(is_list(samples, "field9"))
        self.assertFalse(is_list(samples, "field10"))

    def test_save_from_folder(self):
        cas = export_cas_data(TEST_WMB_FOLDER, TEST_OUTPUT, TEST_DATA_FOLDER)
        self.assertTrue(os.path.exists(TEST_OUTPUT))

        self.assertTrue(cas)
        result = cas.to_dict()

        self.assertEqual("Hongkui Zeng", result.get("author_name"))
        self.assertEqual("https://orcid.org/0000-0002-9361-5607", result.get("orcid"))
        self.assertEqual("1.0.0", result.get("cellannotation_schema_version"))

        self.assertEqual(5, len(result.get("labelsets")))
        test_labelset = [x for x in result["labelsets"] if x["name"] == "cluster"][0]
        self.assertEqual(0, test_labelset["rank"])
        self.assertEqual(1, len([x for x in result["labelsets"] if x["name"] == "subclass"]))
        test_labelset = [x for x in result["labelsets"] if x["name"] == "subclass"][0]
        self.assertEqual(2, test_labelset["rank"])
        self.assertEqual(1, len([x for x in result["labelsets"] if x["name"] == "neurotransmitter"]))
        test_labelset = [x for x in result["labelsets"] if x["name"] == "neurotransmitter"][0]
        self.assertTrue("rank" not in test_labelset)

        self.assertEqual(6905, len(result.get("annotations")))
        # print(result["annotations"][:3])
        test_annotation = [x for x in result["annotations"] if x["cell_label"] == "001 CLA-EPd-CTX Car3 Glut"][0]
        self.assertEqual("CS20230722_CLAS_01", test_annotation["parent_cell_set_accession"])
        self.assertFalse("parent_cell_set_name" in test_annotation)
        self.assertFalse("marker_gene_evidence" in test_annotation)
        # self.assertEqual(3, len(test_annotation["marker_gene_evidence"]))
        # self.assertTrue("EPYC" in test_annotation["marker_gene_evidence"])
        # self.assertTrue("RELN" in test_annotation["marker_gene_evidence"])
        # self.assertTrue("GULP1" in test_annotation["marker_gene_evidence"])
        self.assertFalse("transferred_annotations" in test_annotation)
        self.assertFalse("rationale_dois" in test_annotation)

        self.assertTrue("author_annotation_fields" in test_annotation)
        self.assertEqual(35, len(test_annotation["author_annotation_fields"]))
        self.assertEqual('Pallium-Glut', test_annotation["author_annotation_fields"]['neighborhood'])
        self.assertEqual('Cux2,Satb2,Nr4a2,Zfhx4,Pou6f2', test_annotation["author_annotation_fields"]['subclass.tf.markers.combo'])

        self.assertFalse("reviews" in test_annotation)


class AttributeSamples:

    field1 = list()
    field2: Optional[List[str]] = None
    field3: List[str] = []
    field4: List[str] = ["a", "b", "c"]
    field5: Optional[List[str]] = ["a", "b", "c"]
    field6: Optional[List[int]] = None
    field7: List = None

    field8: str = None
    field9: Optional[str] = None
    field10 = None


