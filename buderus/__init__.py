"""
Support to communicate with a Buderus KM200 unit.
"""

import logging
import base64
import json
import binascii
import urllib.request, urllib.error, urllib.parse
import voluptuous as vol
from io import StringIO
from Crypto.Cipher import AES

from homeassistant.helpers import config_validation as cv
from homeassistant.const import (CONF_HOST, CONF_PASSWORD, CONF_NAME)

DOMAIN = 'buderus'

DEFAULT_NAME = 'Buderus'

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    }),
}, extra=vol.ALLOW_EXTRA)

def setup(hass, config):
    conf = config[DOMAIN]
    
    host = conf.get(CONF_HOST)
    name = conf.get(CONF_NAME)
    password = conf.get(CONF_PASSWORD)
	
    bridge = BuderusBridge(name, host, password)
	
    hass.data[DOMAIN] = bridge

    return True

class BuderusBridge(object):
    BS = AES.block_size
    INTERRUPT = '\u0001'
    PAD = '\u0000'

    def __init__(self, name, host, password):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Init Buderus")
        self.__ua = "TeleHeater/2.2.3"
        self.__content_type = "application/json"
        self._host = host
        self._key = binascii.unhexlify(password)
        self._ids = {}
        self.opener = urllib.request.build_opener()
        self.opener.addheaders = [('User-agent', self.__ua), ('Accept', self.__content_type)]
        self.name = name

    def _decrypt(self, enc):
        decobj = AES.new(self._key, AES.MODE_ECB)
        data = decobj.decrypt(base64.b64decode(enc))
        data = data.rstrip(self.PAD.encode()).rstrip(self.INTERRUPT.encode())
        return data

    def _encrypt(self, plain):
        plain = plain + (AES.block_size - len(plain) % self.BS) * self.PAD
        encobj = AES.new(self._key, AES.MODE_ECB)
        data = encobj.encrypt(plain.encode())
        return base64.b64encode(data)

    def _get_data(self, path):
        try:
            url = 'http://' + self._host + path
            self.logger.debug("Buderus fetching data from {}".format(path))
            resp = self.opener.open(url)
            plain = self._decrypt(resp.read())
            self.logger.debug("Buderus data received from {}: {}".format(url, plain))
            return plain
        except Exception as e:
            self.logger.error("Buderus error happened at {}: {}".format(url, e))
            return None
            
    def _get_json(self, data):
        try:
            j = json.load(StringIO(data.decode()))
            return j
        except Exception as e:
            self.logger.error("Buderus error happened while reading JSON data {}: {}".format(data, e))
            return False
            
    def _get_value(self, j):
        return j['value']
        
    def _json_encode(self, value):
        d = {"value": value}
        return json.dumps(d)
        
    def _set_data(self, path, data):
        try:
            url = 'http://' + self._host + path
            self.logger.info("Buderus setting value for {}".format(path))
            headers = {"User-Agent": self.__ua, "Content-Type": self.__content_type}
            request = urllib.request.Request(url, data=data, headers=headers, method='PUT')
            req = urllib.request.urlopen(request)
            self.logger.info("Buderus returned {}: {}".format(req.status, req.reason))
            if not req.status == 204:
                self.logger.debug(req.read())
        except Exception as e:
            self.logger.error("Buderus error happened at {}: {}".format(url, e))
            return None
            
    def _submit_data(self, path, data):
        self.logger.info("Buderus SETTING {} to {}".format(path, data))
        payload = self._json_encode(data)
        self.logger.debug(payload)
        req = self._set_data(path, self._encrypt(str(payload)))

"""
    def _get_type(self, j):
        return j['type']

    def _get_writeable(self, j):
        if j['writeable'] == 1:
            return True
        else:
            return False

    def _get_allowed_values(self, j, value_type):
        if value_type == "stringValue":
            try:
                return j['allowedValues']
            except:
                return None
        elif value_type == "floatValue":
            return {"minValue": j['minValue'], "maxValue": j['maxValue']}

    def update_item(self, item, caller=None, source=None, dest=None):
        if caller != "Buderus":
            id = item.conf['km_id']
            plain = self._get_data(id)
            data = self._get_json(plain)
            if self._get_writeable(data):
                value_type = self._get_type(data)
                allowed_values = self._get_allowed_values(data, value_type)
                if value_type == "stringValue" and item() in allowed_values or not allowed_values:
                    self._submit_data(item, id)
                    return
                elif value_type == "floatValue" and item() >= allowed_values['minValue'] and item() <= allowed_values[
                    'maxValue']:
                    self._submit_data(item, id)
                    return
                else:
                    self.logger.error("Buderus value {} not allowed [{}]".format(item(), allowed_values))
                    item(item.prev_value(), "Buderus")
            else:
                self.logger.error("Buderus item {} not writeable!".format(item))
                item(item.prev_value(), "Buderus")
"""