#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xa3f34c0

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
import io  #2 (line in Coconut source)
import inspect  #3 (line in Coconut source)
import traceback  #4 (line in Coconut source)
import builtins  #5 (line in Coconut source)
from dis import dis  #6 (line in Coconut source)
from collections import defaultdict  #7 (line in Coconut source)


ALL_DEBUG_CONTEXT = defaultdict(list)  #10 (line in Coconut source)


reset = ALL_DEBUG_CONTEXT.clear  #13 (line in Coconut source)


def fixpath(path):  #16 (line in Coconut source)
    """Uniformly format a path."""  #17 (line in Coconut source)
    return os.path.normpath(os.path.realpath(os.path.expanduser(path)))  #18 (line in Coconut source)



def include_file(filepath):  #21 (line in Coconut source)
    """Ensure that the given filepath is included in the context sent to Claude."""  #22 (line in Coconut source)
    ALL_DEBUG_CONTEXT[fixpath(filepath)]  #23 (line in Coconut source)



class DebugContext(_coconut.typing.NamedTuple("DebugContext", [("name", 'str'), ("frame_info", '_coconut.typing.Any'), ("source_type", '_coconut.typing.Optional[str]'), ("raw_source", 'str'), ("extra_info", 'dict[str, str]')])):  #26 (line in Coconut source)
    """Collection of information gathered about a debug event."""  #33 (line in Coconut source)
    __slots__ = ()  #34 (line in Coconut source)
    _coconut_is_data = True  #34 (line in Coconut source)
    __match_args__ = ('name', 'frame_info', 'source_type', 'raw_source', 'extra_info')  #34 (line in Coconut source)
    def __add__(self, other): return _coconut.NotImplemented  #34 (line in Coconut source)
    def __mul__(self, other): return _coconut.NotImplemented  #34 (line in Coconut source)
    def __rmul__(self, other): return _coconut.NotImplemented  #34 (line in Coconut source)
    __ne__ = _coconut.object.__ne__  #34 (line in Coconut source)
    def __eq__(self, other):  #34 (line in Coconut source)
        return self.__class__ is other.__class__ and _coconut.tuple.__eq__(self, other)  #34 (line in Coconut source)
    def __hash__(self):  #34 (line in Coconut source)
        return _coconut.tuple.__hash__(self) ^ _coconut.hash(self.__class__)  #34 (line in Coconut source)
    def __init__(self, *args, **kwargs):  #34 (line in Coconut source)
        ALL_DEBUG_CONTEXT[self.filename].append(self)  #35 (line in Coconut source)

    @property  #36 (line in Coconut source)
    def filename(self):  #37 (line in Coconut source)
        return fixpath(self.frame_info.filename)  #37 (line in Coconut source)

    @property  #38 (line in Coconut source)
    def lineno(self):  #39 (line in Coconut source)
        return self.frame_info.lineno  #39 (line in Coconut source)

    @property  #40 (line in Coconut source)
    def function(self):  #41 (line in Coconut source)
        return self.frame_info.function  #41 (line in Coconut source)

    @property  #42 (line in Coconut source)
    def context_lines(self):  #43 (line in Coconut source)
        return self.frame_info.code_context  #43 (line in Coconut source)

    @property  #44 (line in Coconut source)
    def context_index(self):  #45 (line in Coconut source)
        return self.frame_info.index  #45 (line in Coconut source)

    @property  #46 (line in Coconut source)
    def raw_context(self):  #47 (line in Coconut source)
        return "".join(self.context_lines) if self.context_lines else ""  #47 (line in Coconut source)



_coconut_call_set_names(DebugContext)  #50 (line in Coconut source)
IGNORED_VARS = set(dir(builtins)) | {"claude_here"}  #50 (line in Coconut source)


def format_vars(vardict):  #53 (line in Coconut source)
    return (repr)(_coconut.dict(((name), (val)) for name, val in vardict.items() if not name.startswith("__") and name not in IGNORED_VARS))  #53 (line in Coconut source)



def get_source(frame):  #59 (line in Coconut source)
    """Extract the source code from frame."""  #60 (line in Coconut source)
    try:  #61 (line in Coconut source)
        source_lines, source_lineno = inspect.getsourcelines(frame)  #62 (line in Coconut source)
    except OSError:  #63 (line in Coconut source)
        fake_file = io.StringIO()  #64 (line in Coconut source)
        dis(frame.f_code, file=fake_file)  #65 (line in Coconut source)
        fake_file.seek(0)  #66 (line in Coconut source)
        return (_coconut_mk_anon_namedtuple(('source_type', 'raw_source'))("dis", fake_file.read()))  #67 (line in Coconut source)
    else:  #68 (line in Coconut source)
        return (_coconut_mk_anon_namedtuple(('source_type', 'raw_source'))(None, "".join(source_lines)))  #69 (line in Coconut source)



def collect_stack_info(stack_level=1):  #72 (line in Coconut source)
    """Collect information about the callee site for sending to Claude."""  #73 (line in Coconut source)
    cur_frame = inspect.currentframe()  #74 (line in Coconut source)
    outer_frame = reduce(lambda frame, _: frame.f_back, range(stack_level), cur_frame)  #75 (line in Coconut source)

    frame_info = inspect.getframeinfo(outer_frame)  #81 (line in Coconut source)
    source_type, raw_source = get_source(outer_frame)  #82 (line in Coconut source)

    return DebugContext(name="breakpoint", frame_info=frame_info, source_type=source_type, raw_source=raw_source, extra_info=_coconut.dict((("locals", format_vars(outer_frame.f_locals)), ("globals", format_vars(outer_frame.f_globals)))))  #84 (line in Coconut source)



def filter_traceback(orig_tb):  #96 (line in Coconut source)
    """Filter out traceback frames from claude_here."""  #97 (line in Coconut source)
    new_tb_top = orig_tb  #98 (line in Coconut source)
    while new_tb_top is not None and new_tb_top.tb_frame.f_globals.get("__package__") == "claude_here":  #99 (line in Coconut source)
        new_tb_top = new_tb_top.tb_next  #100 (line in Coconut source)

    if new_tb_top is not None:  #102 (line in Coconut source)
        tb_cursor_plus_1 = new_tb_top  #103 (line in Coconut source)
        tb_cursor = tb_cursor_plus_1.tb_next  #104 (line in Coconut source)
        while tb_cursor is not None:  #105 (line in Coconut source)
            tb_cursor_minus_1 = tb_cursor.tb_next  #106 (line in Coconut source)
            if tb_cursor.tb_frame.f_globals.get("__package__") == "claude_here":  #107 (line in Coconut source)
                tb_cursor_plus_1.tb_next = tb_cursor_minus_1  #108 (line in Coconut source)
                tb_cursor_plus_1, tb_cursor = (tb_cursor_plus_1, tb_cursor_minus_1)  #109 (line in Coconut source)
            else:  #113 (line in Coconut source)
                tb_cursor_plus_1, tb_cursor = (tb_cursor, tb_cursor_minus_1)  #114 (line in Coconut source)

    return new_tb_top  #119 (line in Coconut source)



def collect_exc_info(exc_type, exc_val, exc_tb):  #122 (line in Coconut source)
    """Collect information about the given exception for sending to Claude."""  #123 (line in Coconut source)
    filtered_tb = filter_traceback(exc_tb)  #124 (line in Coconut source)

    frame_info = inspect.getframeinfo(filtered_tb.tb_frame)  #126 (line in Coconut source)
    source_type, raw_source = get_source(filtered_tb)  #127 (line in Coconut source)
    pretty_tb = (("".join)(traceback.format_exception(exc_type, exc_val, filtered_tb)))  #128 (line in Coconut source)

    return DebugContext(name="exception", frame_info=frame_info, source_type=source_type, raw_source=raw_source, extra_info=_coconut.dict((("traceback", pretty_tb),)))  #133 (line in Coconut source)
