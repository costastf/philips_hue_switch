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
# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

import network
import time
import ujson
import gc
import machine

gc.collect()
# load configuration
configuration = ujson.loads(open('configuration.json').read())
ssid = configuration.get('network_ssid')
password = configuration.get('network_password')

# network initializing
network_reset_timeout = configuration.get('network_reset_timeout')
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(ssid, password)
seconds = 0
print('Waiting for network "{}"'.format(ssid))
while not wifi.isconnected():
    time.sleep(1)
    seconds += 1
    print('.',)
    if seconds == network_reset_timeout:
        print(('No network for {} seconds, '
               'reseting...').format(network_reset_timeout))
        machine.reset()
ip, netmask, gateway, dns = wifi.ifconfig()
report = ('Network connected',
          'IP address :{}'.format(ip),
          'Netmask :{}'.format(netmask),
          'Gateway :{}'.format(gateway),
          'DNS :{}'.format(dns))
print('\n'.join(report))
