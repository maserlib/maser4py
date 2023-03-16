# -*- coding: utf-8 -*-


from maser.data.base.class_factory import data_class_factory
from .data import (
    ExpresCdfData
)

# def expres_class_factory(observer, source) :
#     dataset = f'{ExpresCdfData.dataset}_{observer}_{source}'
#     class NewClass(ExpresCdfData, dataset=dataset): pass
#     class_name = f'{ExpresCdfData.dataset}{observer}{source}'
#     NewClass.__name__ = class_name
#     NewClass.__qualname__ = class_name
#     NewClass.__doc__ = "Expres Test"
#     return NewClass


observer_list = [
    'earth',
    'cassini',
    'juno',
    'stereoA',
    'stereoB',
    'ulysses',
    'voyager1'
]

source_list = [
    'jupiter_ganymede',
    'jupiter_io',
    'jupiter_europa',
    'jupiter_callisto'
]

for obs in observer_list:
    for src in source_list:
        planet, moon = src.split('_')
        class_name = f"Expres{obs.title()}{planet.title()}{moon.title()}"
        new_class = data_class_factory(
            BaseClass=ExpresCdfData,
            dataset=f'expres_{obs}_{src}',
            class_name=class_name,
            class_doc=f'EXPRES {class_name} dataset'
        )
        globals()[new_class.__name__] = new_class

