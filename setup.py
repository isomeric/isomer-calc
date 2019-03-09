#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Isomer - The distributed application framework
# ==============================================
# Copyright (C) 2011-2019 Heiko 'riot' Weinen <riot@c-base.org> and others.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from isomer.tool.templates import insert_nginx_service

__author__ = "Heiko 'riot' Weinen"
__license__ = "AGPLv3"

from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop


def insert_service():
    definition = """# EtherCalc Module
    location /ethercalc/ {
        proxy_pass      http://127.0.0.1:8056/;
        include         proxy_params;
    }
    
    location /zappa/socket/__local/ {
        rewrite (.*) /ethercalc/$1;
    }
"""

    insert_nginx_service(definition)


class PostInstall(install):
    def run(self):
        install.run(self)
        insert_service()


class PostDevelop(develop):
    def run(self):
        develop.run(self)
        insert_service()


setup(
    name="isomer-calc",
    version="0.0.1",
    description="isomer-calc",
    author="Isomer Community",
    author_email="riot@c-base.org",
    url="https://github.com/isomeric/isomer-calc",
    license="GNU Affero General Public License v3",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Isomer :: 1',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Office/Business :: Financial :: Spreadsheet'
    ],
    packages=find_packages(),
    include_package_data=True,
    long_description="""Isomer - Calc
=============

Seamlessly integrate EtherCalc into Isomer.

This software package is a plugin module for Isomer.
""",
    dependency_links=[
    ],
    install_requires=[
        'isomer>=1.0',
    ],
    cmdclass={
        'develop': PostDevelop,
        'install': PostInstall
    },
    entry_points="""[isomer.components]
    spreadsheetwatcher=isomer.calc.spreadsheetwatcher:SpreadsheetWatcher
    [isomer.schemata]
    spreadsheet=isomer.calc.schemata.spreadsheet:Spreadsheet
    """,
    test_suite="tests.main.main",
)
