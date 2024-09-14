import random
import json
import base64
import re
from os import path, environ

import requests


def generate_random_name_username(salt=''):
    """
    Generates a random (ajdective + noun) expression
    used for name and username.
    It also generates a suffix with the given salt.
    Returns a tuple: name, username.
    """
    adjectives_path = path.join(
        path.dirname(__file__), 'word_salad', 'adjectives.txt'
    )
    nouns_path = path.join(
        path.dirname(__file__), 'word_salad', 'nouns.txt'
    )
    adjectives, nouns = [], []

    with open(adjectives_path, 'r') as adjectives_file:
        adjectives = adjectives_file.read().split('\n')
    with open(nouns_path, 'r') as nouns_file:
        nouns = nouns_file.read().split('\n')

    suffix = salt[random.randint(0, len(salt)-1)::-2].lower()
    generated = [
        random.choice(adjectives).capitalize(),
        random.choice(nouns).capitalize()
    ]

    username = ''.join(generated) + '_' + suffix
    name = ' '.join(generated)

    return name, username


def handled_request(method: str, url, **kwargs):
    """
    Making requests safely.
    """
    try:
        res = requests.request(method, url, **kwargs)
        if res.status_code == 200:
            return res.json(), 200
        else:
            return res.text, res.status_code
    except Exception as e:
        return e.__class__.__name__, 400


def download_file(url):
    """
    Downloads a file from a url and saves it to a file.
    """
    local_filename = url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                f.write(chunk)
    return local_filename


def parse_str_to_list_or_nothing(thestring):
    """
    Parses a list like string to a list or return it as it was before.
    """
    if isinstance(thestring, str):
        converted_string = eval(thestring)
        if isinstance(converted_string, list):
            return converted_string

    return thestring


def manipulate_class_variables(klass, changing_vars=dict()):
    """
    A decorator for assigning some variables to a class.
    `changing_vars` is a dictionary consisting name, values
    of each variable.
    """
    class manipulated_klass(klass):
        pass

    for name, value in changing_vars.items():
        setattr(manipulated_klass, name, value)

    return manipulated_klass


def getattr_getattr_getattr_(obj, attr: str, sep='.', **kwargs):
    """
    Recursively gets attribute of an object.
    With given `sep` like `.` and `attr` like `foo.bar`,
    it returns obj.foo.bar value.
    """
    attr_list = attr.split(sep, 1)
    if len(attr_list) < 2:
        if 'default' in kwargs:
            return getattr(obj, attr_list[0], kwargs['default'])
        return getattr(obj, attr_list[0])
    value = getattr(obj, attr_list[0])
    return getattr_getattr_getattr_(value, attr_list[1], sep=sep, **kwargs)


def dict_to_base64(input_dict: dict) -> str:
    # Convert dictionary to JSON string
    json_string = json.dumps(input_dict)
    # Convert JSON string to bytes and encode to Base64
    base64_bytes = base64.b64encode(json_string.encode('utf-8'))
    # Convert Base64 bytes to string
    return base64_bytes.decode('utf-8')


def base64_to_dict(base64_string: str) -> dict:
    # Decode Base64 string to bytes
    json_bytes = base64.b64decode(base64_string.encode('utf-8'))
    # Convert bytes to JSON string
    json_string = json_bytes.decode('utf-8')
    # Convert JSON string back to dictionary
    return json.loads(json_string)


def get_key_value_from_dict(
    the_dict: dict,
    the_key: str  # Should be like this: ['a'][1]['b']
):
    """
    Gives grandchilds of a dictionary.
    """
    keys = re.findall(r"\[('[^']*'|\w+)\]", the_key)
    value = the_dict
    for key in keys:
        value = value[eval(key)]
    return value
