from importlib import import_module


def import_spec_object(obj_str):
    path, obj = obj_str.rsplit('.', maxsplit=1)
    module = import_module(path)
    return getattr(module, obj)
