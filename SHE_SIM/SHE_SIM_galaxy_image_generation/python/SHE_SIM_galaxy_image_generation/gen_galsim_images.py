#!/usr/bin/env python

"""gen_galsim_images.py
   Created by Bryan Gillis, March 2014
   Last edited by brg, 11 Aug 2015

   Contact: brg@roe.ac.uk

   Requirements: GalSim toolkit (and its requirements).
   GalSim can be downloaded from https://github.com/GalSim-developers/GalSim, and see
   https://github.com/GalSim-developers/GalSim/wiki/Installation-Instructions for its
   installation requirements.

   This is a script to generate a set of seeded random images using the GalSim toolkit,
   suitable for Euclid benchmarking tests of shear-measurement algorithms.
   This script should be invoked with a command that points it to an appropriate
   configuration script, for instance through:

   $ python gen_galsim_images.py my_config.cfg

   See the sample configuration files included with this script for the proper format.
   It is recommended that you start with an appropriate configuration script and modify
   it to suit your purposes.

   If a configuration file is not passed to this script, it will use the set of default
   configuration values assigned in the load_default_configurations(...) function below.

   NOTE 1: If you got this script or the configuration file from someone else, check the
   output directory and change it if necessary. It can use absolute paths, and the
   folders will be created if necessary, which may result in creating a file structure
   you don't want.

   NOTE 2: If you see odd bugs in running this, it's possibly due to a parallelization bug.
   This script assumes that all of the process it calls are not parallelized, and if they
   are, it can lead to clashes between threads. You can try fixing this by setting the
   following environmental variables before run (which one is actually needed depends on
   the specifics of your installation):
       export MKL_NUM_THREADS=1
       export NUMEXPR_NUM_THREADS=1
       export OPENBLAS_NUM_THREADS=1
    If this doesn't work, please let me know at brg@roe.ac.uk, and I'll try to figure out
    what's going on.
"""

from galsim_images_generation.run_from_config import run_from_config_file
from utility import timing


def main(argv):

    # Check that a configuration file name was passed at command line
    if(len(argv)) <= 1:
        config_file_name = ""
    else:
        config_file_name = argv[1]

    run_from_config_file(config_file_name)

    print 'Execution complete.'


if __name__ == "__main__":
    main(sys.argv)
