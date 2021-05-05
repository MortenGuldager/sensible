#!/usr/bin/python3
import os
import yaml
from pprint import pprint
import shutil

stats={
    "sensible": 0,
    "roles" : 0,
    "files" : 0
}

def load_yaml_file(yaml_file):
    with open(yaml_file) as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
    return data

def write_role_files(roles_dir, role_name, role_data):
    stats["roles"] += 1
    role_dir = os.path.join(roles_dir, role_name)
    os.mkdir(role_dir)
    for (section_name, section_data) in role_data.items():
        section_dir = os.path.join(role_dir, section_name)
        os.mkdir(section_dir)
        for (file, file_data) in section_data.items():
            stats["files"] += 1
            ff = os.path.join(section_dir, file) + ".yml"
            with open(ff, "w") as f:
                yaml.dump(file_data, f, indent=4, default_flow_style=False)

def expand_sensible(sensible_dir, roles_dir):
    for sensible_file in os.listdir(sensible_dir):
        ff = os.path.join(sensible_dir, sensible_file)
        data = load_yaml_file(ff)    
        (role_name, ext) = os.path.splitext(sensible_file)
        write_role_files(roles_dir, role_name, data)


def main():
    src="sensible"
    dst="roles-unsensible"
    try:
        shutil.rmtree(dst)
    except FileNotFoundError:
        pass
    os.mkdir(dst)
    expand_sensible(src,dst)
    print("transformed sensible into", stats)

    try:
        sl = os.readlink("roles")
    except FileNotFoundError:
        print("Please create a symlink from roles to", dst)
        print("ln -s %s roles" % dst)
        exit(1)

if __name__ == "__main__":
    main()
