#!/usr/bin/env python3

import argparse
import os
import common
import shutil
import cmake_project_generator
import subprocess
import mkfish_settings


def generate_console_main_cpp():
    common.print_between_eols("""
#include <stdio.h>

int main ()
{
    printf ("Hello, World!\\n");
    return 0;
}
""")


def generate_ncurses_main_cpp():
    common.print_between_eols("""
#include <curses.h>
#include <string.h>

int main ()
{
    initscr ();
    raw ();
    keypad (stdscr, 1);
    noecho ();
    curs_set (0);
    set_escdelay (0);

    int nrows, ncols;
    getmaxyx (stdscr, nrows, ncols);
    
    const char message[] = "Hello, World!";
    int length = static_cast<int> (strlen (message));
    
    move (nrows / 2, (ncols - length) / 2);
    addstr (message);
    
    getch();
    endwin();
    
    return 0;
}
""")


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-n', '--project_name', default='fish', help='Name of the project')
    parser.add_argument('-p', '--prefix', required=True, help='Directory where the project will be created')
    parser.add_argument('--std', default='c++14', help='C++ language standard version')
    parser.add_argument('-f', '--force', action='store_true')
    parser.add_argument('--type', choices=['console', 'ncurses'], default='console')

    return parser.parse_args()


def main():
    args = parse_args()
    if not os.path.isdir(args.prefix):
        common.print_error('Error: path "%s" is not a directory.' % args.prefix)
        exit(-1)

    outer_project_directory = os.path.join(args.prefix, args.project_name)
    inner_project_directory = os.path.join(outer_project_directory, args.project_name)
    try:
        if os.path.exists(outer_project_directory):
            if not args.force:
                common.print_error('Error: path "%s" already exists. Use --force to remove it.' %
                                   outer_project_directory)
                exit(-1)
            shutil.rmtree(outer_project_directory)

        os.mkdir(outer_project_directory)
        os.mkdir(inner_project_directory)
    except Exception as e:
        common.print_error(str(e))
        exit(-1)

    libraries = list()

    if args.type == 'console':
        common.generate_file(os.path.join(inner_project_directory, 'main.cpp'), generate_console_main_cpp)
    elif args.type == 'ncurses':
        common.generate_file(os.path.join(inner_project_directory, 'main.cpp'), generate_ncurses_main_cpp)
        libraries.append('ncurses')
    common.generate_file(os.path.join(inner_project_directory, 'CMakeLists.txt'),
                         cmake_project_generator.generate_cmakelists_txt, args.project_name, args.std, libraries)

    configured_compilers = mkfish_settings.mkfish_settings['compilers']
    configured_build_types = mkfish_settings.mkfish_settings['build_types']
    for compiler in configured_compilers:
        compiler_spec = configured_compilers[compiler]
        for build_type in configured_build_types:
            build_type_spec = configured_build_types[build_type]
            build_directory_name = compiler + '.' + build_type
            build_directory = os.path.join(outer_project_directory, build_directory_name)

            os.mkdir(build_directory)

            cmake_args = list()
            cmake_args.append(mkfish_settings.mkfish_settings['cmake_executable'])
            cmake_args.append('-DCMAKE_BUILD_TYPE='+ build_type_spec['cmake_build_type'])
            cmake_args.append('-DCMAKE_C_COMPILER=' + compiler_spec['c_compiler'])
            cmake_args.append('-DCMAKE_CXX_COMPILER=' + compiler_spec['cxx_compiler'])
            cmake_args.append('../' + args.project_name)

            subprocess.Popen(cmake_args, cwd=build_directory).wait()


if __name__ == '__main__':
    main()
