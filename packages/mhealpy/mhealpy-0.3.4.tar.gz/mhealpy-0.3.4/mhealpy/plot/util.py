
import matplotlib as mpl
import matplotlib.pyplot as plt

from astropy.visualization.wcsaxes import WCSAxes
from astropy.coordinates import ICRS, Galactic, BarycentricMeanEcliptic, BaseCoordinateFrame

# I couldn't find a public method to do this
from astropy.coordinates.sky_coordinate_parsers import _get_frame_class

def get_fig_ax(ax, **kwargs):

    if isinstance(ax, mpl.axes.Axes):

        fig = ax.get_figure()

    else:

        fig = plt.figure(figsize = [4,4], dpi = 150)        

        ax = fig.add_axes([0,0,1,1],
                          projection  = ax,
                          **kwargs)

    if not isinstance(ax, WCSAxes):
        raise ValueError("Axes is not a valid WCSAxes")

    return fig,ax

def healpy_coord_to_astropy(coord):

    if isinstance(coord, str):

        # Transform for common HEALPix coordsys when possible
        # If unrecognized, return as input so astropy looks in
        # it registered coord frames
        
        coord = coord.lower() 
        
        if coord == 'c':
            coord = 'icrs'
        elif coord == 'g':
            coord = 'galactic'
        elif coord == 'e':
            coord = 'barycentricmeanecliptic'

    return coord

def astropy_frame_to_healpy(coord):

    if coord is None:
        return None
    
    if not isinstance(coord, BaseCoordinateFrame):
        coord = _get_frame_class(coord)()

    # Use common HEALPix coordsys when possible, and default
    # to using the coordinate frame name
    if isinstance(coord, ICRS):
        return 'c'
    elif isinstance(coord, Galactic):
        return 'g'
    elif isinstance(coord, BarycentricMeanEcliptic):
        return 'e'
    elif hasattr(coord, 'name'):
        return coord.name
    else:
        return None
