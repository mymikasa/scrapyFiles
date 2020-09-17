# -*- coding: utf-8 -*-

import os
from os import path
import random
import pkg_resources

os.environ['PYTHON_EGG_CACHE'] = '/tmp'

# See https://github.com/N0taN3rd/userAgentLists
# You can use exist csv file from upon project or re-generate csv file
# which you wanted, then move then into `csv_dir`.
csv_dir = 'csv/chrome.csv'
user_agent_list = list()


def extract_one_line(line):
    for i in range(2):
        index = line.rfind(',')
        if index == -1:
            return None
        line = line[:index]

    return None if 'Windows' in line else line.replace('"', '')


def read_one_csv_file(filepath):
    with open(filepath, 'r', encoding="utf-8") as f:
        next(f)  # skip first line

        lines = f.readlines()
        for line in lines:
            user_agent = extract_one_line(line)
            if user_agent is not None:
                user_agent_list.append(user_agent)

    f.close()


try:
    # for file in pkg_resources.resource_listdir('crawler', csv_dir):
    #     read_one_csv_file(pkg_resources.resource_filename(
    #         'crawler', path.join(csv_dir, file)))
    d = path.dirname(__file__)
    file_path = path.join(d, csv_dir)
    read_one_csv_file(file_path)
    user_agent_list = list(set(user_agent_list))
except Exception as e:
    raise e


def get_user_agent():
    return random.choice(user_agent_list)


if __name__ == '__main__':
    print(get_user_agent())
