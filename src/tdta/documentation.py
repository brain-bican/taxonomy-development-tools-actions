import os
from pathlib import Path

from jinja2 import Template
from urllib.parse import urlparse

from tdta.tdt_export import db_to_cas
from tdta.utils import read_project_config

ANNOTATIONS_TEMPLATE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../resources/annotation_template.md")
TAXONOMY_TEMPLATE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../resources/taxonomy_template.md")


def generate_documentation(sqlite_db: str, output_folder: str, project_config=None):
    """
    Generate markdown documentation for a CAS database.
    Parameters:
        sqlite_db: Path to the CAS database.
        output_folder: Path to the output documentation folder.
        project_config: Project configuration.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    cell_sets_folder = os.path.join(output_folder, "cell_sets")
    if not os.path.exists(cell_sets_folder):
        os.makedirs(cell_sets_folder)

    cas_obj = db_to_cas(sqlite_db)
    cas = cas_obj.to_dict()
    if project_config is None:
        project_config = read_project_config(Path(output_folder).parent.absolute())
    cas = transform_cas(cas, project_config)

    annotation_template = read_jinja_template(ANNOTATIONS_TEMPLATE)
    cell_sets_folder = os.path.join(output_folder, "cell_sets")
    for annotation in cas["annotations"]:
        rendered_file = annotation_template.render(annotation=annotation, metadata=cas)
        annotation_file_name = annotation["cell_set_accession"].replace(":", "_")

        with open(os.path.join(cell_sets_folder,  annotation_file_name + ".md"), "w") as fh:
            fh.write(rendered_file)

    taxonomy_template = read_jinja_template(TAXONOMY_TEMPLATE)
    rendered_file = taxonomy_template.render(cas=cas)
    with open(os.path.join(output_folder, "index.md"), "w") as fh:
        fh.write(rendered_file)


def transform_cas(cas, project_config):
    """
    Adds extra data to cas for visualisation purposes.
    """
    add_purl(cas, project_config)
    add_parents(cas)
    add_weigth(cas)
    transform_annotation_transfer(cas)

    return cas


def transform_annotation_transfer(cas):
    for annotation in cas["annotations"]:
        if "transferred_annotations" in annotation:
            for transferred_annotation in annotation["transferred_annotations"]:
                parsed_url = urlparse(transferred_annotation["source_taxonomy"])
                path_parts = parsed_url.path.split('/')
                taxonomy_id = path_parts[-2]
                purl_base = f"{parsed_url.scheme}://{parsed_url.netloc}/taxonomy/{taxonomy_id}/"
                transferred_annotation["purl_base"] = purl_base


def add_purl(cas, project_config):
    project_id = project_config["id"]
    purl_base = get_project_purl(project_config)
    cas["purl_base"] = purl_base
    if "cellannotation_url" not in cas:
        cas["cellannotation_url"] = f"https://purl.brain-bican.org/taxonomy/{project_id}/{project_id}.json"


def get_project_purl(project_config):
    if "custom_purl" in project_config:
        purl_base = project_config["custom_purl"]
        if not purl_base.endswith("/"):
            purl_base += "/"
    else:
        project_id = project_config["id"]
        purl_base = f"https://purl.brain-bican.org/taxonomy/{project_id}/"
    return purl_base


def add_parents(cas):
    parents = build_hierarchy(cas["annotations"])
    for annotation in cas["annotations"]:
        annotation["parents"] = parents[annotation["cell_set_accession"]]


def add_weigth(cas):
    """
    Add weight to annotations to be used for sorting pages.
    """
    for annotation in cas["annotations"]:
        order = annotation["cell_set_accession"].replace(":", "_").split("_")[-1]
        if order.isdigit():
            annotation["weight"] = int(order)
        else:
            annotation["weight"] = 10 - len(annotation["parents"])


def build_hierarchy(annotations):
    """
    Build a hierarchy of cell sets. Keys of the dicts are cell set accessions, values are lists of parent cell set
    accessions ordered from highest to lowest.
    """
    hierarchy = {}
    annotation_dict = {annotation['cell_set_accession']: annotation for annotation in annotations}

    def get_hierarchy(annotation):
        if 'parent_cell_set_accession' not in annotation:
            return []
        parent_accession = annotation['parent_cell_set_accession']
        parent_annotation = annotation_dict.get(parent_accession)
        if parent_annotation:
            return get_hierarchy(parent_annotation) + [parent_accession]
        return []

    for annotation in annotations:
        cell_set_accession = annotation['cell_set_accession']
        hierarchy[cell_set_accession] = get_hierarchy(annotation)

    return hierarchy


def read_jinja_template(template_path):
    """
    Read Jinja template from file.
    """
    with open(template_path, 'r') as file:
        template = Template(file.read(), trim_blocks=True)
    return template

