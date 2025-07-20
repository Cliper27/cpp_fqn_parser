from typing import Dict, Any


def to_dict(obj: Any) -> Dict[str, Any]:
    """
    Recursively converts an object and its attributes into a dictionary.

    This function inspects the given object and returns a dictionary of its attributes.
    If any attribute is:
    - An object with a `to_dict()` method, it calls that method.
    - A list, it recursively serializes each item.
    - A dict, it recursively serializes each value.
    - A primitive type (str, int, float, etc.), it leaves it unchanged.

    This is useful for converting nested objects into JSON-serializable dictionaries.

    Args:
        obj (Any): The object to convert.

    Returns:
        Dict[str, Any]: A dictionary representing the object's attributes and their serialized values.
    """
    def serialize(inner_obj):
        if hasattr(inner_obj, "to_dict"):
            return inner_obj.to_dict()
        elif isinstance(inner_obj, list):
            return [serialize(item) for item in inner_obj]
        elif isinstance(inner_obj, dict):
            return {k: serialize(v) for k, v in inner_obj.items()}
        else:
            return inner_obj

    return {k: serialize(v) for k, v in vars(obj).items()}
