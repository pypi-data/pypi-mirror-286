from . import param


def get_class_param_list(obj) -> list[param.Param]:
    variable_ids: list[str] = [attr for attr in dir(obj) if
                               not callable(getattr(obj, attr)) and not attr.startswith("__") and isinstance(getattr(obj,attr),
                                                                                                             param.Param)]
    return [getattr(obj, variable) for variable in variable_ids]


def make_param_list(*options) -> list[str]:
    return make_param_list(list[param.Param](options))


def make_param_list_(options: list[param.Param]) -> list[str]:
    result: list[str] = list()
    for option in options:
        if not option.is_active():
            continue
        result.append(option.get_value())
    return result


def make_class_param_list(obj) -> list[str]:
    return make_param_list_(get_class_param_list(obj))
