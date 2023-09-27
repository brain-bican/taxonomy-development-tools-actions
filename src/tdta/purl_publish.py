import os


def publish_to_purl(file_path: str) -> str:
    """
    Publishes the given taxonomy to the purl system. First checks if PURL system already has a config for the given
    taxonomy. If not, makes a pull request to create a config.
    :param file_path: path to the project root folder
    :return: url of the created pull request or the url of the existing PURL configuration.
    """
    print("In PURL action.")
    current_dir = os.path.dirname(os.path.realpath(__file__))
    print(os.path.abspath(current_dir))
    print(os.path.abspath(file_path))

    files = [f for f in os.listdir(os.path.abspath(file_path)) if os.path.isfile(f)]
    for file in files:
        print(file)

    return "DONE"
