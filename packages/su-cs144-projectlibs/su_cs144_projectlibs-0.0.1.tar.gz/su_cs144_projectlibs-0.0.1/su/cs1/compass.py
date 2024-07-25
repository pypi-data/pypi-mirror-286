import random as _rnd
from random import Random as _Random
from string import ascii_uppercase as _ascii_uppercase, digits as _digits
import os as _os
import math as _math


class _Seeder():
    def __init__(self, seed):
        self.seeder = _Random(seed)
        self.seen = {}
        self.init_state = self.seeder.getstate()

    def get_seed(self, row, col):
        seed = None
        if ((col, row) in self.seen):
            state = self.seen[(col, row)]
            self.seeder.setstate(state)
        else:
            self.seeder.setstate(self.init_state)
        seed = ''.join(self.seeder.choices(_ascii_uppercase + _digits, k=128))
        self.seen[(col, row)] = self.seeder.getstate()
        return seed


# Set up the global seeder
_seeder = None
if ('BEE_SEARCH_SEED' in _os.environ):
    _seeder = _Seeder(_os.environ['BEE_SEARCH_SEED'])


class Trajectory:
    """
    A trajectory for a moving entity. The trajectory is a single straight-line
    movement of an entity and includes the direction the entity will move in,
    and the distance it will move.
    """
    def __init__(self, direction: float, distance: int, degrees=False):
        """Create a new trajectory with the given direction and distance. The
        direction can be specified in radians or degrees (default radians)"""
        self.distance = distance
        if (degrees):
            self.direction = _math.radians(direction)
        else:
            self.direction = direction

    def get_direction_in_degrees(self) -> float:
        """Retrieve the direction component of the trajectory in degrees"""
        return _math.degrees(self.direction)

    def get_direction_in_radians(self) -> float:
        """Retrieve the direction component of the trajectory in radians"""
        return self.direction

    def get_distance(self) -> int:
        """Retrieve the distance component of the trajectory"""
        return self.distance

    def __str__(self):
        return "("+"{:.2f}".format(self.direction)+", "+str(self.distance)+")"


class Compass:
    """
    Supplies a single map entity with trajectories which dictate the path the
    entity will take. NOTE: Each map entity MUST USE A SEPARATE compass.
    """
    def __init__(self, row: int, col: int, speed: int):
        """
        Create a new compass for the map entity starting at the given location,
        which gives directions in the form of trajectories to the entity based
        on the given speed of the entity.
        """
        self.speed = speed
        if (_seeder is not None):
            seed = _seeder.get_seed(row, col)
            self.rand = _Random(str(seed)+str(row)+str(col))
        else:
            self.rand = _Random()
        self.scout = bool(self.rand.getrandbits(1))

    def get_next_trajectory(self) -> Trajectory:
        """Return the next trajectory that the map entity must take."""
        # Generate direction
        angle = self.rand.vonmisesvariate(0, 0)
        direction = (angle//(0.25*_math.pi))*(0.25*_math.pi)
        # Generate distance
        distance = _math.ceil(self.rand.triangular(0, self.speed, self.speed))
        # return trajectory
        return Trajectory(direction, distance)

    def is_scout(self) -> bool:
        """
        When this compass is given to a Honey Bee, determine if the Honey Bee
        should be a scout or a forager. This method can be called multiple
        times and will always return the same result for a particular Honey Bee.
        """
        return self.scout
