from ..utils.entity import get_type, get_input_types

class TestGetType:
    def test_get_type_str(self):
        input = "test"
        assert get_type(input) == 'str'
    
    def test_get_type_list(self):
        input = ["a", "b", "c"]
        assert get_type(input) == ['str', 'str', 'str']

    # This is a weird edge case. Usually inputs would not be in this format
    def test_get_type_comb_list(self):
        input = ["a", 123, "c"]
        assert get_type(input) == ['str', 'int', 'str']
    
    def test_get_type_dict(self):
        input = {"a": 123, "b": 456}
        assert get_type(input) == {'a': 'int', 'b': 'int'}

    def test_get_type_nested_dict(self):
        input = {"a": {"b": 123}, "c": 456}
        print(get_type(input))
        assert get_type(input) == {'a': {'b': 'int'}, 'c': 'int'}


class TestGetInputTypes:
    def test_get_input_types_various_types(self):
        def func_with_various_types(a: int, b: str, c: float = 3.5):
            pass
        assert get_input_types(func_with_various_types) == [
            {'name': 'a', 'type': 'int'},
            {'name': 'b', 'type': 'str'},
            {'name': 'c', 'type': 'float'}
        ]

    def test_get_input_types_dict(self):
        def func_with_dict(input_dict: dict, b: int):
            pass
        assert get_input_types(func_with_dict) == [
            {
                'name': 'input_dict',
                'type': 'dict',
            },
            {
                'name': 'b',
                'type': 'int',
            }
        ]
