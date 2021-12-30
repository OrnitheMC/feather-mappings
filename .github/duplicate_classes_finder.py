from os import listdir, path
from os.path import isfile, join
from collections import defaultdict
from typing import List

"""---- Config ----"""
mappings_folder = path.join("..", "mappings")  # the path to the mappings folder
mappings = defaultdict(list)  # the dictionary to put the mappings in


def main():
    """
    Main function checking for duplicates inside the mappings folder. If duplicates
    are found an error is raised and the duplicates are printed.
    """
    dirs = unpack_directory(path)
    travel_directory(dirs)
    duplicates = dict(filter(lambda elem: len(elem[1]) > 1, mappings.items()))
    if duplicates:
        raise DuplicateMappings(len(duplicates), duplicates)


def travel_directory(dirs: list):
    """
    This function travels through a directory. If the entry is a file it will add it to the
    dictionary containing the mappings. If the entry is a dictionary it will again call
    this method on that dictionary.
    :param dirs: a list of folders and files that are in the directory
    """
    for f in dirs:
        if isfile(f):
            add_to_dict(f)
        else:
            travel_directory(unpack_directory(f))


def unpack_directory(dir_path: str) -> List[str]:
    """
    This function unpacks a directory into it's components (files and subdirectories)
    :param dir_path: a path to a directory
    :return: a list of paths to the files and directories inside the directory
    """
    return [join(dir_path, f) for f in listdir(dir_path)]


def add_to_dict(file: str):
    """
    This method reads a file and checks the mapped class. It will add the file to the
    directory containing all of the mappings. The key is the class name in the intermediaries.
    The value is a list of all the different names this class is mapped under. Each element
    in this list is a list it self containing the mapped name of the entry and the file path.
    :param file: the file to be analyzed
    """
    with open(file) as f:
        class_mapping = f.readline().split(' ')[1:]

    class_ = class_mapping[0].strip('\n')
    mapping = class_mapping[1].strip('\n') if len(class_mapping) == 2 else class_
    mappings[class_].append([mapping, file])


class DuplicateMappings(Exception):
    """
    Exception raised when duplicate mappings are found.

    Attributes:
        the amount of classes that have duplicates
        the dictionary containing the duplicates
        the Exception message (set by default but is able to be overridden)
    """

    def __init__(self, n, duplicates, message="Duplicate mappings found for {} classes"):
        self.n = n
        self.duplicates = duplicates
        self.message = message.format(self.n)
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}\n\n{self.get_formatted_duplicates()}'

    def get_formatted_duplicates(self):
        """
        A function that formats the duplicates that have been found in a nice human readable output.
        :return: a string containing the duplicates to output as a message
        """
        duplicates_string = ''
        for key in self.duplicates:
            duplicates_string += f'Duplicates ({len(self.duplicates[key])}) found of {key} mapped as:\n'
            for mapping in self.duplicates[key]:
                duplicates_string += f'\t{mapping[0]} in file {mapping[1]}\n'
        return duplicates_string


if __name__ == '__main__':
    main()
