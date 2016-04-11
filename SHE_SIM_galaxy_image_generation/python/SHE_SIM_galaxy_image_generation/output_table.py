"""
    @file output_table.py

    Created 23 Jul 2015

    Functions related to output of details tables describing galaxy images.

    ---------------------------------------------------------------------

    Copyright (C) 2015, 2016 Bryan R. Gillis

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

from astropy.io import fits
import subprocess

from SHE_SIM_galaxy_image_generation import magic_values as mv

names_and_dtypes = (('ID','i8','K'),
            ('x_center_pix','f4','E'),
            ('y_center_pix','f4','E'),
            ('hlr_bulge_arcsec','f4','E'),
            ('hlr_disk_arcsec','f4','E'),
            ('bulge_ellipticity','f4','E'),
            ('bulge_axis_ratio','f4','E'),
            ('bulge_fraction','f4','E'),
            ('magnitude','f4','E'),
            ('sersic_index','f4','E'),
            ('rotation','f4','E'),
            ('spin','f4','E'),
            ('tilt','f4','E'),
            ('shear_magnitude','f4','E'),
            ('shear_angle','f4','E'),
            ('subtracted_sky_level','f4','E'),
            ('unsubtracted_sky_level','f4','E'),
            ('read_noise','f4','E'),
            ('gain','f4','E'),
            ('is_target_galaxy','b1','L'))

def get_names():
    """
        @brief Get the column names for the details table.
        
        @returns
            <list<string>> The column names
    """
    
    return zip(*names_and_dtypes)[0]

def get_dtypes():
    """ 
        @brief Get the data types for the details table, in the format for an astropy table.
        
        @returns
            <list<string>> The data types
    """
    
    return zip(*names_and_dtypes)[1]

def get_fits_dtypes():
    """ 
        @brief Get the data types for the details table, in the format for a fits table
        
        @returns
            <list<string>> The data types
    """
    
    return zip(*names_and_dtypes)[2]

def size():
    """ 
        @brief Get the number of columns for the details table.
        
        @returns
            <list<string>> The number of columns of the details table
    """
    
    return len(names_and_dtypes)

def add_row(table, **kwargs):
    """ 
        @brief Add a row to a table by packing the keyword arguments and passing them as a
            dict to its 'vals' keyword argument.
            
        @details Side-effects: Row is appended to end of table.
        
        @param table
            <astropy.tables.Table> Table to add the row to
        @param **kwargs
            <...> One or more keyword arguments corresponding to columns
            in the table
    """
    
    
    table.add_row(vals=kwargs)
    return
    
def output_as_fits(table,filename):
    """ 
        @brief Output an astropy table as a fits binary table.
        
        @details Side-effects: Overwrites the file at 'filename'
    
        @param table
            <astropy.tables.Table> Table to be output
        @param filename
            <string> Name of file to output this table to
    """
    fits_cols = []
    for name, _, my_format in names_and_dtypes:
        fits_cols.append(fits.Column(name=name, format=my_format, array=table[name]))
    
    # Set up the binary extension HDU with the correct data and filenames
    my_bin_hdu = fits.BinTableHDU.from_columns( fits_cols )
    
    # Output it to the desired filename
    my_bin_hdu.writeto(filename, clobber=True)
    
    return

def output_details_tables(table, file_name_base, options):
    """ 
        @brief Output an astropy table as an ascii file and/or a fits binary table.
        
        @details Side-effects: Overwrites files with new tables
    
        @param table
            <astropy.tables.Table> Table to be output
        @param file_name_base
            <string> Root of the filename (which will be expanded with the proper tail for each
            version of the table output)
        @param options
            <dict> The options dictionary for the run.
    """
    
    if ((options['details_output_format'] == 'ascii') or (options['details_output_format'] == 'both')):
        text_file_name = file_name_base + mv.ascii_details_file_tail
        table.write(text_file_name, format='ascii.commented_header')
        # Allow group access to it
        cmd = 'chmod g+rw ' + text_file_name
        subprocess.call(cmd, shell=True)
        
    if ((options['details_output_format'] == 'fits') or (options['details_output_format'] == 'both')):
        fits_file_name = file_name_base + mv.fits_details_file_tail
        output_as_fits(table, fits_file_name)
        # Allow group access to it
        cmd = 'chmod g+rw ' + fits_file_name
        subprocess.call(cmd, shell=True)
        
    return