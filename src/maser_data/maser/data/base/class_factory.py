# -*- coding: utf-8 -*-


__all__ = ["data_class_factory"]


def data_class_factory(BaseClass, dataset, class_name, class_doc):
    class NewClass(BaseClass, dataset=dataset):
        pass

    NewClass.__name__ = class_name
    NewClass.__qualname__ = class_name
    NewClass.__doc__ = class_doc
    return NewClass
