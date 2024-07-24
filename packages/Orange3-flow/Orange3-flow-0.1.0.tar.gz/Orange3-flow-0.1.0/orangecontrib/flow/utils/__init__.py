import numpy as np




def objects_equal(object_a, object_b):
    if not isinstance(object_a, type(object_b)):
        return False
    
    ## Special Cases:

    if isinstance(object_a, np.ndarray):
        return np.array_equal(object_a, object_b)

    ##
    
    if not hasattr(object_a, "__dict__"):
        return object_a == object_b

    d = object_b.__dict__

    ignore = [
        ("Table", "ids"),
        ("Domain", "_indices"),
    ]

    for key, val in object_a.__dict__.items():
        if (type(object_a).__name__, key) in ignore:
            continue

        if key not in d or not objects_equal(val, d[key]):
            return False

    return True
