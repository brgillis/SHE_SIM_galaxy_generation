#!/usr/bin/env python

""" @file /disk2/brg/Program_Files/workspace/Generate_GalSim_Images/test_convolve_time.py

    Created 1 Mar 2016

    @TODO: File docstring

    ---------------------------------------------------------------------

    Copyright (C) 2016 brg

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import pickle
import sys

from astropy.convolution import convolve_fft
import scipy.signal

from SHE_SIM_galaxy_image_generation import magic_values as mv
from SHE_SIM_galaxy_image_generation.utility import timing
from icebrgpy.convolve import fftw_convolve
import numpy as np
import pyfftw


# Monkey patch in fftn and ifftn from pyfftw.interfaces.scipy_fftpack
scipy.signal.signaltools.fftn = pyfftw.interfaces.scipy_fftpack.fft
scipy.signal.signaltools.ifftn = pyfftw.interfaces.scipy_fftpack.ifftn

size1 = 1000
size2 = 1000
im1_shape = (size1, size1)
im2_shape = (size2, size2)

scale = 0.1

def main(argv):
    """ @TODO main docstring
    """

    # Set up pyfftw
    pyfftw.interfaces.cache.enable()
    try:
        pyfftw.import_wisdom(pickle.load(open(mv.fftw_wisdom_filename, "rb")))
    except IOError as _e:
        print("WARNING: Could not load fftw wisdom. Rerun to get more accurate timings.")

    for _i in range(100):
#         im1 = np.random.rand(size1,size1)
#         im2 = np.random.rand(size2,size2)

        im1 = np.outer(scipy.signal.gaussian(size1, 1),
                       scipy.signal.gaussian(size1, 1),)
        im2 = np.outer(scipy.signal.gaussian(size2, scale * (_i + 1)),
                       scipy.signal.gaussian(size2, scale * (_i + 1)),)

#         _imc1 = scipy.signal.fftconvolve(im1, im2, mode='same')
#
#         _imc2 = convolve_fft(im1, im2, fftn=pyfftw.interfaces.scipy_fftpack.fftn,
#                              ifftn=pyfftw.interfaces.scipy_fftpack.ifftn)

        _imc3 = fftw_convolve(im1, im2)

        pass

    # Save fftw wisdom
    pickle.dump(pyfftw.export_wisdom(), open(mv.fftw_wisdom_filename, "wb"))

if __name__ == "__main__":
    main(sys.argv)
