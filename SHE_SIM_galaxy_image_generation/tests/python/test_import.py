"""
    Tests of various imports, to make sure galsim is installed and other parts of the project are
    linked correctly.
"""

import unittest


class TestCase(unittest.TestCase):

    # External imports

    def testGalSimImport(self):
        import galsim
        
    # Internal python imports

    def testicebrgpyImport(self):
        import icebrgpy
        
    # Internal C++ imports

    def testcIceBRGpyImport(self):
        import cIceBRGpy

    def testSHESIMImport(self):
        import SHE_SIM
