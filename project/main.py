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
from machine import Pin
from library import Lamp
import time

bridge_ip = configuration.get('hue_bridge_ip')
token = configuration.get('hue_user_token')
name = configuration.get('lamp_name')

lamp = Lamp(bridge_ip, token, name)

# switch is connected to pin 0 and we start it pulled up if wemos d1
# switch = Pin(0, Pin.IN, pull=Pin.PULL_UP)

# for esp8266 01s boards a pull up resistor is required on d0 so the board
# never boots in flashing mode
switch = Pin(3, Pin.IN, pull=Pin.PULL_UP)  # using RX pin as input so we don't
# mess with the booting process
initial_state = switch.value()
print('Current switch state is {}'.format(initial_state))

while True:
    try:
        current_state = switch.value()
        if not current_state == initial_state:
            lamp.toggle()
            initial_state = current_state
        time.sleep_ms(300)
    except Exception as e:
        print('Caught exception {}, waiting two seconds'.format(e))
        time.sleep(2)
