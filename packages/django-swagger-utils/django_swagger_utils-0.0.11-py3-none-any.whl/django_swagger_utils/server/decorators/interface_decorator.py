from functools import wraps
from django.http import JsonResponse


def validate_decorator(validator_class):
    @wraps(validator_class)
    def wrapper(request, *args, **kwargs):
        # Custom logic before the validator_class is called
        validator_instance = validator_class(request, *args, **kwargs)
        result = validator_instance.validate()
        print("result in validate_decorator: ", result)
        # if isinstance(result, dict):
            # Convert the dictionary to a JsonResponse
            # return result
        # else:
            # If result is not a dictionary, return it as-is
            # return result

    return wrapper