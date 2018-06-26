from ..utils.datatypes import *

def param(p):
    return '/' + p

def build_url(base, 
        meter_id, 
        fs,
        method, 
        database, 
        timemode, 
        when=None, 
        start_time=None,
        end_time=None,
        num_format=None,
        **kwargs
        ):

    """
    Builds the url to connect to the API
    """
    
    url = base
    url += param(method)
    url += param(database)
    url += param(timemode)
    if method == Method.GET_VALUES_AT_TIME_JSON:
        url += param(when)
    meter = fs.format(meter_id)
    url += param(meter)

    ## For multiple readings
    if start_time is not None:
        url += param(str(start_time))
    if end_time is not None:
        url += param(str(end_time))
    if num_format is not None:
        url += param(num_format)

    ## Change of Value 
    if Extra.CHANGE_OF_VALUE in kwargs:
        url += param(Extra.CHANGE_OF_VALUE)
        # -> True = Excel mode
        if kwargs[Extra.CHANGE_OF_VALUE]:
            url += param(Extra.EXCEL)

    elif Extra.INTERVAL in kwargs:
        url += param(Extra.INTERVAL)
        url += param(str(kwargs[Extra.INTERVAL]))

    return url
