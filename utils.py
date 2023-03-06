import os
import torch.nn as nn
import pickle
import torch


def ensure_dir_exist(directory):
    """This function ensure the given directory is exist.

    Args:
        directory (str): The directory that needs to be ensure.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def pad_sentence(array, max_len):
    tensor = torch.tensor(array)
    """Padding array to desired length.

    Args:
        array (list): The array needs to be padded.
        max_len (int): The desired length.

    Returns:
        torch.tensor: The tensor with desired length.
    """
    return nn.ConstantPad1d((0, max_len - tensor.shape[0]), 0)(tensor).tolist()


def save_object(obj, directory, name):
    """Save Object using pickle

    Args:
        object (object): The object to be saved.
        directory (str): The saved directory.
        name (str): File name.
    """
    if not directory.endswith('/'):
        directory = directory + '/'

    file = open(directory + name, 'wb')
    pickle.dump(obj, file)


def load_object(path):
    """Load pickle object .

    Args:
        path (str): Saved file path.

    Returns:
        object: Object loaded from pickle file.
    """
    file = open(path, 'rb')
    return pickle.load(file)


def vector_to_dict(vector):
    features = list(range(len(vector)))
    return dict(zip(features, vector))


if __name__ == "__main__":
    a = list(range(20))
    print(vector_to_dict(a))
