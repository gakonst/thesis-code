#!/usr/bin/env python
import sys
import json
import requests
requests.packages.urllib3.disable_warnings()

from ..utils.colors import green, red, yellow

from ..utils.logconfig import configure_logging

from ..utils.datatypes import (
        Method, 
        Timemode, 
        NumberFormat,
        Time
)

from .formatters import param, build_url

import random 

class MonitoringClient(object):

    """
    Monitoring server module:
    https://smart-comp.honda-ri.de/app.php/monitor/monitoring/help/rest
    """

    def __init__(self, 
                meter_id,
                url='https://smart-comp.honda-ri.de/app.php',
                database='monitoring'):

        """ 
        Mandatory correct username/password for logging in the API
        Default url: https://smart-comp.honda-ri.de/app.php
        Default database: monitoring
        """

        self.logger = configure_logging(meter_id)

        self.API_ENDPOINT = 'api'
        self.METER_FORMATSTRING = '("{}")'
        self.meter_id = meter_id
        self.api_url = url + param(self.API_ENDPOINT)
        self.database = database

        info = 'API Endpoint {}'.format(self.api_url)
        self.logger.debug(green(info))

        # Need to disable env and SSL verification bc of proxy
        session = requests.Session()
        session.verify = False
        session.trust_env = False
        self._test_connection(session)

        self.api = session


    def get_single_reading(self, 
            method=Method.CURRENT_JSON, 
            timemode=Timemode.LOCAL,
            when=Time.NOW):
        """ 
        Get current values for an URN. 
        Default return format is json and localtime tmode.
        Default time to return 
        """

        url = build_url(self.api_url,
            self.meter_id,
            self.METER_FORMATSTRING,
            method,
            self.database,
            timemode,
            when=when
        )

        resp = self._request_blocking(url)
        data = json.loads(resp.content)[self.meter_id]

        reading, timestamp = data['value'], data['timeStamp']/1000
        info = 'Got {} kWh at t={} from Server'.format(reading, timestamp)
        self.logger.info(green(info))
        return (reading, timestamp)


    def get_multiple_readings(self,
            start_time,
            end_time,
            timemode=Timemode.LOCAL,
            num_format=NumberFormat.DE,
            **kwargs):

        """
         Get multiple readings in a given time window
         Returns the csv data unformatted
        """
        url = build_url(self.api_url,
            self.meter_id,
            self.METER_FORMATSTRING,
            Method.URNS_CSV,
            self.database,
            timemode,
            start_time=start_time,
            end_time=end_time,
            num_format=num_format,
            **kwargs
        )


        resp = self._request_blocking(url)
        return (resp.text)

    def _request_blocking(self, url):
        # TODO: Implement retries according to https://www.peterbe.com/plog/best-practice-with-retries-with-requests
        try: 
            resp = self.api.get(url)
        except:
            pass
            # error 
        info = 'Fetching {}'.format(url)
        self.logger.debug(green(info))
        return resp


    def _test_connection(self, session):
        try: 
            session.get(self.api_url)
        except:
            self.logger.info("Cannot reach API!")
            sys.exit(-1)
        



if __name__ =="__main__":
    meter_id = 'H3.Z40.W'
    meter = MonitoringClient(meter_id)

    data = meter.get_single_reading()

    # start_time = 1523360380
    # end_time = 1523363980
    # data = meter.get_multiple_readings(
    #         start_time, 
    #         end_time, 
    #         timemode=Timemode.TIMESTAMP,
    #         changeOfValue=True) # True = excel mode

    # data = meter.get_multiple_readings(
    #         start_time, 
    #         end_time, 
    #         timemode=Timemode.TIMESTAMP,
    #         changeOfValue=False)

    # data = meter.get_multiple_readings(
    #         start_time, 
    #         end_time, 
    #         timemode=Timemode.TIMESTAMP,
    #         interval=5)
