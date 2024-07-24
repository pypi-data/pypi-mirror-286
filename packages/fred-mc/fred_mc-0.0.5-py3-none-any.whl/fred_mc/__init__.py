import os
import ctypes
from ctypes import c_int,c_float,c_void_p,c_char_p,c_ulonglong, POINTER

# python wrapper class to C library
class libFRED:
    def __init__(self):
        libPath = os.path.join(os.path.dirname(__file__),'libFred.so')
        # print(libPath)
        self._lib = ctypes.cdll.LoadLibrary(libPath)
        # self._lib.fredInit()
        # self.beams = Beams(self._lib)
        # self.physmod = PhysModels(self._lib)
        # self.phantom = Region(self._lib,1)
        # self._refreshedOutdir = False

    @property
    def version(self):
        s = b'\0'*256
        self._lib.fred_Version(c_char_p(s))
        vers = s.decode("utf-8").split("\x00")[0]
        # print(vers,len(vers))
        try:
            major,minor,patch = map(int,vers.split()[2].split('.'))
            return major,minor,patch
        except:
            return (-1,-1,-1)

    @property
    def changeset(self):
        s = b'\0'*256
        self._lib.fred_Version(c_char_p(s))
        vers = s.decode("utf-8").split("\x00")[0]
        return (vers.split()[3])[1:-1]
    
    @property
    def buildDate(self):
        s = b'\0'*256
        self._lib.fred_Version(c_char_p(s))
        vers = s.decode("utf-8").split("\x00")[0]
        return vers.split()[-1]

