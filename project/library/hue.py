# -*- coding: utf-8 -*-
# Micropython code to toggle philips hue lamp through an esp8266
# Copyright (C) 2017  Costas Tyfoxylos
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import urequests
import ujson


class Lamp(object):
    def __init__(self, bridge_ip, token, lamp_name):
        self.bridge_ip = bridge_ip
        self.token = token
        self._lights = ('http://{bridge}/api/{token}/'
                        'lights').format(bridge=bridge_ip,
                                         token=token)
        self.number = self._get_index_by_name(lamp_name)
        self._url = '{base}/{number}'.format(base=self._lights,
                                             number=self.number)

    def _get_index_by_name(self, name):
        response = urequests.get(self._lights)
        lights = response.json()
        response.close()
        try:
            number = next((int(index) for index, info in lights.items()
                           if info.get('name', '').lower() == name.lower()))
        except StopIteration:
            raise ValueError('No lamp with that name! {}'.format(name))
        return number

    @property
    def status(self):
        return 'on' if self._state else 'off'

    @property
    def _state(self):
        response = urequests.get(self._url)
        status = response.json()['state']['on']
        response.close()
        return status

    @_state.setter
    def _state(self, status):
        status = True if status else False
        payload = {"on": status}
        state_url = '{base}/state'.format(base=self._url)
        response = urequests.put(state_url, data=ujson.dumps(payload))
        print(response.text)
        response.close()

    def toggle(self):
        self._state = not self._state
        print("Lamp's status is:{}".format(self.status))
