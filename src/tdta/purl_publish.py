import os


def publish_to_purl() -> str:
    """
    Publishes the given taxonomy to the purl system. First checks if PURL system already has a config for the given
    taxonomy. If not, makes a pull request to create a config.
    :return: url of the created pull request or the url of the existing PURL configuration.
    """
    print("In PURL action.")
    current_dir = os.path.dirname(os.path.realpath(__file__))
    print(os.path.abspath(current_dir))

    return "DONE"
