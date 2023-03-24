import yaml
from src.generic import deepAttrDict


def yaml_parser(filename):
    with open(f"{filename}.yml", "r") as yml_file:
        parsed_yml_file = yaml.safe_load(yml_file)
    return deepAttrDict(parsed_yml_file)


yaml_filename = "/home/sohinim/github/clariah/pure3d/pilots/test-pure3d/src/workflow/init"
users_list = yaml_parser(yaml_filename)
print(users_list.userRole.site)
