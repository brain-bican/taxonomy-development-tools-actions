import unittest
import os
import shutil
import json

from tdta.documentation import generate_documentation, build_hierarchy

TEST_DATA_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_data/")
TEST_DB = os.path.join(TEST_DATA_FOLDER, "nanobot_siletti_nn_with_at.db")
TEST_OUTPUT = os.path.join(TEST_DATA_FOLDER, "docs/")


class GenerateDocsTestCase(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_OUTPUT):
            shutil.rmtree(TEST_OUTPUT)

    def test_documentation_generation(self):
        generate_documentation(TEST_DB, TEST_OUTPUT, project_config={"id": "CS202210140"})
        self.assertTrue(os.path.exists(TEST_OUTPUT))

        self.assertEqual(True, False)  # add assertion here

    def test_hierarchy_breadcrumb(self):
        with open("./test_data/CS202210140.json") as f:
            siletti = json.load(f)

        hierarchy = build_hierarchy(siletti["annotations"])
        self.assertEqual(386, len(list(hierarchy.keys())))

        subcluster_parents = hierarchy["CS202210140_3490"]
        self.assertEqual(2, len(subcluster_parents))
        self.assertEqual("CS202210140_469", subcluster_parents[0])
        self.assertEqual("CS202210140_51", subcluster_parents[1])

        cluster_parents = hierarchy["CS202210140_6"]
        self.assertEqual(1, len(cluster_parents))
        self.assertEqual("CS202210140_464", cluster_parents[0])

        supercluster_parents = hierarchy["CS202210140_465"]
        self.assertEqual(0, len(supercluster_parents))


if __name__ == '__main__':
    unittest.main()
