# -*- coding: utf-8 -*-


from maser.data.base.class_factory import data_class_factory
from .plot import ExpresCdfPlot


observer_list = [
    "earth",
    "cassini",
    "juno",
    "stereoA",
    "stereoB",
    "ulysses",
    "voyager1",
]

magnetic_field_models = ["isaac", "jrm09"]

source_list = ["jupiter_ganymede", "jupiter_io", "jupiter_europa", "jupiter_callisto"]

# Automatically create all the different ExpresCdfData classes that matches the various available datasets.
# These new classes inherit from ExpresCdfData.
for obs in observer_list:
    for src in source_list:

        # Sort out the name
        planet, moon = src.split("_")
        class_name = f"Expres{obs.title()}{planet.title()}{moon.title()}"

        # Generate the class
        new_class = data_class_factory(
            BaseClass=ExpresCdfPlot,
            dataset=f"expres_{obs}_{src}",
            class_name=class_name,
            class_doc=f"EXPRES {class_name} dataset",
        )

        # Set the new class as globally accessible in order to be detectable
        # E.g.:
        #     from maser.data import Data
        #     Data._registry
        # should contain all the 'expres_*' datasets
        globals()[new_class.__name__] = new_class
