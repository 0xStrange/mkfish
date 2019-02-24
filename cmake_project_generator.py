#!/usr/bin/env python3

import common
import cxx_compilers


def generate_cmake_cxx_flags_settings(cxx_standard):
    cxx_compiler_ids = cxx_compilers.get_supported_cxx_compiler_ids()
    for i in range(len(cxx_compiler_ids)):
        cxx_compiler_id = cxx_compiler_ids[i]
        cxx_flags = cxx_compilers.build_cxx_compiler_flags(cxx_compiler_id, cxx_standard)
        condition = f'${{CMAKE_CXX_COMPILER_ID}} STREQUAL "{cxx_compiler_id}"'
        if i == 0:
            print(f'if({condition})')
        else:
            print(f'elseif({condition})')

        for cxx_flag in cxx_flags:
            print(f'    list(APPEND CMAKE_CXX_FLAGS "{cxx_flag}")')
        print('\n    list(JOIN CMAKE_CXX_FLAGS " " CMAKE_CXX_FLAGS)')
    common.print_between_eols('''
else()
    message(FATAL_ERROR "Unsupported compiler type: ${{CMAKE_CXX_COMPILER_ID}}")
endif()
''')


def generate_cmakelists_txt(project_name, cxx_standard, libraries):
    common.print_between_eols(f"""
cmake_minimum_required(VERSION 3.12)

project({project_name})

""")
    if 'ncurses' in libraries:
        common.print_between_eols(f"""
find_package (Curses REQUIRED)

""")
    generate_cmake_cxx_flags_settings(cxx_standard)
    common.print_between_eols(f"""

add_executable({project_name} main.cpp)
""")
    if 'ncurses' in libraries:
        common.print_between_eols(f"""
target_link_libraries ({project_name} ${{CURSES_LIBRARIES}})
""")
