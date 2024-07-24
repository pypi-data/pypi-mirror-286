from typing import Any, Dict
from graphql_query import Argument, Operation

def scalar_argument(key: str, value: Any) -> Argument:
    """Generate an Argument in the following form

    key: "value"
    key: true
    key: false
    ...

    """

    if isinstance(value, str):

        return Argument(name=key, value=f'"{value}"')

    elif isinstance(value, bool):
        return Argument(name=key, value=str(value).lower())

    # your cases here...

def get_query_arguments(arguments_dict: Dict[str, Any]) -> list[Argument]:
    query_arguments = []

    for key, value in arguments_dict.items():
        # processing of scalar values
        
        if isinstance(value, str) or isinstance(value, bool):
            query_arguments.append(scalar_argument(key, value))
        elif isinstance(value, int) or isinstance(value, float):
            query_arguments.append(Argument(name=key, value=value))
            
        # processing of list with objects
        elif isinstance(value, list):
            
            values = [get_query_arguments(obj) for obj in value]
            query_arguments.append(Argument(name=key, value=values))
            
        elif isinstance(value, dict):
            print("test")
            values: list[Argument] = get_query_arguments(value)
            query_arguments.append(Argument(name=key, value=values))
            
    return query_arguments
