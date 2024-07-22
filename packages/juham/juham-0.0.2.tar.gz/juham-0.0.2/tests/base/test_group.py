import unittest
from juham.base import Object, Base, Group


class TestGroup(unittest.TestCase):

    def test_constructor(self):
        ok = False
        try:
            object = Group("group")
            self.assertNotNull(object)
        except Exception:
            ok = True

        self.assertTrue(ok)

    def test_get_classid(self):
        classid = Group.get_class_id()
        self.assertEqual("Group", classid)

    def test_add(self):
        group = Group("parent")
        child = Object("child")
        group.add(child)
        self.assertEqual(1, len(group.children))

    def test_serialization(self):
        """Create hierarchical object and assert deserialization restores the
        structure.

        Group("mygroup") ├─ Object("child1") ├─ Base("child2") ├─
        Group("child3") │   └─ Object("child4")
        """
        group = Group("mygroup")
        child1 = Object("child1")
        group.add(child1)
        child2 = Base("child2")
        group.add(child2)
        sub_group = Group("child3")
        group.add(sub_group)
        child_of_subgroup = Object("child4")
        sub_group.add(child_of_subgroup)

        #  make sure the hierarchy is what we expect
        self.assertEqual(3, len(group.children))
        self.assertEqual(1, len(sub_group.children))

        # serialize
        filename = "group.json"
        with open(filename, "w") as f:
            group.serialize_to_json(f)

        # deserialize
        group2 = Group("bar")
        with open(filename, "r") as f:
            group2.deserialize_from_json(f)
        self.assertEqual("mygroup", group2.name)
        #  make sure the hierarchy is what we expect
        self.assertEqual(3, len(group2.children))


if __name__ == "__main__":
    unittest.main()
