#!/usr/bin/env python

from osfs import OSFS
import tempfile
from shutil import rmtree

class TempFS(OSFS):

    """Create a Filesystem in a tempory directory (with tempfile.mkdtemp),
    and removes it when the TempFS object is cleaned up."""

    def __init__(self, identifier=None, thread_syncronize=True):
        """Creates a temporary Filesystem

        identifier -- A string that is included in the name of the temporary directory,
        default uses "TempFS"

        """
        self._temp_dir = tempfile.mkdtemp(identifier or "TempFS")
        self._cleaned = False
        OSFS.__init__(self, self._temp_dir, thread_syncronize=thread_syncronize)

    def __str__(self):
        return '<TempFS: %s>' % self._temp_dir

    __repr__ = __str__

    def __unicode__(self):
        return unicode(self.__str__())

    def close(self):
        """Removes the temporary directory.
        This will be called automatically when the object is cleaned up by Python.
        Note that once this method has been called, the FS object may no longer be used."""

        if not self._cleaned:
            self._lock.acquire()
            try:
                rmtree(self._temp_dir)
                self._cleaned = True
            finally:
                self._lock.release()

    def __del__(self):
        self.close()

if __name__ == "__main__":

    tfs = TempFS()
    print tfs