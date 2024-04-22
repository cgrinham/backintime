#    Back In Time
#    Copyright (C) 2008-2022 Oprea Dan, Bart de Koning, Richard Bailey, Germar Reitze
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


import os

import logger
from applicationinstance import ApplicationInstance


class GUIApplicationInstance(ApplicationInstance):
    """
    class used to handle one application instance mechanism
    """
    def __init__(self, baseControlFile, raiseCmd=''):
        """
        specify the base for control files
        """
        self.raiseFile = baseControlFile + '.raise'
        self.raiseCmd = raiseCmd

        super(GUIApplicationInstance, self).__init__(f"{baseControlFile}.pid", False, False)

        # remove raiseFile is already exists
        if os.path.exists(self.raiseFile):
            os.remove(self.raiseFile)

        self.check_is_single_instance(autoExit=raiseCmd)
        self.startApplication()

    def check(self, raiseCmd):
        """
        check if the current application is already running
        """
        is_single_instance = super(GUIApplicationInstance, self).check_is_single_instance(autoExit=False)
        if is_single_instance:
            return is_single_instance

        print(f"The application is already running! (pid: {self.pid})")  # CG: why aren't we using logger here?
        # notify raise
        try:
            with open(self.raiseFile, 'wt') as f:
                f.write(raiseCmd)
        except OSError as e:
            logger.error(f'Failed to write raise file {e.filename}: [{e.errno}] {e.strerror}')

        exit(0)  # exit raise an exception so don't put it in a try/except block

    def raiseCommand(self):
        """
        check if the application must to be raised
           return None if no raise needed, or a string command to raise
        """
        ret_val = None

        try:
            if os.path.isfile(self.raiseFile):
                with open(self.raiseFile, 'rt') as f:
                    ret_val = f.read()
                os.remove(self.raiseFile)
        except:
            pass

        return ret_val
