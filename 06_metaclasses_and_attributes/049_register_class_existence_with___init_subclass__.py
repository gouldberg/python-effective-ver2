#!/usr/bin/env PYTHONHASHSEED=1234 python3

import json


# ------------------------------------------------------------------------------
# Get serialized object of the class
# ------------------------------------------------------------------------------

class Serializable:
    def __init__(self, *args):
        self.args = args

    def serialize(self):
        return json.dumps({'args': self.args})


class Point2D(Serializable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Point2D({self.x}, {self.y})'

point = Point2D(5, 3)

print('Object:    ', point)
print('Serialized:', point.serialize())


# ------------------------------------------------------------------------------
# Deserializable, which inherit from Serializable
# ------------------------------------------------------------------------------

# This inherit Serializable
class Deserializable(Serializable):
    @classmethod
    def deserialize(cls, json_data):
        params = json.loads(json_data)
        return cls(*params['args'])


# This inherit Not Serializable but Deserializable
# (other code is same as Point2D class)
class BetterPoint2D(Deserializable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Point2D({self.x}, {self.y})'


before = BetterPoint2D(5, 3)
print('Before:    ', before)

data = before.serialize()
print('Serialized:', data)

after = BetterPoint2D.deserialize(data)
print('After:     ', after)


# ------------------------------------------------------------------------------
# More generic:
# class name set (register) in JSON data
# ------------------------------------------------------------------------------

class BetterSerializable:
    def __init__(self, *args):
        self.args = args

    # ----------
    # class name set in JSON data
    def serialize(self):
        return json.dumps({
            'class': self.__class__.__name__,
            'args': self.args,
        })

    def __repr__(self):
        name = self.__class__.__name__
        args_str = ', '.join(str(x) for x in self.args)
        return f'{name}({args_str})'

registry = {}

def register_class(target_class):
    registry[target_class.__name__] = target_class


# now deserialize function works for normal any class.
def deserialize(data):
    params = json.loads(data)
    name = params['class']
    target_class = registry[name]
    return target_class(*params['args'])


class EvenBetterPoint2D(BetterSerializable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y


register_class(EvenBetterPoint2D)

# registered class
registry


# ----------
before = EvenBetterPoint2D(5, 3)
print('Before:    ', before)

data = before.serialize()
print('Serialized:', data)

after = deserialize(data)
print('After:     ', after)


# -->
# This program risks for forgetting calling register_class()


# ------------------------------------------------------------------------------
# use meta class
# ------------------------------------------------------------------------------

class Meta(type):
    def __new__(meta, name, bases, class_dict):
        cls = type.__new__(meta, name, bases, class_dict)
        register_class(cls)
        return cls

class RegisteredSerializable(BetterSerializable,
                             metaclass=Meta):
    pass


class Vector3D(RegisteredSerializable):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)
        self.x, self.y, self.z = x, y, z

before = Vector3D(10, -7, 3)
print('Before:    ', before)

data = before.serialize()
print('Serialized:', data)
print('After:     ', deserialize(data))


# ------------------------------------------------------------------------------
# use __init__subclass__
# ------------------------------------------------------------------------------

class BetterRegisteredSerializable(BetterSerializable):
    def __init_subclass__(cls):
        super().__init_subclass__()
        register_class(cls)


class Vector1D(BetterRegisteredSerializable):
    def __init__(self, magnitude):
        super().__init__(magnitude)
        self.magnitude = magnitude


before = Vector1D(6)
print('Before:    ', before)


data = before.serialize()
print('Serialized:', data)
print('After:     ', deserialize(data))
