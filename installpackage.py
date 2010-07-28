#!/usr/bin/python

## system-config-printer

## Copyright (C) 2008, 2009 Red Hat, Inc.
## Copyright (C) 2008, 2009 Tim Waugh <twaugh@redhat.com>

## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import os
import glib

GPK_INSTALL_PACKAGE_NAME='/usr/share/system-config-printer/gpk-install-package-name'

class PackageKit:
    def __init__ (self):
        self.gpk_install_package_name = GPK_INSTALL_PACKAGE_NAME

    def InstallPackageName (self, xid, timestamp, name):
        glib.spawn_async ([self.gpk_install_package_name, name])
