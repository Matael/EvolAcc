# -*- coding: utf-8 -*-
#########################
#       SIMULATION      #
#########################


#########################
# IMPORTS               #
#########################
from evolacc.observer import Observable
from evolacc.placing  import Placer
from evolacc.unit     import Unit

from evolacc.config   import UNIVERSE_SIZE, FACTORY



#########################
# PRE-DECLARATIONS      #
#########################



#########################
# CLASS                 #
#########################
class Simulation(Observable):
    """
    A Simulation is a composition of Units through objects like Placer.

    Simulation is Observable, and is the target of 
    Action instances invocations.
    """


# CONSTRUCTOR #################################################################
    def __init__(self, configuration):
        self.configuration = configuration
        self.actions = []
        self.placer  = Placer()
        # call factory for each place in the world
        for coords in Placer.all_coordinates(configuration[UNIVERSE_SIZE]):
            # its impossible to have to object at the same place
            assert(None is self.placer.place(
                # place a factory generated Unit at generated coords
                configuration[FACTORY].create(self, coords), coords
            ))


# PUBLIC METHODS ##############################################################
    def step(self, times=1, configuration=None):
        """Apply times phases to simulation. If configuration is provided,
        it will replace the ancient one"""
        # configuration management
        if configuration is not None:
            self.configuration = configuration
        configuration = self.configuration # use is as shortcut
        # generate steps and invoke actions
        for coords, unit in self.placer.items():
            unit.step(self, coords)
        self._invoke_actions()

    def add(self, action):
        """Add given action to actions stack"""
        self.actions.append(action)


# PRIVATE METHODS #############################################################
    def _invoke_actions(self):
        """Invoke all actions on self, and forget them."""
        [action.execute(self) for action in self.actions]
        self.actions = []


# PREDICATS ###################################################################
# ACCESSORS ###################################################################
    @staticmethod
    def units(self):
        """Return a generator of units"""
        return (u for u in self.placer.values())

    @staticmethod
    def life(self):
        """Return a generator of units that have a genome"""
        return (u for u in self.placer.values() if u.is_life())
# CONVERSION ##################################################################
# OPERATORS ###################################################################




#########################
# FUNCTIONS             #
#########################



