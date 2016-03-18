""" @file generate_images.py

    Created 23 Jul 2015

    This module contains the function "generate_images" which does the
    heavy lifting of actually using GalSim to generate images.

    ---------------------------------------------------------------------

    Copyright (C) 2015 Bryan R. Gillis

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

from __future__ import division

import multiprocessing as mtp
from os.path import join
import numpy as np

import pyfftw
import galsim

from icebrgpy.rebin import rebin
from icebrgpy.convolve import fftw_convolve

from astropy.table import Table
from galsim_images_generation.combine_dithers import combine_dithers
from galsim_images_generation.compress_image import compress_image
from galsim_images_generation.cutouts import make_cutout_image
from galsim_images_generation.dither_schemes import get_dither_scheme
from galsim_images_generation.galaxy import (get_bulge_galaxy_profile, 
                                             get_disk_galaxy_image,
                                             is_target_galaxy)
from galsim_images_generation.magnitude_conversions import get_I
from galsim_images_generation.psf import get_psf_profile
from galsim_images_generation import output_table
from galsim_images_generation import magic_values as mv
from parmap import parmap

def generate_images( survey, options ):
    """ This function handles assigning specific images to be created by different parallel
        threads.
        
        @param survey <SHE_SIM.Survey>
        @param options <dict>
        
        Side-effects: If successful, generates images and corresponding details according to
                      the configuration stored in the survey and options objects.
    """
    
    # Seed the survey
    survey.set_seed(options['seed'])
    
    # Create empty image objects for the survey
    survey.fill_images()
    images = survey.get_images()
    
    # If we just have one thread, we'll just use a simply function call to ease debugging
    if options['num_parallel_threads']==1:
        for image in images:
            generate_image(image,options)
    else:
        if(options['num_parallel_threads'] <= 0):
            options['num_parallel_threads'] += mtp.cpu_count()
        
        # Split up using parmap
        def generate_image_with_options(image_index):
            generate_image(images[image_index],options)
            return
            
        parmap( generate_image_with_options, range(len(images)), nprocs=options['num_parallel_threads'] )
        
    return

def print_galaxies(image,
                 options,
                 centre_offset,
                 num_dithers,
                 dithers,
                 full_x_size,
                 full_y_size,
                 pixel_scale,
                 otable):
    
    galaxies = image.get_galaxy_descendants()
    
    background_galaxies = []
    target_galaxies = []
    
    # Generate parameters first (for consistent rng)
    
    for galaxy in galaxies:
        galaxy.generate_parameters()
        
        # Sort out target galaxies
        if(is_target_galaxy(galaxy, options)):
            target_galaxies.append(galaxy)
        else:
            background_galaxies.append(galaxy)
    
        num_background_galaxies = len(background_galaxies)
        num_target_galaxies = len(target_galaxies)
        
    # If we're aiming for a certain number of target galaxies, adjust as necessary
    if options['num_target_galaxies'] > 0:
        num_ratio = options['num_target_galaxies'] / num_target_galaxies
        
        if num_ratio > 1:
            
            # Add new galaxies
            num_extra_target_galaxies = int((num_ratio-1)*num_target_galaxies)
            if options['mode']=='field':
                num_extra_background_galaxies = 0
            else:
                num_extra_background_galaxies = int((num_ratio-1)*num_background_galaxies)
            
            num_new_target_galaxies = 0
            num_new_background_galaxies = 0
            
            field = image.get_field_descendants()[0]
            
            while ((num_new_target_galaxies<num_extra_target_galaxies) and
                   (num_new_background_galaxies<num_extra_background_galaxies)):
                
                new_galaxy = field.add_galaxy()
                
                bad_type = True
                
                while bad_type:
                    new_galaxy.clear()
                    new_galaxy.generate_parameters()
                    
                    # Check what type it is, and if we can add another galaxy of that type
                    
                    if is_target_galaxy(new_galaxy, options):
                        if(num_new_target_galaxies<num_extra_target_galaxies):
                            target_galaxies.append(new_galaxy)
                            num_new_target_galaxies += 1
                            bad_type = False
                    else:
                        if(num_new_background_galaxies<num_extra_background_galaxies):
                            background_galaxies.append(new_galaxy)
                            num_new_background_galaxies += 1
                            bad_type = False
            
        elif num_ratio < 1:
            
            # Remove galaxies from the lists
            num_extra_target_galaxies = int((1-num_ratio)*num_target_galaxies)
            num_extra_background_galaxies = int((1-num_ratio)*num_background_galaxies)
            
            for _ in range(num_extra_target_galaxies):
                del target_galaxies[-1]
            for _ in range(num_extra_background_galaxies):
                del background_galaxies[-1]
            
        num_target_galaxies = len(target_galaxies)
        
        # Set up the new galaxies list
        galaxies = target_galaxies + background_galaxies
        
    else:
        num_ratio = 1
            
        
    if options['mode'] == 'stamps':
        
        # Figure out how to set up the grid, making it as square as possible
        ncols = int(np.ceil(np.sqrt(num_target_galaxies)))
        nrows = int(np.ceil(num_target_galaxies / ncols))
        
        stamp_size_pix = options['stamp_size']
        
        stamp_image_npix_x = ncols * stamp_size_pix
        stamp_image_npix_y = nrows * stamp_size_pix
        
        if options['render_background_galaxies']:
            size_ratio = (num_target_galaxies/num_ratio)*np.pi*(stamp_size_pix/2)**2 / \
                                      (full_x_size*full_y_size)
            bg_stamp_area_pix = stamp_size_pix**2/size_ratio
            bg_aperture_rad_pix = np.sqrt(bg_stamp_area_pix/np.pi)
            
            old_x_size, full_x_size = full_x_size, stamp_image_npix_x
            old_y_size, full_y_size = full_y_size, stamp_image_npix_y
            
            # Check this is valid
            if 2*bg_aperture_rad_pix > stamp_size_pix:
                raise Exception("Stamp size is too small to properly render background galaxies. " +
                                "Increase the stamp size to at least " + str(int(2*bg_aperture_rad_pix+1)) + " pixels.")
    
        icol = -1
        irow = 0
        
        # Replace the images we've set up with stamp images
        for di in range(num_dithers):
            dithers[di] =  galsim.Image( stamp_image_npix_x,
                                         stamp_image_npix_y,
                                         dtype = dithers[di].dtype,
                                         scale = dithers[di].scale )
        
    # Loop over galaxies now
    
    for galaxy in galaxies:
    
        is_target_gal = is_target_galaxy(galaxy, options)
        
        # If it isn't a target and we aren't rendering background galaxies, skip it
        if (not is_target_gal) and (not options['render_background_galaxies']):
            continue 
    
        gal_I = get_I(galaxy.get_param_value('apparent_mag_vis'), 
                      'mag_vis', 
                      gain=options['gain'], 
                      exp_time=options['exp_time'])
        
        # Set up the unsheared profiles for the psf and galaxy
        if is_target_gal:
            bulge_psf_profile = get_psf_profile(galaxy.get_param_value('sersic_index'),
                                                galaxy.get_param_value('redshift'), 
                                                True,
                                                False)
            disk_psf_profile = get_psf_profile(galaxy.get_param_value('sersic_index'), 
                                                galaxy.get_param_value('redshift'),
                                                False,
                                                False)
        else:
            bulge_psf_profile = get_psf_profile(galaxy.get_param_value('sersic_index'),
                                                galaxy.get_param_value('redshift'), 
                                                True,
                                                True)
            disk_psf_profile = bulge_psf_profile
        
        # Get the position of the galaxy, depending on whether we're in field or stamp mode
        
        if (options['mode'] == 'stamps') and is_target_gal:
        
            # Increment position first
            icol += 1
            if icol >= ncols:
                icol = 0
                irow += 1
                if irow >= nrows:
                    raise Exception("More galaxies than expected when printing cutouts.")
            
            xp_init = galaxy.get_param_value("xp")
            yp_init = galaxy.get_param_value("yp")
            
            xp_sp_shift = xp_init - int(xp_init)
            yp_sp_shift = yp_init - int(yp_init)
                
            xp = xp_sp_shift + stamp_size_pix // 2 + icol*stamp_size_pix
            yp = yp_sp_shift + stamp_size_pix // 2 + irow*stamp_size_pix
        
        elif options['mode'] == 'stamps':
            
            # Background galaxy in stamp mode. We'll have to determine a valid position
            # on a non-empty stamp
            
            # Pick a random stamp to appear on
            si = np.random.randint(0,num_target_galaxies)
            yi = si // ncols
            xi = si - yi*ncols
            
            # Use the generated xp and yp values as random input here, so we don't affect
            # the seeding
            xp_init = galaxy.get_param_value("xp")
            yp_init = galaxy.get_param_value("yp")
            
            # Place bgs in a circular aperture around target galaxies
            
            # Uniform random angle
            theta_rad = 2*np.pi * xp_init/old_x_size
            
            # Random distance, using sqrt to weight by area at a given distance
            rp = bg_aperture_rad_pix * np.sqrt(yp_init/old_y_size)
            
            xp = stamp_size_pix // 2 + xi*stamp_size_pix + rp * np.cos(theta_rad)
            yp = stamp_size_pix // 2 + yi*stamp_size_pix + rp * np.sin(theta_rad)
            
        else:
            
            xp = galaxy.get_param_value("xp")
            yp = galaxy.get_param_value("yp")
        
        xp_i = int(xp)
        yp_i = int(yp)
        
        xp_sp_shift = xp - xp_i
        yp_sp_shift = yp - yp_i
        
        subsampling_factor = int(pixel_scale / mv.psf_model_scale)
        
        # Store galaxy data to save calls to the class
        
        rotation = galaxy.get_param_value('rotation')
        spin = galaxy.get_param_value('spin')
        tilt = galaxy.get_param_value('tilt')
        
        g_shear = galaxy.get_param_value('shear_magnitude')
        beta_shear = galaxy.get_param_value('shear_angle')
        
        g_ell = galaxy.get_param_value('bulge_ellipticity')
        
        bulge_fraction = galaxy.get_param_value('bulge_fraction')
        n = galaxy.get_param_value('sersic_index')
        
        bulge_size = galaxy.get_param_value('apparent_size_bulge')
        disk_size = galaxy.get_param_value('apparent_size_disk')
        
        if is_target_gal:
        
            bulge_gal_profile = get_bulge_galaxy_profile(sersic_index = n, 
                                            half_light_radius = bulge_size, 
                                            flux = gal_I * bulge_fraction, 
                                            g_ell = g_ell, 
                                            beta_deg_ell = rotation, 
                                            g_shear = g_shear, 
                                            beta_deg_shear = beta_shear)
                
            # Convolve the galaxy, psf, and pixel profile to determine the final (well, before noise) pixelized image
            final_bulge = galsim.Convolve([bulge_gal_profile, bulge_psf_profile],
                                          gsparams=galsim.GSParams(maximum_fft_size=12000))
            
            disk_gal_image = get_disk_galaxy_image(sersic_index = n, 
                                            half_light_radius = disk_size,
                                            stamp_size_factor = options['stamp_size_factor'],
                                            rotation = rotation, 
                                            tilt = tilt,
                                            spin = spin, 
                                            flux = 1., 
                                            g_shear = g_shear, 
                                            beta_deg_shear = beta_shear, 
                                            xp_sp_shift = xp_sp_shift, 
                                            yp_sp_shift = yp_sp_shift, 
                                            image_scale = pixel_scale, 
                                            subsampling_factor = subsampling_factor)
    
            im1 = pyfftw.byte_align(disk_psf_profile.image.array)
            im2 = pyfftw.byte_align(disk_gal_image)
                
            ss_disk_image = fftw_convolve(im1, im2, norm=True)
            
            final_disk_image = rebin(ss_disk_image, 
                                    x_shift=int(subsampling_factor * xp_sp_shift + 0.5), 
                                    y_shift=int(subsampling_factor * yp_sp_shift + 0.5), 
                                    subsampling_factor=subsampling_factor)
            
            final_disk = galsim.InterpolatedImage(galsim.Image(final_disk_image, scale=pixel_scale),
                                                               flux=gal_I * (1 - bulge_fraction),
                                                               x_interpolant='nearest')
        else:
            # Just use a single sersic profile for background galaxies
            # to make them more of a compromise between bulges and disks
            gal_profile = get_bulge_galaxy_profile(sersic_index = n, 
                                            half_light_radius = bulge_size, 
                                            flux = gal_I, 
                                            g_ell = 2.*g_ell, 
                                            beta_deg_ell = rotation,  
                                            g_shear = g_shear, 
                                            beta_deg_shear = beta_shear)
            
            # Convolve the galaxy, psf, and pixel profile to determine the final (well, before noise) pixelized image
            final_gal = galsim.Convolve([gal_profile, disk_psf_profile],
                                          gsparams=galsim.GSParams(maximum_fft_size=12000))
        
        if not options['mode']=='stamps':
            if is_target_gal:
                stamp_size_pix = 2 * (
                    np.max((int(options['stamp_size_factor'] * bulge_size / pixel_scale),
                            int(options['stamp_size_factor'] * disk_size / pixel_scale)))) + \
                                      int(np.max(np.shape(disk_psf_profile.image.array))/subsampling_factor)
            else:
                stamp_size_pix = 4 * (
                    np.max((int(options['stamp_size_factor'] * bulge_size / pixel_scale),
                            int(options['stamp_size_factor'] * disk_size / pixel_scale))))
        
            if stamp_size_pix > full_x_size:
                stamp_size_pix = full_x_size
            if stamp_size_pix > full_y_size:
                stamp_size_pix = full_y_size
        
        # Determine boundaries
        xl = xp_i - stamp_size_pix // 2 + 1
        xh = xl + stamp_size_pix - 1
        yl = yp_i - stamp_size_pix // 2 + 1
        yh = yl + stamp_size_pix - 1
        
        x_shift = 0
        y_shift = 0
        
        if not (is_target_gal and (options['mode']=='stamps')):
            # Check if the stamp crosses an edge and adjust as necessary
            if (xl < 1):
                x_shift = 1 - xl
            elif (xh > full_x_size):
                x_shift = full_x_size - xh
            xh += x_shift
            xl += x_shift
            
            if (yl < 1):
                y_shift = 1 - yl
            elif (yh > full_y_size):
                y_shift = full_y_size - yh
            yh += y_shift
            yl += y_shift
        
        bounds = galsim.BoundsI(xl, xh, yl, yh)
        
        gal_images = []
        for di in xrange(num_dithers):
            gal_images.append(dithers[di][bounds])
        
        # Get centers, correcting by 1.5 - 1 since Galsim is offset by 1, .5 to move from
        # corner of pixel to center
        x_centre_offset = x_shift
        y_centre_offset = y_shift
        xc = bounds.center().x + centre_offset + x_centre_offset
        yc = bounds.center().y + centre_offset + y_centre_offset
        
        # Draw the image
        for gal_image, (x_offset, y_offset) in zip(gal_images, get_dither_scheme(options['dithering_scheme'])):
            
            if is_target_gal:
                final_bulge.drawImage(gal_image, scale=pixel_scale,
                                      offset=(-x_centre_offset + x_offset + xp_sp_shift,
                                              -y_centre_offset + y_offset + yp_sp_shift),
                                      add_to_image=True)
                final_disk.drawImage(gal_image, scale=pixel_scale,
                                     offset=(-x_centre_offset + x_offset,
                                             -y_centre_offset + y_offset),
                                     add_to_image=True,
                                     method='no_pixel')
    
            else:
                final_gal.drawImage(gal_image, scale=pixel_scale,
                                     offset=(-x_centre_offset + x_offset + xp_sp_shift,
                                             -y_centre_offset + y_offset + xp_sp_shift),
                                     add_to_image=True)
                
                pass 
                
        
        # Record all data used for this galaxy in the output table
        if is_target_gal or (options['mode']=='field'):
            output_table.add_row(otable,
                             ID = galaxy.get_full_ID(),
                             x_center_pix = xc + xp_sp_shift,
                             y_center_pix = yc + yp_sp_shift,
                             hlr_bulge_arcsec = bulge_size,
                             hlr_disk_arcsec = disk_size,
                             magnitude = galaxy.get_param_value('apparent_mag_vis'),
                             sersic_index = n,
                             bulge_ellipticity = g_ell,
                             bulge_axis_ratio = galaxy.get_param_value('bulge_axis_ratio'),
                             bulge_fraction = bulge_fraction,
                             rotation = rotation,
                             tilt = tilt,
                             spin = spin,
                             shear_magnitude = g_shear,
                             shear_angle = beta_shear,
                             subtracted_sky_level = galaxy.get_param_value('subtracted_background'),
                             unsubtracted_sky_level = galaxy.get_param_value('unsubtracted_background'),
                             read_noise = options['read_noise'],
                             gain = options['gain'],
                             is_target_galaxy = is_target_gal)
        
        if is_target_gal:
            del ss_disk_image, final_disk, disk_gal_image, disk_psf_profile
        
    return galaxies

def generate_image( image, options ):
    """ This function does the heavy lifting of actually generating an image with the GalSim toolkit.

        @param image <SHE_SIM.Image>
        @param options <dict>
        
        Side-effects: If successful, generates an image and corresponding details according to
                      the configuration stored in the image and options objects.
    """
    
    # Magic numbers
    
    centre_offset = -0.5
    
    # Set up
    
    file_name_base = join(options['output_folder'],options['output_file_name_base'] + '_')
    
    # General setup from config
    num_dithers = len(get_dither_scheme(options['dithering_scheme']))

    # Setup for the file
    dithers = []
                      
    # Create the image object, using the appropriate method for the image type
    full_x_size = int(image.get_param_value("image_size_xp"))
    full_y_size = int(image.get_param_value("image_size_yp"))
    pixel_scale = image.get_param_value("pixel_scale")
    for _ in xrange(num_dithers):
        if(options['image_datatype'] == '32f'):
            dithers.append(galsim.ImageF(full_x_size , full_y_size, scale=pixel_scale))
        elif(options['image_datatype'] == '64f'):
            dithers.append(galsim.ImageD(full_x_size , full_y_size, scale=pixel_scale))
        else:
            raise Exception("Bad image type slipped through somehow.")
        
    # Fill in the galaxies within the image
    image.autofill_children()
            
    # If shape noise cancellation is being applied, we'll use the angle for galaxy shape we generated
    # as the initial angle. Also, set up parameters for the cancellation
    if(options['shape_noise_cancellation']):
        galaxy_groups = image.get_galaxy_group_descendants()
        
        # For each group, set the rotations as uniformly distributed
        for galaxy_group in galaxy_groups:
            
            galaxies_in_group = galaxy_group.get_galaxies()
            num_in_group = len(galaxies_in_group)
            
            base_rotation = galaxy_group.get_param_value("rotation")
            
            for i, galaxy in enumerate(galaxies_in_group):
                new_rotation = base_rotation + i * 180. / num_in_group
                galaxy.set_param_param("rotation","fixed",new_rotation)
        
    # Set up a table for output
    init_cols = []
    for _ in xrange(output_table.size()):
        init_cols.append([])
    otable = Table(init_cols, names=output_table.get_names(),
                   dtype=output_table.get_dtypes())
    
    pixel_scale = image.get_param_value('pixel_scale')

    galaxies = print_galaxies(image, options, centre_offset, num_dithers, dithers,
                   full_x_size, full_y_size, pixel_scale, otable)
        
    image_ID = image.get_full_ID()
    
    sky_level_subtracted_pixel = image.get_param_value('subtracted_background') * pixel_scale ** 2
    sky_level_unsubtracted_pixel = image.get_param_value('unsubtracted_background') * pixel_scale ** 2
        
    # For each dither
    for di, (x_offset, y_offset) in zip(range(num_dithers), get_dither_scheme(options['dithering_scheme'])):
        
        
        # If we're using cutouts, make the cutout image now
        if options['mode']=='cutouts':
            dithers[di] = make_cutout_image(dithers[di], options, galaxies, otable,
                                            centre_offset )
            
        dither = dithers[di]
        
        # Output the image
        if(num_dithers>1):
            dither_file_name_base = file_name_base + str(image_ID) + '_dither_' + str(di)
        else:
            dither_file_name_base = file_name_base + str(image_ID)
            
        dither_file_name = dither_file_name_base + '.fits'
            
        dither += sky_level_unsubtracted_pixel
        if not options['suppress_noise']:
            noise = galsim.CCDNoise(galsim.BaseDeviate( image.get_full_seed() +1),
                                    gain = options['gain'],
                                    read_noise = options['read_noise'],
                                    sky_level = sky_level_subtracted_pixel)
            dither.addNoise(noise)
        galsim.fits.write(dither, dither_file_name)
            
        # Compress the image if necessary
        if(options['compress_images'] >= 1):
            compress_image(dither_file_name, lossy=(options['compress_images']>=2))
                
        
        # Output the datafile
        
        # Temporarily adjust centre positions by dithering
        otable['x_center_pix'] += x_offset
        otable['y_center_pix'] += y_offset
        
        output_table.output_details_tables(otable, dither_file_name_base, image, options)
        
        # Undo dithering adjustment
        otable['x_center_pix'] -= x_offset
        otable['y_center_pix'] -= y_offset
        
    # If we have more than one dither, output the combined image
    if(num_dithers>1):
        
        # Get the base name for this combined image
        combined_file_name_base = file_name_base + str(i) + "_combined"
        
        # Get the table and (possibly changed) otable
        combined_image, combined_otable = combine_dithers(dithers=dithers,
                                                          dithering_scheme=options['dithering_scheme'],
                                                          output_table=otable,
                                                          copy_otable=False)
        
        # Output the new image
        combined_file_name = combined_file_name_base + '.fits'
        galsim.fits.write(combined_image, combined_file_name)
        
        # Output the details file for it
        output_table.output_details_tables(combined_otable, combined_file_name_base, image, options)
    
    # We no longer need this image's children, so clear it to save memory
    image.clear()
    
    return