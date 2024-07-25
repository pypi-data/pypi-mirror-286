from ruamel.yaml import YAML
import os

yaml = YAML()

def extract_stack_name(file_path, environment):
    """
    Extracts the stack name from a given template.yml file based on the environment.

    :param file_path: Path to the template.yml file.
    :param environment: Environment to get the stack name for ('staging' or 'production').
    :return: Stack name if found, else None.
    """
    if not os.path.exists(file_path):
        print("File not found: {}".format(file_path))
        return None

    with open(file_path, 'r') as file:
        try:
            template = yaml.load(file)
            if environment == 'staging':
                stack_name = template.get('Metadata', {}).get('StagingStackName')
            elif environment == 'production':
                stack_name = template.get('Metadata', {}).get('ProductionStackName')
            else:
                print("Invalid environment specified.")
                return None
            return stack_name
        except Exception as exc:
            print("Error reading YAML file: {}".format(exc))
            return None
