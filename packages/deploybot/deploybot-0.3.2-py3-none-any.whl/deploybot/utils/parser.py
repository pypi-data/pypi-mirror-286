import yaml
import os

def yaml_constructor(loader, node):
    """Return the node's value as is, handling scalars, sequences, and mappings."""
    if isinstance(node, yaml.ScalarNode):
        return loader.construct_scalar(node)
    elif isinstance(node, yaml.SequenceNode):
        return loader.construct_sequence(node)
    elif isinstance(node, yaml.MappingNode):
        return loader.construct_mapping(node)
    else:
        return loader.construct_object(node)

# Custom loader to handle CloudFormation intrinsic functions
class CustomYamlLoader(yaml.SafeLoader):
    pass

# Register all the CloudFormation intrinsic functions
def register_yaml_constructors(loader):
    tags = [
        '!Ref', '!GetAtt', '!Sub', '!Join', '!Equals', '!If', 
        '!And', '!Or', '!FindInMap', '!Select', '!ImportValue', 
        '!Condition', '!Not'
    ]
    for tag in tags:
        loader.add_constructor(tag, yaml_constructor)

register_yaml_constructors(CustomYamlLoader)

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
            template = yaml.load(file, Loader=CustomYamlLoader)
            if environment == 'staging':
                stack_name = template.get('Metadata', {}).get('StagingStackName')
            elif environment == 'production':
                stack_name = template.get('Metadata', {}).get('ProductionStackName')
            else:
                print("Invalid environment specified.")
                return None
            return stack_name
        except yaml.YAMLError as exc:
            print("Error reading YAML file: {}".format(exc))
            return None
