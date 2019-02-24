#!/usr/bin/env python3

mkfish_settings = {
    'cmake_executable': '/usr/bin/cmake',
    'make_executable': '/usr/bin/make',
    'build_types': {
        'debug': {
            'cmake_build_type': 'Debug'
        },
        'release': {
            'cmake_build_type': 'Release'
        },
    },
    'compilers': {
        'gcc': {
            'compiler_id': 'GNU',
            'c_compiler': '/usr/bin/gcc',
            'cxx_compiler': '/usr/bin/g++',
        },
        'clang': {
            'compiler_id': 'Clang',
            'c_compiler': '/usr/bin/clang',
            'cxx_compiler': '/usr/bin/clang++',
        }
    },
}


def get_cmake_executable():
    return mkfish_settings['cmake_executable']


def get_configured_compilers():
    return mkfish_settings['compilers']
