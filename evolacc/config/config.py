# -*- coding: utf-8 -*-
#########################
#     CONFIGPARSER      #
#########################
"""
This module is here for simplify work of __main__.
This module provide a decorator for docopt module.

Do something like:
    import config 
    configuration = config.generate_from(__doc__)

Then args will be equal to usable dictionnary like object.
In fact, this dictionnary will be a ChainMap that will take 
count, in order, of command-line arguments, configuration file, 
and default values defined in this file.

configparser will also intercept some arguments, like those that 
trigger saving or loading of (non-)existing configurations.
"""


#########################
# IMPORTS               #
#########################
from evolacc.unit.component import Genome

from collections import ChainMap
from docopt      import docopt
import importlib
import json
import sys
import os





#########################
# PRE-DECLARATIONS      #
#########################
# directories and files
DIRCNAME_USER_GENOMES = 'evolacc/usergenomes/'
FILENAME_CONFIG       = 'data/inputs/config.json'
# configuration keys
UNIVERSE_SIZE   = 'universe_size'
GENOMES_CLASSES = 'genomes_classes'
CONFIG_FILE     = 'config_file'




#########################
# GENERATE_FROM         #
#########################
def generate_from(docstring):
    """
    Collect information from given docstring,
    configuration file, and default values.
    Generate and return a dict like object
    that have all keys accessibles.
    """
    # CREATE COMMAND LINE ARGUMENTS CONFIGURATION
    config_args = __parse_from_doc(docstring)

    # TODO: CREATE FILE CONFIGURATION
    config_file = __parse_from_file(
        config_args.get(CONFIG_FILE, FILENAME_CONFIG)
    )

    # TODO: CREATE DEFAULT CONFIGURATION
    config_default = __default_configuration()

    # CREATE AND RETURN FINAL CONFIGURATION
    configuration = ChainMap({}, config_args, config_file, config_default)
    return configuration




#########################
# PARSE FROM DOC        #
#########################
def __parse_from_doc(docstring):
    """
    Collect information from docstring with help of docopt
    Return a dictionnary with all interesting options.
    """
    # CREATE COMMAND LINE ARGUMENTS CONFIGURATION
    # Parse args with docopt and keep those are interestings
    args = docopt(docstring)
    config_args = {k.lstrip('-'):v         # don't keep the firsts '-'
                   for k,v in args.items() 
                   if v is not None and k.startswith('-')}

    # universe size must be treat as a list of integer
    if UNIVERSE_SIZE in config_args:
        config_args[UNIVERSE_SIZE] = tuple((
            int(_) for _ in config_args[UNIVERSE_SIZE].split(',')
        ))

    # import users genomes
    if GENOMES_CLASSES in config_args:
        config_args[GENOMES_CLASSES] = __import_user_genomes(
            config_args[GENOMES_CLASSES]
        )

    return config_args



#########################
# PARSE FROM FILE       #
#########################
def __parse_from_file(filename=FILENAME_CONFIG):
    """
    Collect information from config file, formatted in json.
    Return a dictionnary with all interesting options.
    Wait optionnaly the config filename.
    NOT IMPLEMENTED
    """
    return {}




#########################
# DEFAULT CONFIGURATION #
#########################
def __default_configuration():
    """
    Return dict that describes the default configuration.
    NOT IMPLEMENTED
    """
    return {}




#########################
# IMPORT USER GENOMES   #
#########################
def __import_user_genomes(genomes):
    """
    Import all genomes from modules in user genomes directory.
    Given genomes must be a list of string that contain name of
    wanted Genome realizations.
    Return a list of class, garanteed Genome realizations. 
    If a class is found multiple times, it will be added multiple times. 
    If a class is not found, no error will be reported.
    If a class is not a Genome subclass, an error will be reported.
    """
    classes = []
    # open python modules in user genomes directory
    # ex: 'evolacc/usergenomes/thing.py' -> 'evolacc.usergenomes.thing'
    modules = (DIRCNAME_USER_GENOMES.replace('/', '.')+os.path.splitext(f)[0] 
               for f in os.listdir(DIRCNAME_USER_GENOMES) 
               if os.path.splitext(f)[1] == '.py' and f != '__init__.py'
              )
    # collect all expected classes in usergenomes list
    for module in modules:
        # import user module
        module = importlib.import_module(module, package='evolacc')
        # collect expected classes
        for cls in module.__dict__.keys():
             if cls in module.__dict__:
                classes.append(module.__getattribute__(cls))
    # verify and attach collected genomes to args configuration
    assert(all(issubclass(usergenome, Genome) for usergenome in classes)) # TODO: replace by logging
    return classes




