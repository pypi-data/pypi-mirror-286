#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xb8fc4a04

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
import urllib  #2 (line in Coconut source)
import webbrowser  #3 (line in Coconut source)
import traceback  #4 (line in Coconut source)
from warnings import warn  #5 (line in Coconut source)

from claude_here.debugger import ALL_DEBUG_CONTEXT  #7 (line in Coconut source)
from claude_here.prompter import generate_prompt  #8 (line in Coconut source)


def get_bool_env_var(env_var, default=None):  #11 (line in Coconut source)
    """Get a boolean from an environment variable."""  #12 (line in Coconut source)
    boolstr = os.getenv(env_var, "").lower()  #13 (line in Coconut source)
    if boolstr in ("true", "yes", "on", "1", "t"):  #14 (line in Coconut source)
        return True  #15 (line in Coconut source)
    elif boolstr in ("false", "no", "off", "0", "f"):  #16 (line in Coconut source)
        return False  #17 (line in Coconut source)
    else:  #18 (line in Coconut source)
        if boolstr not in ("", "none", "default"):  #19 (line in Coconut source)
            warn("{_coconut_format_0} has invalid value {_coconut_format_1!r} (defaulting to {_coconut_format_2})".format(_coconut_format_0=(env_var), _coconut_format_1=(os.getenv(env_var)), _coconut_format_2=(default)))  #20 (line in Coconut source)
        return default  #21 (line in Coconut source)



DEFAULT_MAX_CONTEXT_ITEMS = 10  #24 (line in Coconut source)
TEXT_BASED_BROWSERS = {"www-browser", "w3m", "elinks", "lynx"}  #25 (line in Coconut source)


def launch_claude(project_id=None, max_context_items=None, open_browser=None, dry_run=None):  #28 (line in Coconut source)
    """Launch claude.ai with all the collected debug context."""  #29 (line in Coconut source)
    project_id = os.getenv("CLAUDE_HERE_PROJECT_ID", None) if project_id is None else project_id  #30 (line in Coconut source)
    max_context_items = (int)(os.getenv("CLAUDE_HERE_MAX_CONTEXT_ITEMS", DEFAULT_MAX_CONTEXT_ITEMS)) if max_context_items is None else max_context_items  #31 (line in Coconut source)
    open_browser = get_bool_env_var("CLAUDE_HERE_OPEN_BROWSER", webbrowser.get().name not in TEXT_BASED_BROWSERS) if open_browser is None else open_browser  #32 (line in Coconut source)
    dry_run = get_bool_env_var("CLAUDE_HERE_DRY_RUN", False) if dry_run is None else dry_run  #33 (line in Coconut source)

    _coconut_match_to_0 = generate_prompt(ALL_DEBUG_CONTEXT, max_context_items=max_context_items)  #35 (line in Coconut source)
    _coconut_match_check_0 = False  #35 (line in Coconut source)
    _coconut_match_temp_7 = _coconut.getattr(tuple, "_coconut_is_data", False) or _coconut.isinstance(tuple, _coconut.tuple) and _coconut.all(_coconut.getattr(_coconut_x, "_coconut_is_data", False) for _coconut_x in tuple)  # type: ignore  #35 (line in Coconut source)
    _coconut_match_check_0 = True  #35 (line in Coconut source)
    if _coconut_match_check_0:  #35 (line in Coconut source)
        _coconut_match_check_0 = False  #35 (line in Coconut source)
        if not _coconut_match_check_0:  #35 (line in Coconut source)
            _coconut_match_set_name_prompt = _coconut_sentinel  #35 (line in Coconut source)
            _coconut_match_set_name_attachment = _coconut_sentinel  #35 (line in Coconut source)
            if (_coconut_match_temp_7) and (_coconut.isinstance(_coconut_match_to_0, tuple)):  #35 (line in Coconut source)
                _coconut_match_temp_8 = _coconut.getattr(_coconut_match_to_0, 'prompt', _coconut_sentinel)  #35 (line in Coconut source)
                _coconut_match_temp_9 = _coconut.getattr(_coconut_match_to_0, 'attachment', _coconut_sentinel)  #35 (line in Coconut source)
                _coconut_match_temp_10 = _coconut.len(_coconut_match_to_0) <= _coconut.max(0, _coconut.len(_coconut_match_to_0.__match_args__)) and _coconut.all(i in _coconut.getattr(_coconut_match_to_0, "_coconut_data_defaults", {}) and _coconut_match_to_0[i] == _coconut.getattr(_coconut_match_to_0, "_coconut_data_defaults", {})[i] for i in _coconut.range(0, _coconut.len(_coconut_match_to_0.__match_args__)) if _coconut_match_to_0.__match_args__[i] not in ('prompt', 'attachment')) if _coconut.hasattr(_coconut_match_to_0, "__match_args__") else _coconut.len(_coconut_match_to_0) == 0  # type: ignore  #35 (line in Coconut source)
                if (_coconut_match_temp_8 is not _coconut_sentinel) and (_coconut_match_temp_9 is not _coconut_sentinel) and (_coconut_match_temp_10):  #35 (line in Coconut source)
                    _coconut_match_set_name_prompt = _coconut_match_temp_8  #35 (line in Coconut source)
                    _coconut_match_set_name_attachment = _coconut_match_temp_9  #35 (line in Coconut source)
                    _coconut_match_check_0 = True  #35 (line in Coconut source)
            if _coconut_match_check_0:  #35 (line in Coconut source)
                if _coconut_match_set_name_prompt is not _coconut_sentinel:  #35 (line in Coconut source)
                    prompt = _coconut_match_set_name_prompt  #35 (line in Coconut source)
                if _coconut_match_set_name_attachment is not _coconut_sentinel:  #35 (line in Coconut source)
                    attachment = _coconut_match_set_name_attachment  #35 (line in Coconut source)

        if not _coconut_match_check_0:  #35 (line in Coconut source)
            _coconut_match_set_name_prompt = _coconut_sentinel  #35 (line in Coconut source)
            _coconut_match_set_name_attachment = _coconut_sentinel  #35 (line in Coconut source)
            if (not _coconut_match_temp_7) and (_coconut.isinstance(_coconut_match_to_0, tuple)):  #35 (line in Coconut source)
                _coconut_match_temp_12 = _coconut.getattr(_coconut_match_to_0, 'prompt', _coconut_sentinel)  #35 (line in Coconut source)
                _coconut_match_temp_13 = _coconut.getattr(_coconut_match_to_0, 'attachment', _coconut_sentinel)  #35 (line in Coconut source)
                if (_coconut_match_temp_12 is not _coconut_sentinel) and (_coconut_match_temp_13 is not _coconut_sentinel):  #35 (line in Coconut source)
                    _coconut_match_set_name_prompt = _coconut_match_temp_12  #35 (line in Coconut source)
                    _coconut_match_set_name_attachment = _coconut_match_temp_13  #35 (line in Coconut source)
                    _coconut_match_check_0 = True  #35 (line in Coconut source)
            if _coconut_match_check_0:  #35 (line in Coconut source)
                _coconut_match_check_0 = False  #35 (line in Coconut source)
                if not _coconut_match_check_0:  #35 (line in Coconut source)
                    if _coconut.type(_coconut_match_to_0) in _coconut_self_match_types:  #35 (line in Coconut source)
                        _coconut_match_check_0 = True  #35 (line in Coconut source)

                if not _coconut_match_check_0:  #35 (line in Coconut source)
                    if not _coconut.type(_coconut_match_to_0) in _coconut_self_match_types:  #35 (line in Coconut source)
                        _coconut_match_temp_11 = _coconut.getattr(tuple, '__match_args__', ())  # type: _coconut.typing.Any  # type: ignore  #35 (line in Coconut source)
                        if not _coconut.isinstance(_coconut_match_temp_11, _coconut.tuple):  #35 (line in Coconut source)
                            raise _coconut.TypeError("tuple.__match_args__ must be a tuple")  #35 (line in Coconut source)
                        if _coconut.len(_coconut_match_temp_11) < 0:  #35 (line in Coconut source)
                            raise _coconut.TypeError("too many positional args in class match (pattern requires 0; 'tuple' only supports %s)" % (_coconut.len(_coconut_match_temp_11),))  #35 (line in Coconut source)
                        _coconut_match_check_0 = True  #35 (line in Coconut source)


            if _coconut_match_check_0:  #35 (line in Coconut source)
                if _coconut_match_set_name_prompt is not _coconut_sentinel:  #35 (line in Coconut source)
                    prompt = _coconut_match_set_name_prompt  #35 (line in Coconut source)
                if _coconut_match_set_name_attachment is not _coconut_sentinel:  #35 (line in Coconut source)
                    attachment = _coconut_match_set_name_attachment  #35 (line in Coconut source)


    if not _coconut_match_check_0:  #35 (line in Coconut source)
        raise _coconut_MatchError('tuple(prompt=prompt, attachment=attachment) = generate_prompt(ALL_DEBUG_CONTEXT, max_context_items=)', _coconut_match_to_0)  #35 (line in Coconut source)

    if dry_run:  #36 (line in Coconut source)
        print(prompt)  #37 (line in Coconut source)
        if attachment:  #38 (line in Coconut source)
            print(attachment)  #39 (line in Coconut source)
    else:  #40 (line in Coconut source)
        url = ("https://claude.ai/new?q={_coconut_format_0}".format(_coconut_format_0=(urllib.parse.quote_plus(prompt))) + ("&attachment={_coconut_format_0}".format(_coconut_format_0=(urllib.parse.quote_plus(attachment))) if attachment else "") + ("&project={_coconut_format_0}".format(_coconut_format_0=(urllib.parse.quote_plus(project_id))) if project_id else ""))  #41 (line in Coconut source)
        if open_browser:  #46 (line in Coconut source)
            try:  #47 (line in Coconut source)
                webbrowser.open(url)  #48 (line in Coconut source)
            except ValueError:  #49 (line in Coconut source)
                traceback.print_exc()  #50 (line in Coconut source)
                open_browser = False  #51 (line in Coconut source)
        if not open_browser:  #52 (line in Coconut source)
            print("\e]8;;{_coconut_format_0}\e\\Cmd+click here to open Claude!\e]8;;\e\\\n".format(_coconut_format_0=(url)))  #53 (line in Coconut source)
