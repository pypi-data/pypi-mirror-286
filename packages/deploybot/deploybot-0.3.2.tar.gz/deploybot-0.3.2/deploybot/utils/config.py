import configparser
from pathlib import Path

CONFIG_FILE = Path.home() / '.deploybot_config'

def get_config():
    config = configparser.ConfigParser()
    if not CONFIG_FILE.exists():
        config['DEFAULT'] = {'aws_account_id': '', 'environment': '', 'base_path': '', 'branch': '', 'sam_deployment_bucket': '', 'buildkite_org_slug': '', 'buildkite_pipeline_slug': ''}
        with open(str(CONFIG_FILE), 'w') as configfile:
            config.write(configfile)
    else:
        config.read(str(CONFIG_FILE))
    return config

def save_config(aws_account_id, environment, base_path, branch, sam_deployment_bucket, buildkite_org_slug, buildkite_pipeline_slug):
    config = configparser.ConfigParser()
    config['DEFAULT'] = {
        'aws_account_id': aws_account_id,
        'environment': environment,
        'base_path': base_path,
        'branch': branch,
        'sam_deployment_bucket': sam_deployment_bucket,
        'buildkite_org_slug': buildkite_org_slug,
        'buildkite_pipeline_slug': buildkite_pipeline_slug
    }
    with open(str(CONFIG_FILE), 'w') as configfile:
        config.write(configfile)
