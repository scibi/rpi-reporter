#!/usr/bin/env python
# coding: utf-8

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from uuid import getnode
import collections
import json
import copy

import six

import requests


class ConfigError(Exception):
    pass


def recursive_update(d, u):
    for k, v in six.iteritems(u):
        if isinstance(v, collections.Mapping):
            r = recursive_update(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d


class ReporterConfig(object):

    def __init__(self):

        self.default_config = {
            'name': 'rpi-{}'.format(self.get_mac()),
            'temperature': {
                'enable': True,
                'sensors': {},
            },
        }

        self.config = copy.deepcopy(self.default_config)

    def __getitem__(self, key):
        return self.config[key]

    def get(self, key, default):
        try:
            return self[key]
        except KeyError:
            return default

    def get_mac(self):
        return '{:12x}'.format(getnode())

    def load(self, config_file_path):
        """Load config from file"""
        with open(config_file_path) as config_file:
            json_data = json.load(config_file)
            self.config = recursive_update(self.config, json_data)

    def update_config(self):
        """Update config with data downloaded over HTTP"""
        try:
            d = {
                'MAC': self.get_mac(),
            }
            config_url = self.config['auto_update_url'].format(**d)

            r = requests.get(config_url, verify=self.get('ssl_verify', True))
            if r.status_code != 200:
                raise ConfigError("Unable to fetch config. "
                                  "HTTP Code: {}".format(r.status_code))
            self.config = recursive_update(self.config, r.json())
        except KeyError:  # auto_update_url is not set
            pass

if __name__ == "__main__":
    c = ReporterConfig()
    c.load('test1.json')
    c.update_config()
    print(c.config)
