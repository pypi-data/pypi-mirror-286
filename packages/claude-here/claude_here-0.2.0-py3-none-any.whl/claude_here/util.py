#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xf5a97254

# Compiled with Coconut version 3.1.1-post_dev2

# Coconut Header: -------------------------------------------------------------

import sys as _coconut_sys
import os as _coconut_os
_coconut_header_info = ('3.1.1-post_dev2', '3', True)
_coconut_cached__coconut__ = _coconut_sys.modules.get('__coconut__')
_coconut_file_dir = _coconut_os.path.dirname(_coconut_os.path.abspath(__file__))
_coconut_pop_path = False
if _coconut_cached__coconut__ is None or getattr(_coconut_cached__coconut__, "_coconut_header_info", None) != _coconut_header_info and _coconut_os.path.dirname(_coconut_cached__coconut__.__file__ or "") != _coconut_file_dir:  # type: ignore
    if _coconut_cached__coconut__ is not None:
        _coconut_sys.modules['_coconut_cached__coconut__'] = _coconut_cached__coconut__
        del _coconut_sys.modules['__coconut__']
    _coconut_sys.path.insert(0, _coconut_file_dir)
    _coconut_pop_path = True
    _coconut_module_name = _coconut_os.path.splitext(_coconut_os.path.basename(_coconut_file_dir))[0]
    if _coconut_module_name and _coconut_module_name[0].isalpha() and all(c.isalpha() or c.isdigit() for c in _coconut_module_name) and "__init__.py" in _coconut_os.listdir(_coconut_file_dir):  # type: ignore
        _coconut_full_module_name = str(_coconut_module_name + ".__coconut__")  # type: ignore
        import __coconut__ as _coconut__coconut__
        _coconut__coconut__.__name__ = _coconut_full_module_name
        for _coconut_v in vars(_coconut__coconut__).values():  # type: ignore
            if getattr(_coconut_v, "__module__", None) == '__coconut__':  # type: ignore
                try:
                    _coconut_v.__module__ = _coconut_full_module_name
                except AttributeError:
                    _coconut_v_type = type(_coconut_v)  # type: ignore
                    if getattr(_coconut_v_type, "__module__", None) == '__coconut__':  # type: ignore
                        _coconut_v_type.__module__ = _coconut_full_module_name
        _coconut_sys.modules[_coconut_full_module_name] = _coconut__coconut__
from __coconut__ import *
from __coconut__ import _coconut_call_set_names, _namedtuple_of, _coconut, _coconut_Expected, _coconut_MatchError, _coconut_SupportsAdd, _coconut_SupportsMinus, _coconut_SupportsMul, _coconut_SupportsPow, _coconut_SupportsTruediv, _coconut_SupportsFloordiv, _coconut_SupportsMod, _coconut_SupportsAnd, _coconut_SupportsXor, _coconut_SupportsOr, _coconut_SupportsLshift, _coconut_SupportsRshift, _coconut_SupportsMatmul, _coconut_SupportsInv, _coconut_iter_getitem, _coconut_base_compose, _coconut_forward_compose, _coconut_back_compose, _coconut_forward_star_compose, _coconut_back_star_compose, _coconut_forward_dubstar_compose, _coconut_back_dubstar_compose, _coconut_pipe, _coconut_star_pipe, _coconut_dubstar_pipe, _coconut_back_pipe, _coconut_back_star_pipe, _coconut_back_dubstar_pipe, _coconut_none_pipe, _coconut_none_star_pipe, _coconut_none_dubstar_pipe, _coconut_bool_and, _coconut_bool_or, _coconut_none_coalesce, _coconut_minus, _coconut_map, _coconut_partial, _coconut_complex_partial, _coconut_get_function_match_error, _coconut_base_pattern_func, _coconut_addpattern, _coconut_sentinel, _coconut_assert, _coconut_raise, _coconut_mark_as_match, _coconut_reiterable, _coconut_self_match_types, _coconut_dict_merge, _coconut_exec, _coconut_comma_op, _coconut_arr_concat_op, _coconut_mk_anon_namedtuple, _coconut_matmul, _coconut_py_str, _coconut_flatten, _coconut_multiset, _coconut_back_none_pipe, _coconut_back_none_star_pipe, _coconut_back_none_dubstar_pipe, _coconut_forward_none_compose, _coconut_back_none_compose, _coconut_forward_none_star_compose, _coconut_back_none_star_compose, _coconut_forward_none_dubstar_compose, _coconut_back_none_dubstar_compose, _coconut_call_or_coefficient, _coconut_in, _coconut_not_in, _coconut_attritemgetter, _coconut_if_op, _coconut_CoconutWarning
if _coconut_pop_path:
    _coconut_sys.path.pop(0)
try:
    __file__ = _coconut_os.path.abspath(__file__) if __file__ else __file__
except NameError:
    pass
else:
    if __file__ and '__coconut_cache__' in __file__:
        _coconut_file_comps = []
        while __file__:
            __file__, _coconut_file_comp = _coconut_os.path.split(__file__)
            if not _coconut_file_comp:
                _coconut_file_comps.append(__file__)
                break
            if _coconut_file_comp != '__coconut_cache__':
                _coconut_file_comps.append(_coconut_file_comp)
        __file__ = _coconut_os.path.join(*reversed(_coconut_file_comps))

# Compiled Coconut: -----------------------------------------------------------

import os  #1 (line in Coconut source)
import sys  #2 (line in Coconut source)
from warnings import warn  #3 (line in Coconut source)


def fixpath(path):  #6 (line in Coconut source)
    """Uniformly format a path."""  #7 (line in Coconut source)
    return os.path.normpath(os.path.realpath(os.path.expanduser(path)))  #8 (line in Coconut source)



@_coconut_mark_as_match  #11 (line in Coconut source)
def lives_in(_coconut_match_first_arg=_coconut_sentinel, *_coconut_match_args, **_coconut_match_kwargs):  #11 (line in Coconut source)
    """Determine if check_path lives inside of base_dir."""  #12 (line in Coconut source)
    _coconut_match_check_0 = False  #13 (line in Coconut source)
    _coconut_match_set_name_check_path = _coconut_sentinel  #13 (line in Coconut source)
    _coconut_match_set_name_base_dir = _coconut_sentinel  #13 (line in Coconut source)
    _coconut_FunctionMatchError = _coconut_get_function_match_error()  #13 (line in Coconut source)
    if _coconut_match_first_arg is not _coconut_sentinel:  #13 (line in Coconut source)
        _coconut_match_args = (_coconut_match_first_arg,) + _coconut_match_args  #13 (line in Coconut source)
    if _coconut.len(_coconut_match_args) == 2:  #13 (line in Coconut source)
        try:  #13 (line in Coconut source)
            _coconut_match_temp_0 = (fixpath)(_coconut_match_args[0])  #13 (line in Coconut source)
        except _coconut.Exception as _coconut_view_func_exc:  #13 (line in Coconut source)
            if _coconut.getattr(_coconut_view_func_exc.__class__, "__name__", None) == "MatchError":  #13 (line in Coconut source)
                _coconut_match_temp_0 = _coconut_sentinel  #13 (line in Coconut source)
            else:  #13 (line in Coconut source)
                raise  #13 (line in Coconut source)
        try:  #13 (line in Coconut source)
            _coconut_match_temp_1 = (fixpath)(_coconut_match_args[1])  #13 (line in Coconut source)
        except _coconut.Exception as _coconut_view_func_exc:  #13 (line in Coconut source)
            if _coconut.getattr(_coconut_view_func_exc.__class__, "__name__", None) == "MatchError":  #13 (line in Coconut source)
                _coconut_match_temp_1 = _coconut_sentinel  #13 (line in Coconut source)
            else:  #13 (line in Coconut source)
                raise  #13 (line in Coconut source)
        if (_coconut_match_temp_0 is not _coconut_sentinel) and (_coconut_match_temp_1 is not _coconut_sentinel):  #13 (line in Coconut source)
            _coconut_match_set_name_check_path = _coconut_match_temp_0  #13 (line in Coconut source)
            _coconut_match_set_name_base_dir = _coconut_match_temp_1  #13 (line in Coconut source)
            if not _coconut_match_kwargs:  #13 (line in Coconut source)
                _coconut_match_check_0 = True  #13 (line in Coconut source)
    if _coconut_match_check_0:  #13 (line in Coconut source)
        if _coconut_match_set_name_check_path is not _coconut_sentinel:  #13 (line in Coconut source)
            check_path = _coconut_match_set_name_check_path  #13 (line in Coconut source)
        if _coconut_match_set_name_base_dir is not _coconut_sentinel:  #13 (line in Coconut source)
            base_dir = _coconut_match_set_name_base_dir  #13 (line in Coconut source)
    if not _coconut_match_check_0:  #13 (line in Coconut source)
        raise _coconut_FunctionMatchError('def (fixpath -> check_path) `lives_in` (fixpath -> base_dir) =', _coconut_match_args)  #13 (line in Coconut source)

    return os.path.commonpath([base_dir, check_path]) == base_dir  #13 (line in Coconut source)



def in_stdlib(filepath):  #16 (line in Coconut source)
    """Determine if the given filepath is in the Python standard library."""  #17 (line in Coconut source)
    python_dir = os.path.dirname(sys.executable)  #18 (line in Coconut source)
    lib_dir = os.path.join(python_dir, "Lib")  #19 (line in Coconut source)
    site_packages = os.path.join(lib_dir, "site-packages")  #20 (line in Coconut source)
    return (lives_in)(filepath, lib_dir) and not (lives_in)(filepath, site_packages)  #21 (line in Coconut source)



def get_bool_env_var(env_var, default=None):  #24 (line in Coconut source)
    """Get a boolean from an environment variable."""  #25 (line in Coconut source)
    boolstr = os.getenv(env_var, "").lower()  #26 (line in Coconut source)
    if boolstr in ("true", "yes", "on", "1", "t"):  #27 (line in Coconut source)
        return True  #28 (line in Coconut source)
    elif boolstr in ("false", "no", "off", "0", "f"):  #29 (line in Coconut source)
        return False  #30 (line in Coconut source)
    else:  #31 (line in Coconut source)
        if boolstr not in ("", "none", "default"):  #32 (line in Coconut source)
            warn("{_coconut_format_0} has invalid value {_coconut_format_1!r} (defaulting to {_coconut_format_2})".format(_coconut_format_0=(env_var), _coconut_format_1=(os.getenv(env_var)), _coconut_format_2=(default)))  #33 (line in Coconut source)
        return default  #34 (line in Coconut source)



DEFAULT_VERBOSITY = 10  #37 (line in Coconut source)


def get_verbosity():  #40 (line in Coconut source)
    """Get the verbosity level to use in determining how much info to send to Claude."""  #41 (line in Coconut source)
    return (int)(os.getenv("CLAUDE_HERE_VERBOSITY", DEFAULT_VERBOSITY))  #42 (line in Coconut source)
