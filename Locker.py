##
# Copyright (C) 2012 Jasper Snoek, Hugo Larochelle and Ryan P. Adams
# 
# This code is written for research and educational purposes only to 
# supplement the paper entitled
# "Practical Bayesian Optimization of Machine Learning Algorithms"
# by Snoek, Larochelle and Adams
# Advances in Neural Information Processing Systems, 2012
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import sys
import time
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import lockfile


class Locker:

    def __init__(self):
        self.locks = {}

    def __del__(self):
        for filename in self.locks.keys():
            self.locks[filename] = 1
            self.unlock(filename)

    def lock(self, filename):
        if self.locks.has_key(filename):
            self.locks[filename] += 1
            return True
        else:
            lockobj = lockfile.FileLock(filename)
            lockobj.acquire()
            self.locks[filename] = 1
            return True

    def unlock(self, filename):
        if not self.locks.has_key(filename):
            sys.stderr.write("Trying to unlock not-locked file %s.\n" % 
                             (filename))
            return True
        if self.locks[filename] == 1:
            lockobj = lockfile.FileLock(filename)
            success = True
            try:
                lockobj.release()
            except:
                success = False
                sys.stderr.write("Could not unlock file: %s.\n" % (filename))
            del self.locks[filename]
            return success
        else:
            self.locks[filename] -= 1
            return True
            
    def lock_wait(self, filename):
        self.lock(filename)
#        while not self.lock(filename):
#          time.sleep(0.01)
