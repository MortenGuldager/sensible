#!/usr/bin/python3
import os
import yaml
#from yaml.loader import SafeLoader
from pprint import pprint

def load_yaml_file(yaml_file):
    with open(yaml_file) as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
    return data

def load_all_yaml_files(yaml_dir):
    data = {}
    for yaml_name in os.listdir(yaml_dir):
        (name, ext) = os.path.splitext(yaml_name)
        yaml_file = os.path.join(yaml_dir, yaml_name)
        if ext.lower() in (".yml", ".yaml"):
            data[name] = load_yaml_file(yaml_file)
        else:
            print("non-yaml file not expected here", yaml_file)
    return data

def load_role(role_dir):
    data = {}
    for role_section in os.listdir(role_dir):
        role_section_dir = os.path.join(role_dir, role_section)
        if os.path.isdir(role_section_dir):
            if role_section in ("tasks", "handlers"):
                data[role_section] = load_all_yaml_files(role_section_dir)
                continue
        print("unexpected role_section found", role_section)
    return data          
    

def traverse_roles_dir(roles_dir, sensible_dir):

    for role_name in os.listdir(roles_dir):
        if role_name[0] == '.':
            continue
        
        role_dir = os.path.join(roles_dir, role_name)
        if not os.path.isdir(role_dir):
            continue
        
        sensible_file = os.path.join(sensible_dir,role_name) + '.yml'
        data = load_role(role_dir)
        with open(sensible_file, "w") as f:
            yaml.dump(data, f, indent=4, default_flow_style=False)
        

        
def main():
    try:
        os.mkdir("sensible")
    except FileExistsError:
        print("Refuses to overwrite sensible directory, if you really mean it, remove it manually")
        exit()
    traverse_roles_dir("roles-orig", "sensible")

if __name__ == "__main__":
    main()