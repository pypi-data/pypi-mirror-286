import unittest
from juham.base import Object


class TestObject(unittest.TestCase):

    def test_constructor(self):
        ok = False
        try:
            object = Object("foo")
            self.assertNotNull(object)
        except Exception:
            ok = True

        self.assertTrue(ok)

    def test_get_classid(self):
        classid = Object.get_class_id()
        self.assertEqual("Object", classid)

    def test_serialization(self):

        obj = Object("foo")
        with open("foo.json", "w") as f:
            obj.serialize_to_json(f)
        obj2 = Object("bar")
        with open("foo.json", "r") as f:
            obj2.deserialize_from_json(f)
        self.assertEqual("foo", obj2.name)


if __name__ == "__main__":

    unittest.main()
