#!/usr/bin/env python

## Printing troubleshooter

## Copyright (C) 2008 Red Hat, Inc.
## Copyright (C) 2008 Tim Waugh <twaugh@redhat.com>

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
## Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

from base import *
from base import _
class ErrorLogParse(Question):
    def __init__ (self, troubleshooter):
        Question.__init__ (self, troubleshooter, "Error log parse")
        page = self.initial_vbox (_("Error log messages"),
                                  _("There are messages in the error log."))
        sw = gtk.ScrolledWindow ()
        textview = gtk.TextView ()
        textview.set_editable (False)
        sw.add (textview)
        page.pack_start (sw)
        self.buffer = textview.get_buffer ()
        troubleshooter.new_page (page, self)

    def display (self):
        answers = self.troubleshooter.answers
        try:
            error_log = answers['error_log']
        except KeyError:
            return False

        display = False
        for line in error_log:
            if (line.find ("error") != -1 and
                line.find ("no errors") == -1 and
                line.find ("error_log") == -1):
                display = True

        if display:
            self.buffer.set_text (reduce (lambda x, y: x + '\n' + y, 
                                          error_log))

        return display