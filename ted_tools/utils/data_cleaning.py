import json
import ast

# Unique placeholder for single quotes in strings
UNIQUE_PLACEHOLDER = "__UNIQUE_SINGLE_QUOTE__"


def preprocess_string_for_eval(input_str):
    """
    Temporarily replaces single quotes in strings with a unique placeholder.
    """
    return input_str.replace("'", UNIQUE_PLACEHOLDER)


def postprocess_eval_dict(eval_dict):
    """
    Recursively reverts placeholders back to single quotes in the resulting dictionary.
    """
    if isinstance(eval_dict, dict):
        return {k: postprocess_eval_dict(v) for k, v in eval_dict.items()}
    elif isinstance(eval_dict, list):
        return [postprocess_eval_dict(v) for v in eval_dict]
    elif isinstance(eval_dict, str):
        return eval_dict.replace(UNIQUE_PLACEHOLDER, "'")
    else:
        return eval_dict


def clean_dict(data):
    """
    The `clean_dict` function recursively cleans a dictionary by removing backslashes from keys and
    handling nested dictionaries and lists.

    Args:
      data: The `clean_dict` function takes a dictionary as input and cleans it by removing backslashes
    from the keys. It recursively cleans nested dictionaries and lists within the input dictionary.

    Returns:
      The `clean_dict` function is returning a cleaned version of the input data. It processes
    dictionaries by cleaning keys (removing backslashes) and recursively cleaning nested dictionaries
    and lists. The cleaned dictionary is returned as the output. If the input data is not a dictionary
    or a list, it is returned as is.
    """
    if isinstance(data, dict):
        new_dict = {}
        for key, value in data.items():
            # Correctly handle and clean keys by removing backslashes
            cleaned_key = key.replace("\\_", "_")
            if isinstance(value, list):
                new_dict[cleaned_key] = [
                    clean_dict(v) if isinstance(v, (dict, list)) else v for v in value
                ]
            else:
                new_dict[cleaned_key] = (
                    clean_dict(value) if isinstance(value, dict) else value
                )
        return new_dict
    elif isinstance(data, list):
        return [clean_dict(item) for item in data]
    return data


def clean_for_youtube_metadata(data):
    """
    Cleans the data to match the YoutubeMetadata model expectations.
    """
    cleaned_data = {}

    # Fields that should be lists of strings
    list_fields = ["titles", "thumbnail_prompts", "hashtags"]
    # Fields that should be single strings
    string_fields = ["description", "transcript"]

    for key, value in data.items():
        if key in list_fields:
            # Ensure the value is a list of strings
            if isinstance(value, list) and all(isinstance(item, str) for item in value):
                cleaned_data[key] = value
            elif isinstance(value, dict):
                # Example handling if the dictionary has a specific structure you expect
                # This is just a placeholder logic; adjust according to your actual data structure
                cleaned_data[key] = value.get("examples", [])
            else:
                # Fallback or error handling
                cleaned_data[key] = []
        elif key in string_fields:
            # Ensure the value is a string
            if isinstance(value, str):
                cleaned_data[key] = value
            elif isinstance(value, dict):
                # If the dictionary has a 'description' or similar field, use it
                cleaned_data[key] = value.get("examples", "")
            else:
                # Fallback or error handling
                cleaned_data[key] = ""
        else:
            # Handle any other fields as needed
            cleaned_data[key] = value

    return cleaned_data
