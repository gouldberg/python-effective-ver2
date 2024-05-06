#!/usr/bin/env PYTHONHASHSEED=1234 python3


# ------------------------------------------------------------------------------
# implement explicitly getter and setter method in class
# ------------------------------------------------------------------------------

class OldResistor:
    def __init__(self, ohms):
        self._ohms = ohms

    def get_ohms(self):
        return self._ohms

    def set_ohms(self, ohms):
        self._ohms = ohms


# ----------
# constructor
r0 = OldResistor(50e3)
print('Before:', r0.get_ohms())


# set (update)
r0.set_ohms(10e3)
print('After: ', r0.get_ohms())


# ----------
# but when setting, need to get() ...
r0.set_ohms(r0.get_ohms() - 4e3)

# when check value, need get()
assert r0.get_ohms() == 6e3


# ------------------------------------------------------------------------------
# For Python, start with public attribute
# this will suffice in simple case
# ------------------------------------------------------------------------------

class Resistor:
    def __init__(self, ohms):
        self.ohms = ohms
        self.voltage = 0
        self.current = 0


r1 = Resistor(50e3)

r1.ohms = 10e3

print(f'{r1.ohms} ohms, '
      f'{r1.voltage} volts, '
      f'{r1.current} amps')


# ----------
r1.ohms += 5e3


# ------------------------------------------------------------------------------
# @property (getter)
# @attributename.setter (setter)
# ------------------------------------------------------------------------------

class Resistor:
    def __init__(self, ohms):
        self.ohms = ohms
        self.voltage = 0
        self.current = 0


class VoltageResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)
        self._voltage = 0

    # self.voltage --> self._voltage
    @property
    def voltage(self):
        return self._voltage

    @voltage.setter
    def voltage(self, voltage):
        self._voltage = voltage
        self.current = self._voltage / self.ohms


# ----------
# constructor:
r2 = VoltageResistance(1e3)

# now, self.voltage --> self._voltage
r2.__dict__
print(f'Before: {r2.current:.2f} amps')


# setter:
# now, self.voltage --> self._voltage
# now, self.voltage update self.current too.
r2.voltage = 10

r2.__dict__
print(f'After:  {r2.current:.2f} amps')


# ------------------------------------------------------------------------------
# @property (getter)
# @attributename.setter (setter)
#  can also be applied to some checks and introspections.
# ------------------------------------------------------------------------------

class BoundedResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)

    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if ohms <= 0:
            raise ValueError(f'ohms must be > 0; got {ohms}')
        self._ohms = ohms


r3 = BoundedResistance(1e3)

# setter
# ValueError: ohms must be > 0; got 0
r3.ohms = 0


# constructor
# ValueError: ohms must be > 0; got -5
BoundedResistance(-5)


# ------------------------------------------------------------------------------
# @property (getter)
# @attributename.setter (setter)
#  can also make immutable attributes of super class
# ------------------------------------------------------------------------------

class FixedResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)

    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if hasattr(self, '_ohms'):
            raise AttributeError("Ohms is immutable")
        self._ohms = ohms


r4 = FixedResistance(1e3)

r4.ohms = 2e3


# ------------------------------------------------------------------------------
# Do NOT set other property in getter
# ------------------------------------------------------------------------------

class MysteriousResistor(Resistor):

    # here in getter method, other property is set.
    @property
    def ohms(self):
        self.voltage = self._ohms * self.current
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        self._ohms = ohms


r7 = MysteriousResistor(10)
r7.__dict__

r7.current = 0.01
r7.__dict__

# get ohms but voltage is updated ....
r7.ohms
r7.__dict__
