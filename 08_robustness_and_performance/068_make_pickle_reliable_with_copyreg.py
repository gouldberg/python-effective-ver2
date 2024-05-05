#!/usr/bin/env PYTHONHASHSEED=1234 python3

import pickle
import copyreg


# ------------------------------------------------------------------------------
# pickle dump (to file) current state and load
# ------------------------------------------------------------------------------

class GameState:
    def __init__(self):
        self.level = 0
        self.lives = 4


state = GameState()
state.level += 1  # Player beat a level
state.lives -= 1  # Player had to try again

print(state.__dict__)


state_path = '00_tmp/game_state.bin'

with open(state_path, 'wb') as f:
    pickle.dump(state, f)

with open(state_path, 'rb') as f:
    state_after = pickle.load(f)

print(state_after.__dict__)


# ------------------------------------------------------------------------------
# Confusion:
# old pickle dumped data (before updated class) instance IS instance of new updated class ....
# ------------------------------------------------------------------------------

class GameState:
    def __init__(self):
        self.level = 0
        self.lives = 4
        self.points = 0  # New field


state = GameState()

# ----------
# now not dump to file
# use 'dumps' serialized file and 'loads'
serialized = pickle.dumps(state)
serialized

state_after = pickle.loads(serialized)
state_after

# now OK
print(state_after.__dict__)


# ----------
# now load old saved pickled data.
with open(state_path, 'rb') as f:
    state_after = pickle.load(f)

# no points
print(state_after.__dict__)

# but GameState instance !!!
assert isinstance(state_after, GameState)


# ------------------------------------------------------------------------------
# copyreg:
# register function for serialization and deserialization to control pickle behavior and make it reliable
#
# Now we add new state attribute to class
# ------------------------------------------------------------------------------

# set default in constructor
class GameState:
    def __init__(self, level=0, lives=4, points=0):
        self.level = level
        self.lives = lives
        self.points = points


def pickle_game_state(game_state):
    kwargs = game_state.__dict__
    return unpickle_game_state, (kwargs,)


def unpickle_game_state(kwargs):
    return GameState(**kwargs)


# ----------
# copyreg:
# register function for serialization and deserialization to control pickle behavior and make it reliable
copyreg.pickle(GameState, pickle_game_state)


# ----------
state = GameState()
print('Before:', state.__dict__)

# change state
state.points += 1000

# dumps and loads
serialized = pickle.dumps(state)
state_after = pickle.loads(serialized)

print('After: ', state_after.__dict__)


# ----------
# change GameState
class GameState:
    def __init__(self, level=0, lives=4, points=0, magic=5):
        self.level = level
        self.lives = lives
        self.points = points
        self.magic = magic  # New field


# NOW state.__dict__ does NOT have attribute magic
print('Before:', state.__dict__)

# load old serialized data
state_after = pickle.loads(serialized)

# !!! NOW state.__dict__ have attribute magic by default value !!!
print('After: ', state_after.__dict__)


# ------------------------------------------------------------------------------
# Now we remove attribute to class, No backward compatibility
# Version control
# ------------------------------------------------------------------------------

# remove self.lives
class GameState:
    def __init__(self, level=0, points=0, magic=5):
        self.level = level
        self.points = points
        self.magic = magic


# TypeError: GameState.__init__()
pickle.loads(serialized)


# ----------
# add version
def pickle_game_state(game_state):
    kwargs = game_state.__dict__
    kwargs['version'] = 2
    return unpickle_game_state, (kwargs,)


# version control
def unpickle_game_state(kwargs):
    version = kwargs.pop('version', 1)
    if version == 1:
        del kwargs['lives']
    return GameState(**kwargs)


# register to copyreg.
copyreg.pickle(GameState, pickle_game_state)


# now we can load (deserialize) old serialized data
print('Before:', state.__dict__)

state_after = pickle.loads(serialized)
print('After: ', state_after.__dict__)


# ------------------------------------------------------------------------------
# Change class name --> clear copyreg table and register new class
# ------------------------------------------------------------------------------

# now clear table copyreg 
copyreg.dispatch_table.clear()


# serialize current updated GameState() instance and delete its class 
state = GameState()
serialized = pickle.dumps(state)

del GameState


# ----------
# change class name
class BetterGameState:
    def __init__(self, level=0, points=0, magic=5):
        self.level = level
        self.points = points
        self.magic = magic


# now AttributeError: Can't get attribute 'GameState' on ...
pickle.loads(serialized)

# because import path is serialized as 'GameState' ...
print(serialized)


# ----------
# register new class by copyreg
copyreg.pickle(BetterGameState, pickle_game_state)

state = BetterGameState()
serialized = pickle.dumps(state)

# now the import path is 'BetterGameState' ...
print(serialized)