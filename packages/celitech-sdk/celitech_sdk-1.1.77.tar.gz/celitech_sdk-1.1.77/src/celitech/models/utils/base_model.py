import re
from typing import List, Union, Type, Any, TypeVar, Optional
from enum import Enum
from .one_of_base_model import OneOfBaseModel

T = TypeVar("T")


class BaseModel:
    """
    A base class that most of the models in the SDK inherited from.
    """

    def __init__(self):
        pass

    def _pattern_matching(
        self, value: Optional[str], pattern: str, variable_name: str
    ) -> Optional[str]:
        """
        Checks if a value matches a regex pattern and returns the value if there's a match.

        :param value: The value to be checked.
        :type value: str
        :param pattern: The regex pattern.
        :type pattern: str
        :param variable_name: The variable name.
        :type variable_name: str
        :return: The value if it matches the pattern.
        :rtype: str
        :raises ValueError: If the value does not match the pattern.
        """
        if value is None:
            return None

        if re.match(r"{}".format(pattern), value):
            return value
        else:
            raise ValueError(
                f"Invalid value for {variable_name}: must match {pattern}, received {value}"
            )

    def _enum_matching(
        self, value: Union[str, Enum], enum_values: List[str], variable_name: str
    ) -> Union[str, Enum]:
        """
        Checks if a value (str or enum) matches the required enum values and returns the value if there's a match.

        :param value: The value to be checked.
        :type value: Union[str, Enum]
        :param enum_values: The list of valid enum values.
        :type enum_values: List[str]
        :param variable_name: The variable name.
        :type variable_name: str
        :return: The value if it matches one of the enum values.
        :rtype: Union[str, Enum]
        :raises ValueError: If the value does not match any of the enum values.
        """
        if value is None:
            return None

        str_value = value.value if isinstance(value, Enum) else value
        if str_value in enum_values:
            return value
        else:
            raise ValueError(
                f"Invalid value for {variable_name}: must match one of {enum_values}, received {value}"
            )

    def _define_object(self, input_data: Any, input_class: Type[T]) -> Optional[T]:
        """
        Check if the input data is an instance of the input class and return the input data if it is.
        Otherwise, return an instance of the input class.

        :param input_data: The input data to be checked.
        :param input_class: The class that the input data should be an instance of.
        :return: The input data if it is an instance of input_class, otherwise an instance of input_class.
        :rtype: object
        """
        if input_data is None:
            return None
        elif isinstance(input_data, input_class):
            return input_data
        else:
            return input_class._unmap(input_data)

    def _define_list(
        self, input_data: Optional[List[Any]], list_class: Type[T]
    ) -> Optional[List[T]]:
        """
        Create a list of instances of a specified class from input data.
        :param input_data: The input data to be transformed into a list of instances.
        :param list_class: The class that each instance in the list should be an instance of.
        :return: A list of instances of list_class.
        :rtype: list
        """

        if input_data is None:
            return None

        result: List[T] = []
        for item in input_data:
            if hasattr(list_class, "__args__") and len(list_class.__args__) > 0:
                class_list = self.__create_class_map(list_class)
                OneOfBaseModel.class_list = class_list
                result.append(OneOfBaseModel.return_one_of(item))
            elif issubclass(list_class, Enum):
                result.append(
                    self._enum_matching(item, list_class.list(), list_class.__name__)
                )
            elif isinstance(item, list_class):
                result.append(item)
            elif isinstance(item, dict):
                result.append(list_class._unmap(item))
            else:
                result.append(list_class(item))
        return result

    def _get_representation(self, level: int = 0) -> str:
        """
        Get a string representation of the model.

        :param int level: The indentation level.
        :return: A string representation of the model.
        """
        indent = "    " * level
        representation_lines = []

        for attr, value in vars(self).items():
            if value is not None:
                value_representation = (
                    value._get_representation(level + 1)
                    if hasattr(value, "_get_representation")
                    else repr(value)
                )
                representation_lines.append(
                    f"{indent}    {attr}={value_representation}"
                )

        return (
            f"{self.__class__.__name__}(\n"
            + ",\n".join(representation_lines)
            + f"\n{indent})"
        )

    def __str__(self):
        return self._get_representation()

    def __repr__(self):
        return self._get_representation()

    def __create_class_map(self, union_type):
        """
        Create a dictionary that maps class names to the actual classes in a Union type.

        :param union_type: The Union type to create a class map for.
        :return: A dictionary mapping class names to classes.
        :rtype: dict
        """
        class_map = {}
        for arg in union_type.__args__:
            if arg.__name__:
                class_map[arg.__name__] = arg
        return class_map
