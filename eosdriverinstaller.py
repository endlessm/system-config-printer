#!/usr/bin/python3
#
# eosdriverinstaller
#
# Copyright (C) 2015 Endless Mobile, Inc.
# Authors:
#  Mario Sanchez Prada <mario@endlessm.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import dbus

from debug import *
from gi.repository import GLib
from threading import Thread
import queue

EOS_CONFIG_PRINTING_BUS = 'com.endlessm.Config.Printing'
EOS_CONFIG_PRINTING_PATH = '/com/endlessm/Config/Printing'
EOS_CONFIG_PRINTING_IFACE = 'com.endlessm.Config.Printing'

class DriverInstallerThread(Thread):
    def __init__ (self, type_, uri, fingerprint, queue):
        Thread.__init__(self, daemon=True)
        self._type = type_
        self._uri = uri
        self._fingerprint = fingerprint
        self._queue = queue
        debugprint ("+%s" % self)

    def run (self):
        try:
            bus = dbus.SystemBus()
            obj = bus.get_object(EOS_CONFIG_PRINTING_BUS, EOS_CONFIG_PRINTING_PATH)
            iface = dbus.Interface(obj, EOS_CONFIG_PRINTING_IFACE)

            args = { 'uri': self._uri }
            if self._fingerprint is not None:
                args['fingerprint'] = self._fingerprint

            result = iface.InstallDriver(self._type, args, timeout=GLib.MAXINT32/1000)

            # InstallDriver returns a list of installed files as DBus strings
            installed_files = [str(dbus_string) for dbus_string in result]
            self._queue.put(('installed_files', installed_files))

        except dbus.exceptions.DBusException as e:
            debugprint('Unable to execute remote method: %s' % repr(e.get_dbus_message()))
            self._queue.put(('error', e.get_dbus_message()))

        # Wait for the caller to confirm it has consumed the result
        self._queue.join()


if __name__ == "__main__":
    import time
    import sys

    # The whole point of the code below is for debugging.
    set_debugging(True)

    # Get command line parameters
    if len(sys.argv) < 4:
        debugprint('Not enough parameters. Usage: eosdriverinstaller <type> <uri> <fingerprint>')
        sys.exit(1)

    type_ = int(sys.argv[1])
    uri = sys.argv[2]
    fingerprint = sys.argv[3]

    p_queue = queue.Queue()
    p = DriverInstallerThread (type_, uri, fingerprint, p_queue)
    p.start()

    debugprint("Installing driver from %s..." % uri)
    while True:
        # Exit the loop if the thread died for any reason
        if not p.is_alive():
            debugprint("Thread died unexpectedly")
            break

        try:
            (reply_type, result) = p_queue.get(timeout=0.1)
            if reply_type == 'error':
                debugprint("Error installing a driver: %s" % repr(result))
                sys.exit(1)
            elif reply_type == 'installed_files':
                installed_driver_files = result
                debugprint('Driver successfully installed. Installed files: %s'
                           % installed_driver_files)
            else:
                # This should not ever happen
                debugprint("Unknown response received from child thread")
                sys.exit(1)

            # Tell the thread we are done with the data
            p_queue.task_done()
            break

        except queue.Empty:
            time.sleep (0.1)

    debugprint('Finished')
    sys.exit(0)
