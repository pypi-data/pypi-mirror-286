import json
from typing import Any, Dict, Mapping, Type, Union, get_args, get_origin


class Template:
    @staticmethod
    def _cast(expected_type: Type[Any], value: Any) -> Any:
        if expected_type is None and value is None:
            return value
        
        if expected_type is Any:
            return value
        
        if isinstance(expected_type, type):
            return expected_type(value)
        
        origin_type = get_origin(expected_type)
        type_args = get_args(expected_type)

        if origin_type is dict:
            key_type, value_type = type_args
            return {
                Template._cast(key_type, k): Template._cast(value_type, v)
                for k, v in value.items()
            }
        
        elif origin_type is list:
            return [Template._cast(type_args[0], item) for item in value]
        
        elif origin_type is tuple:
            return tuple(Template._cast(type_args[i], item) for i, item in enumerate(value))
        
        elif origin_type is set:
            return {Template._cast(type_args[0], item) for item in value}

        elif origin_type is Union:
            if isinstance(value, type_args):
                return value

            for union_type in type_args:
                return Template._cast(union_type, value)
    
        else:
            raise TypeError(f"Unsupported type {expected_type}.")

    @staticmethod
    def cast(
        data: Union[bytes, bytearray, str, Mapping],
        type_annotations: Dict[str, Type],
        strict: bool = False,
    ) -> Dict[str, Any]:
        if isinstance(data, (bytes, bytearray, str)):
            data = json.loads(data)

        if not isinstance(data, Mapping):
            raise ValueError("Data must be a dictionary or a JSON-compatible format.")

        results = {}

        for key, item in data.items():
            expected_type = type_annotations.get(key)
            
            try:
                results[key] = Template._cast(expected_type, item)

            except (ValueError, TypeError) as e:
                if strict:
                    raise e
                results[key] = item

        return results

    def __init__(
        self, data: Union[bytes, bytearray, str, Mapping], strict: bool = False
    ) -> None:
        self.__dict__.update(self.cast(data, self.__annotations__, strict))
