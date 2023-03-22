import yaml


def yaml_parser(filename):
    with open(f"{filename}.yml", "r") as yml_file:
        parsed_yml_file = yaml.safe_load(yml_file)
    return parsed_yml_file


yaml_filename = "/home/sohinim/github/clariah/pure3d/pilots/test-pure3d/src/workflow/init"
users_list = dict(yaml_parser(yaml_filename)["userRole"]["site"])

for key, value in users_list.items():
    print(key, value)

#print(key)
#print(value)
    #with open(yaml_filename, "r") as yml_file:
    #parsed_yml_file = yaml.safe_load(yml_file)
#print(parsed_yml_file["userRole"]["site"])