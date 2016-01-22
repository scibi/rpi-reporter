#!/usr/bin/env python
# coding: utf-8

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import time

import statsd
import six
import w1thermsensor


class Reporter(object):
    def __init__(self, config):
        self.config = config
        self.client = statsd.StatsClient(
            config.get('server', 'localhost'), 8125, prefix=config['name'])

    def report_temperature(self, sensor_id, sensor_value):
        self.client.gauge('temperature.{}'.format(sensor_id), sensor_value)

    def report_temperature_error(self, error_id, error_count):
        self.client.gauge('errors.temperature.{}'.format(error_id),
                          error_count)

    def get_temperatures(self):
        results = {}
        unkown_sensors = 0
        sensors_not_ready = 0
        for sensor in w1thermsensor.W1ThermSensor.get_available_sensors():
            try:
                sensor_name = self.config['temperature']['sensors'][sensor.id]
                results[sensor_name] = sensor.get_temperature()
                print("DBG: {} ({}) = {} °C".format(sensor.id, sensor_name,
                                                    results[sensor_name]))
            except KeyError:
                unkown_sensors += 1
                print("WARN: Unkonwn sensor: {}".format(sensor.id))
            except w1thermsensor.core.SensorNotReadyError:
                sensors_not_ready += 1
                print("WARN: sensor not ready: {}".format(sensor.id))
        errors = {
                    'unkown_sensors': unkown_sensors,
                    'sensors_not_ready': sensors_not_ready
        }
        return results, errors

    def process_temperatures(self):
        temperatures, errors = self.get_temperatures()
        for k, v in six.iteritems(temperatures):
            self.report_temperature(k, v)
        for k, v in six.iteritems(errors):
            self.report_temperature_error(k, v)

    def report_loop(self, single_run=False):
        report_interval = self.config.get('report_interval', 5)
        while True:
            self.process_temperatures()
            if single_run:
                break
            time.sleep(report_interval)
