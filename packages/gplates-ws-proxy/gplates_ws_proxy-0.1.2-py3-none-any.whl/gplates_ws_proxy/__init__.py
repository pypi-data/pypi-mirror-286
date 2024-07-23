import warnings

warnings.warn(
    """
    ###
    ###
    ##############################################################################################
    
    The gplates-ws-proxy is deprecated!!! 

    Use [gwspy](https://pypi.org/project/gwspy/) instead!!!
    
    ##############################################################################################
    ###
    ###
    """
)


from .coastlines import get_paleo_coastlines
from .plate_model import PlateModel, reconstruct_shapely_points

__version__ = "0.1.2"
