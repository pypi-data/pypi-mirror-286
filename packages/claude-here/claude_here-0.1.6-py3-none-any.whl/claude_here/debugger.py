#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xae7221d0

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
import inspect  #2 (line in Coconut source)
import traceback  #3 (line in Coconut source)
import builtins  #4 (line in Coconut source)
from collections import defaultdict  #5 (line in Coconut source)


ALL_DEBUG_CONTEXT = defaultdict(list)  #8 (line in Coconut source)


reset = ALL_DEBUG_CONTEXT.clear  #11 (line in Coconut source)


def fixpath(path):  #14 (line in Coconut source)
    """Uniformly format a path."""  #15 (line in Coconut source)
    return os.path.normpath(os.path.realpath(os.path.expanduser(path)))  #16 (line in Coconut source)



def include_file(filepath):  #19 (line in Coconut source)
    """Ensure that the given filepath is included in the context sent to Claude."""  #20 (line in Coconut source)
    ALL_DEBUG_CONTEXT[fixpath(filepath)]  #21 (line in Coconut source)



class DebugContext(_coconut.typing.NamedTuple("DebugContext", [("name", 'str'), ("frame_info", '_coconut.typing.Any'), ("source_lines", '_coconut.typing.Sequence[str]'), ("extra_info", 'dict[str, str]')])):  #24 (line in Coconut source)
    """Collection of information gathered about a debug event."""  #30 (line in Coconut source)
    __slots__ = ()  #31 (line in Coconut source)
    _coconut_is_data = True  #31 (line in Coconut source)
    __match_args__ = ('name', 'frame_info', 'source_lines', 'extra_info')  #31 (line in Coconut source)
    def __add__(self, other): return _coconut.NotImplemented  #31 (line in Coconut source)
    def __mul__(self, other): return _coconut.NotImplemented  #31 (line in Coconut source)
    def __rmul__(self, other): return _coconut.NotImplemented  #31 (line in Coconut source)
    __ne__ = _coconut.object.__ne__  #31 (line in Coconut source)
    def __eq__(self, other):  #31 (line in Coconut source)
        return self.__class__ is other.__class__ and _coconut.tuple.__eq__(self, other)  #31 (line in Coconut source)
    def __hash__(self):  #31 (line in Coconut source)
        return _coconut.tuple.__hash__(self) ^ _coconut.hash(self.__class__)  #31 (line in Coconut source)
    def __init__(self, *args, **kwargs):  #31 (line in Coconut source)
        ALL_DEBUG_CONTEXT[self.filename].append(self)  #32 (line in Coconut source)

    @property  #33 (line in Coconut source)
    def filename(self):  #34 (line in Coconut source)
        return fixpath(self.frame_info.filename)  #34 (line in Coconut source)

    @property  #35 (line in Coconut source)
    def lineno(self):  #36 (line in Coconut source)
        return self.frame_info.lineno  #36 (line in Coconut source)

    @property  #37 (line in Coconut source)
    def function(self):  #38 (line in Coconut source)
        return self.frame_info.function  #38 (line in Coconut source)

    @property  #39 (line in Coconut source)
    def context_lines(self):  #40 (line in Coconut source)
        return self.frame_info.code_context  #40 (line in Coconut source)

    @property  #41 (line in Coconut source)
    def context_index(self):  #42 (line in Coconut source)
        return self.frame_info.index  #42 (line in Coconut source)

    @property  #43 (line in Coconut source)
    def raw_context(self):  #44 (line in Coconut source)
        return "".join(self.context_lines) if self.context_lines else ""  #44 (line in Coconut source)

    @property  #45 (line in Coconut source)
    def raw_source(self):  #46 (line in Coconut source)
        return "".join(self.source_lines)  #46 (line in Coconut source)



_coconut_call_set_names(DebugContext)  #49 (line in Coconut source)
IGNORED_VARS = set(dir(builtins)) | {"claude_here"}  #49 (line in Coconut source)


def format_vars(vardict):  #52 (line in Coconut source)
    return (repr)(_coconut.dict(((name), (val)) for name, val in vardict.items() if not name.startswith("__") and name not in IGNORED_VARS))  #52 (line in Coconut source)



def get_source_lines(frame):  #58 (line in Coconut source)
    """Extract the source code lines from frame."""  #59 (line in Coconut source)
    try:  #60 (line in Coconut source)
        source_lines, source_lineno = inspect.getsourcelines(frame)  #61 (line in Coconut source)
    except OSError:  #62 (line in Coconut source)
        source_lines = []  #63 (line in Coconut source)
    return source_lines  #64 (line in Coconut source)



def collect_stack_info(stack_level=1):  #67 (line in Coconut source)
    """Collect information about the callee site for sending to Claude."""  #68 (line in Coconut source)
    cur_frame = inspect.currentframe()  #69 (line in Coconut source)
    outer_frame = reduce(lambda frame, _: frame.f_back, range(stack_level), cur_frame)  #70 (line in Coconut source)

    frame_info = inspect.getframeinfo(outer_frame)  #76 (line in Coconut source)
    source_lines = get_source_lines(outer_frame)  #77 (line in Coconut source)

    return DebugContext(name="breakpoint", frame_info=frame_info, source_lines=source_lines, extra_info=_coconut.dict((("locals", format_vars(outer_frame.f_locals)), ("globals", format_vars(outer_frame.f_globals)))))  #79 (line in Coconut source)



def filter_traceback(orig_tb):  #90 (line in Coconut source)
    """Filter out traceback frames from claude_here."""  #91 (line in Coconut source)
    new_tb_top = orig_tb  #92 (line in Coconut source)
    while new_tb_top is not None and new_tb_top.tb_frame.f_globals.get("__package__") == "claude_here":  #93 (line in Coconut source)
        new_tb_top = new_tb_top.tb_next  #94 (line in Coconut source)

    if new_tb_top is not None:  #96 (line in Coconut source)
        tb_cursor_plus_1 = new_tb_top  #97 (line in Coconut source)
        tb_cursor = tb_cursor_plus_1.tb_next  #98 (line in Coconut source)
        while tb_cursor is not None:  #99 (line in Coconut source)
            tb_cursor_minus_1 = tb_cursor.tb_next  #100 (line in Coconut source)
            if tb_cursor.tb_frame.f_globals.get("__package__") == "claude_here":  #101 (line in Coconut source)
                tb_cursor_plus_1.tb_next = tb_cursor_minus_1  #102 (line in Coconut source)
                tb_cursor_plus_1, tb_cursor = (tb_cursor_plus_1, tb_cursor_minus_1)  #103 (line in Coconut source)
            else:  #107 (line in Coconut source)
                tb_cursor_plus_1, tb_cursor = (tb_cursor, tb_cursor_minus_1)  #108 (line in Coconut source)

    return new_tb_top  #113 (line in Coconut source)



def collect_exc_info(exc_type, exc_val, exc_tb):  #116 (line in Coconut source)
    """Collect information about the given exception for sending to Claude."""  #117 (line in Coconut source)
    filtered_tb = filter_traceback(exc_tb)  #118 (line in Coconut source)

    frame_info = inspect.getframeinfo(filtered_tb.tb_frame)  #120 (line in Coconut source)
    source_lines = get_source_lines(filtered_tb)  #121 (line in Coconut source)
    pretty_tb = (("".join)(traceback.format_exception(exc_type, exc_val, filtered_tb)))  #122 (line in Coconut source)

    return DebugContext(name="exception", frame_info=frame_info, source_lines=source_lines, extra_info=_coconut.dict((("traceback", pretty_tb),)))  #127 (line in Coconut source)
