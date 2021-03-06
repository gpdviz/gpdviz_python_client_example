#!/usr/bin/env python
# -*- coding: utf8 -*-

import random
from pprint import pprint

from swagger_client import ApiClient
from swagger_client import SensorSystemApi
from swagger_client import DataStreamApi
from swagger_client import ObservationApi
from swagger_client import SensorSystemAdd
from swagger_client import DataStreamAdd
from swagger_client import ObservationsAdd
from swagger_client.models import VariableDef
from swagger_client.rest import ApiException
from datetime import datetime


BASE_TIMESTAMP_MS = 1503090553000

random.seed(1341)


def time_ms_to_iso(time_ms):
    dt = datetime.fromtimestamp(float(time_ms) / 1000.0)
    return dt.isoformat() + 'Z'


def myrandom():
    return random.randrange(0, 32767)


class Demo(object):
    def __init__(self, sysid, host):
        self.sysid = sysid
        self.api_client = ApiClient(host=host)
        self.system_api = SensorSystemApi(self.api_client)
        self.stream_api = DataStreamApi(self.api_client)
        self.observations_api = ObservationApi(self.api_client)

    def run(self):
        # self.delete_system()
        self.register_system()
        self.generate_str1()
        self.generate_str2()
        self.generate_str3()
        self.generate_str4()

    def delete_system(self):
        try:
            api_response = self.system_api.delete_system(self.sysid)
            if False:
                pprint(api_response)
        except ApiException as e:
            print("Exception when calling SystemApi->delete_system: %s\n" % e)

    def register_system(self):
        body = SensorSystemAdd(
            sysid=self.sysid,
            name="Generated from python client",
        )

        try:
            api_response = self.system_api.register_system(body)
            if False:
                pprint(api_response)
        except ApiException as e:
            print("Exception when calling SystemApi->register_system: %s\n" % e)

    def generate_str1(self):
        self.add_str1()
        now = BASE_TIMESTAMP_MS
        secs = 60
        timestamp = now - secs * 1000
        self.add_str1_polygon(timestamp)
        self.add_scalars("str1", timestamp + 1000, secs - 1)

    def add_str1(self):
        print("add stream str1")
        body = DataStreamAdd(
            strid="str1",
            name="Stream one",
            description="Description of Stream one",
            chart_style={
                "useChartPopup": True,
                "height": 500,
                "yAxis": [{
                    "height": "50%",
                    "title": {"text": "baz (m)"},
                    "opposite": False,
                    "offset": -10
                }, {
                     "top": "55%",
                     "height": "45%",
                     "title": {"text": "temperature (°)"},
                     "opposite": False,
                     "offset": -10
                }]
            },
            variables=[
                VariableDef(
                    name="baz",
                    units="m",
                    chart_style={
                        "yAxis": 0,
                        "type": "column"
                    }
                ),
                VariableDef(
                    name="temperature",
                    units="°",
                    chart_style={
                        "yAxis": 1
                    }
                )
            ],
            map_style={
                "color": "green",
                "dashArray": "5,5"
            }
        )

        try:
            api_response = self.stream_api.register_stream(self.sysid, body)
            if False:
                pprint(api_response)
        except ApiException as e:
            print("Exception when calling StreamApi->register_stream: %s\n" % e)

    def add_str1_polygon(self, timestamp):
        observations = {
            time_ms_to_iso(timestamp): [{
                "geometry": {
                  "type": "Polygon",
                  "coordinates": [
                    [[-121.8564, 36.9], [-122.2217, 36.9574], [-122.0945, 36.6486], [-121.8674, 36.6858]]
                  ]
                }
              }]
        }
        self.add_observations("str1", observations)

    def add_observations(self, strid, observations):
        body = ObservationsAdd(observations)
        try:
            api_response = self.observations_api.add_observations(self.sysid, strid, body)
            if False:
                pprint(api_response)
        except ApiException as e:
            print("Exception when calling ObservationsApi->add_observations: %s\n" % e)

    def add_scalars(self, strid, timestamp, secs):
        print("scalarData: %s time_iso=%s  secs=%s" % (strid, time_ms_to_iso(timestamp), secs))
        observations = {}
        for i in range(secs):
            val0 = myrandom() % 1000 - 500
            val1 = myrandom() % 100
            lat =   36.8 + (myrandom() % 1000) / 10000.0
            lon = -122.1 + (myrandom() % 1000) / 10000.0
            observations[time_ms_to_iso(timestamp)] = [{
                "scalarData": {
                  "vars": ["baz", "temperature"],
                  "vals": [val0, val1],
                  "position": {"lat": lat, "lon": lon}
                }}]
            timestamp += 1000
        self.add_observations(strid, observations)

    def generate_str2(self):
        self.add_str2()

        secs = 30
        timestamp = BASE_TIMESTAMP_MS - secs * 1000

        # geometries:
        observations = {
            time_ms_to_iso(timestamp): [
                {
                  "geometry": {
                    "type": "Point",
                    "coordinates": [-121.906, 36.882]
                  }
                }, {
                  "feature": {
                    "properties": {
                      "style": {"color": "cyan", "radius": 20, "dashArray": "5,5"}
                    },
                    "geometry": {
                      "type": "Point",
                      "coordinates": [-121.965, 36.81]
                    }
                  }
                }]
        }
        self.add_observations("str2", observations)

        # data:
        print("chart data: str2")
        observations = {}

        for i in range(secs):
            timestamp += 1000
            val0 = myrandom() % 100 + 1
            val1 = myrandom() % 100 + 1

            observations[time_ms_to_iso(timestamp)] = [{
                "scalarData": {
                  "vars": ["foo", "bar"],
                  "vals": [val0, val1]
                }}]
        self.add_observations("str2", observations)

    def add_str2(self):
        print("add stream str2")
        body = DataStreamAdd(
            strid="str2",
            variables=[
                VariableDef(
                    name="foo"
                ),
                VariableDef(
                    name="bar"
                )
            ],
            map_style={
                "color": "red",
                "radius": 14
            },
            z_order=10
        )

        try:
            api_response = self.stream_api.register_stream(self.sysid, body)
            if False:
                pprint(api_response)
        except ApiException as e:
            print("Exception when calling StreamApi->register_stream: %s\n" % e)

    def generate_str3(self):
        self.add_str3()

        timestamp = BASE_TIMESTAMP_MS

        observations = {
            time_ms_to_iso(timestamp): [{
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [-122.123, 36.92], [-122.186, 36.774], [-121.9, 36.7]
                    ]
                }
              }]
        }
        self.add_observations("str3", observations)

    def add_str3(self):
        print("add stream str3")
        body = DataStreamAdd(
            strid="str3",
            map_style={
                "color": "blue"
            }
        )

        try:
            api_response = self.stream_api.register_stream(self.sysid, body)
            if False:
                pprint(api_response)
        except ApiException as e:
            print("Exception when calling StreamApi->register_stream: %s\n" % e)

    def generate_str4(self):
        self.add_str4()

        timestamp = BASE_TIMESTAMP_MS

        observations = {
            time_ms_to_iso(timestamp): [{
                  "geometry": {
                    "type": "Point",
                    "coordinates": [-122.09, 36.865]
                  }
              }]
        }
        self.add_observations("str4", observations)

        self.add_delayed_data("str4", "temperature", 10)

    def add_str4(self):
        print("add stream str4")
        body = DataStreamAdd(
            strid="str4",
            variables=[
                VariableDef(
                    name="temperature",
                    units="°C"
                )
            ],
            map_style={
                "color": "yellow",
                "radius": 10
            },
            z_order=10
        )

        try:
            api_response = self.stream_api.register_stream(self.sysid, body)
            if False:
                pprint(api_response)
        except ApiException as e:
            print("Exception when calling StreamApi->register_stream: %s\n" % e)

    def add_delayed_data(self, strid, var_name, secs):
        timestamp = BASE_TIMESTAMP_MS
        for i in range(secs):
            import time
            time.sleep(1)
            timestamp += 1000
            val = myrandom() % 100 + 1
            time_iso = time_ms_to_iso(timestamp)
            observations = {
                time_iso: [{
                    "scalarData": {
                      "vars": [var_name],
                      "vals": [val]
                    }}]
            }
            self.add_observations("str4", observations)
            print("added observation to %s: time_iso=%s" % (strid, time_iso))


if __name__ == "__main__":  # pragma: no cover
    import sys
    if len(sys.argv) > 1:
        gpdviz_host = sys.argv[1]
    else:
        print("""
        USAGE:  
           python demo1.py <gpdviz_host> 
        Example: 
           python demo1.py http://localhost:5050/api
        """)
        sys.exit(1)

    print("Using gpdviz server " + gpdviz_host)
    Demo(sysid="py_demo1", host=gpdviz_host).run()
