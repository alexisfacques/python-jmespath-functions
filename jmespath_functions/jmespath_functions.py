"""Function extensions for the JMESPath language."""
from typing import Any, Dict, List, Union

# From requirements.txt:
import jmespath


class JmespathFunctions(jmespath.functions.Functions):
    """Function extensions for the JMESPath language."""

    @jmespath.functions.signature({'types': ['object']}, {'types': ['string', 'object', 'array']})
    def _func_exclude(self, obj: Dict[str, Any],
                      excludes: Union[Dict[str, Any], str, List[str]]) \
            -> Dict[str, Any]:
        """
        Exclude key-value pairs from a list of dictionnaries.

        :usage:
        Given input: [{'id': 'foo', 'bar': 'baz'}]
        Example of query: [*].exclude(@, 'id')
        Returns: [{'bar': 'baz'}]

        :param obj: the object to transform.
        :param excludes: a key, list of keys, enumeration of keys to exclude
                         for the given object.

        :return: the object pruned off the excluded keys list.
        """
        return {k: v for k, v in obj.items() if k not in ((excludes,)
                if isinstance(excludes, str) else excludes)}

    @jmespath.functions.signature({'types': ['object']}, {'types': ['array']})
    def _func_map_merge(self, obj: Dict[str, Any], elements: List[Dict[str, Any]]):
        """
        Merge parent dictionnary keys in a list of objects.

        :usage:
        Given input: [{'id': 'foo', 'bar': ['baz']}]
        Example of query: [*].map_merge({'id': id}, @.bar[])[]
        Returns: [{'id': 'foo', 'bar': 'baz'}]

        :param obj: the parent object to map_merge into a list
        :param elements: the elements to which map_merge parent dictionnary keys.

        :return: a list of objects, map_merged with the parent keys.
        """
        result = []
        for element in elements:
            merged_object = super()._func_merge(obj, element)
            result.append(merged_object)
        return result

    @jmespath.functions.signature({'types': ['string', 'array']}, {'types': ['number', 'string']})
    def _func_slice(self, to_be_sliced: str,
                    start_from: Union[int, str]) -> str:
        """
        Slice a string starting from a given index position.

        :usage:
        Given input: 'fooBarBaz'
        Example of query: *.slice(@, '1')
        Returns: ooBarBaz

        :param to_be_sliced: the string or list to transform.
        :param start_from: a index position.
        :return: the string of list pruned off the excluded keys list.
        """
        return to_be_sliced[int(start_from):]


def search(*args, **kwargs):
    """
    JMESPath search function alias utilizing the JmespathFunctions custom functions.

    :param args: JMESPath search positionnal arguments.
    :param kwargs: JMESPath search key-word arguments.

    :return: what JMESPath search returns.
    """
    return jmespath.search(*args, options=jmespath.Options(custom_functions=JmespathFunctions()),
                           **{k: v for k, v in kwargs.items() if k not in ('options',)})
