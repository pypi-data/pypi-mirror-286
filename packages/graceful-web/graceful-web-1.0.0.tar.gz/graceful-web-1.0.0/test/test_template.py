import sys
import unittest
from typing import Dict, List, Optional, Tuple, Union


sys.path.append("../graceful")


from graceful.template import Template


class TestTemplate(unittest.TestCase):
    def test_cast_basic_types(self):
        self.assertEqual(Template._cast(int, "123"), 123)
        self.assertEqual(Template._cast(float, "123.45"), 123.45)
        self.assertEqual(Template._cast(str, 123), "123")
        self.assertEqual(Template._cast(bool, 1), True)
        self.assertEqual(Template._cast(bool, 0), False)

    def test_cast_list(self):
        self.assertEqual(Template._cast(List[int], [1, "2", "3"]), [1, 2, 3])

    def test_cast_dict(self):
        self.assertEqual(
            Template._cast(Dict[str, int], {"a": "1", "b": "2"}), {"a": 1, "b": 2}
        )

    def test_cast_tuple(self):
        self.assertEqual(Template._cast(Tuple[int, str], [1, "abc"]), (1, "abc"))

    def test_cast_set(self):
        self.assertEqual(Template._cast(set[int], ["1", "2", "3"]), {1, 2, 3})

    def test_cast_union(self):
        self.assertEqual(Template._cast(Union[int, str], "123"), "123")
        self.assertEqual(Template._cast(Union[int, str], 123), 123)

    def test_cast_invalid_type(self):
        with self.assertRaises(TypeError):
            Template._cast(object, "123")

    def test_cast_strict_mode(self):
        type_annotations = {"age": int, "name": str}
        data = {"age": "25", "name": 123}
        result = Template.cast(data, type_annotations, strict=True)

        self.assertEqual(result, {"age": 25, "name": "123"})

    def test_cast_non_strict_mode(self):
        type_annotations = {"age": int, "name": str}
        data = {"age": "25", "name": 123}
        result = Template.cast(data, type_annotations, strict=False)

        self.assertEqual(result, {"age": 25, "name": "123"})

    def test_cast_invalid_data(self):
        type_annotations = {"age": int}

        with self.assertRaises(ValueError):
            Template.cast("invalid_data", type_annotations)


if __name__ == "__main__":
    unittest.main()
