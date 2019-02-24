#!/usr/bin/env python3


def _build_gcc_cxx_compiler_flags(cxx_standard):
    flags = list()
    flags.append('-std=' + cxx_standard)
    flags.append('-Wall')
    flags.append('-Wextra')
    flags.append('-Werror')
    flags.append('-Wfloat-equal')
    flags.append('-Wnon-virtual-dtor')
    return flags


def _build_clang_cxx_compiler_flags(cxx_standard):
    flags = list()
    flags.append('-std=' + cxx_standard)
    flags.append('-Weverything')
    flags.append('-Werror')
    if cxx_standard != 'c++98':
        flags.append('-Wno-c++98-compat')
        flags.append('-Wno-c++98-compat-pedantic')
    return flags


_global_cxx_compilers_ids = {
    'GNU': {
        'flags_builder': _build_gcc_cxx_compiler_flags,
    },
    'Clang': {
        'flags_builder': _build_clang_cxx_compiler_flags,
    }
}


def get_supported_cxx_compiler_ids():
    return list(_global_cxx_compilers_ids.keys())


def build_cxx_compiler_flags(cxx_compiler_id, cxx_standard):
    return _global_cxx_compilers_ids[cxx_compiler_id]['flags_builder'](cxx_standard)
