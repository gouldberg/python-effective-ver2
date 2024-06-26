#!/usr/bin/env PYTHONHASHSEED=1234 python3

import json


# ------------------------------------------------------------------------------
# mix-in class:  Class only defining additional methods which subclasses should provide.
#                Does not have instance attribute, not required to call __init__ constructor.
# --> Avoid multiple inheritance of class which have instance attribute or __init__ method, instead, use mix-in class.
# ------------------------------------------------------------------------------

# mix-in Class
class ToDictMixin:
    def to_dict(self):
        return self._traverse_dict(self.__dict__)

    def _traverse_dict(self, instance_dict):
        output = {}
        for key, value in instance_dict.items():
            output[key] = self._traverse(key, value)
        return output

    def _traverse(self, key, value):
        if isinstance(value, ToDictMixin):
            return value.to_dict()
        elif isinstance(value, dict):
            return self._traverse_dict(value)
        elif isinstance(value, list):
            return [self._traverse(key, i) for i in value]
        # ----------
        # hasattr:  access to attribute
        # __dict__:  dictionary of instance
        elif hasattr(value, '__dict__'):
            return self._traverse_dict(value.__dict__)
        # ----------
        else:
            return value

class BinaryTree(ToDictMixin):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

# ----------
tree = BinaryTree(10,
    left=BinaryTree(7, right=BinaryTree(9)),
    right=BinaryTree(13, left=BinaryTree(11)))


print(tree)

# convert tree to dictionary
print(tree.to_dict())


# ------------------------------------------------------------------------------
# mix-in class is useful for plugin and for overriding behavior
# ------------------------------------------------------------------------------

class BinaryTreeWithParent(BinaryTree):
    def __init__(self, value, left=None,
                 right=None, parent=None):
        super().__init__(value, left=left, right=right)
        self.parent = parent

    # override _traverse method
    def _traverse(self, key, value):
        if (isinstance(value, BinaryTreeWithParent) and
                key == 'parent'):
            # prevent cycles
            return value.value
        else:
            return super()._traverse(key, value)

# ----------
root = BinaryTreeWithParent(10)

root.left = BinaryTreeWithParent(7, parent=root)

root.left.right = BinaryTreeWithParent(9, parent=root.left)

print(root.to_dict())


# ------------------------------------------------------------------------------
# mix-in class is useful for plugin and for overriding behavior
# ------------------------------------------------------------------------------

class NamedSubTree(ToDictMixin):
    def __init__(self, name, tree_with_parent):
        self.name = name
        self.tree_with_parent = tree_with_parent

my_tree = NamedSubTree('foobar', root.left.right)

# No infinite loop
print(my_tree.to_dict())


# ------------------------------------------------------------------------------
# Generic JSON serialization mix-in
# ------------------------------------------------------------------------------

class JsonMixin:
    @classmethod
    def from_json(cls, data):
        kwargs = json.loads(data)
        return cls(**kwargs)

    def to_json(self):
        return json.dumps(self.to_dict())


class DatacenterRack(ToDictMixin, JsonMixin):
    def __init__(self, switch=None, machines=None):
        self.switch = Switch(**switch)
        self.machines = [
            Machine(**kwargs) for kwargs in machines]


class Switch(ToDictMixin, JsonMixin):
    def __init__(self, ports=None, speed=None):
        self.ports = ports
        self.speed = speed


class Machine(ToDictMixin, JsonMixin):
    def __init__(self, cores=None, ram=None, disk=None):
        self.cores = cores
        self.ram = ram
        self.disk = disk


serialized = """{
    "switch": {"ports": 5, "speed": 1e9},
    "machines": [
        {"cores": 8, "ram": 32e9, "disk": 5e12},
        {"cores": 4, "ram": 16e9, "disk": 1e12},
        {"cores": 2, "ram": 4e9, "disk": 500e9}
    ]
}"""

deserialized = DatacenterRack.from_json(serialized)

roundtrip = deserialized.to_json()

assert json.loads(serialized) == json.loads(roundtrip)
