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
import machine
from machine import Pin
from library import Lamp
import time

exception_timeout = configuration.get('exception_reset_timeout')


def get_switch():
    try:
        pin_number = configuration.get('pin_number')
        pin_supports_pull_up = configuration.get('pin_supports_pull_up')
        args = [pin_number, Pin.IN]
        kwargs = {}
        if pin_supports_pull_up:
            kwargs.update({'pull': Pin.PULL_UP})
        pin = Pin(*args, **kwargs)
        return pin
    except Exception as e:
        print(('Caught exception, {}'
               'resetting in {} seconds...').format(e, exception_timeout))
        time.sleep(exception_timeout)
        machine.reset()


def main():
    try:
        bridge_ip = configuration.get('hue_bridge_ip')
        token = configuration.get('hue_user_token')
        name = configuration.get('lamp_name')

        lamp = Lamp(bridge_ip, token, name)
        switch = get_switch()
        initial_state = switch.value()
        print('Current switch state is {}'.format(initial_state))
        while True:
            try:
                current_state = switch.value()
                if not current_state == initial_state:
                    lamp.toggle()
                    initial_state = current_state
                    print('Current switch state is {}'.format(initial_state))
                time.sleep_ms(300)
            except Exception as e:
                print(('Caught exception {exception}, waiting {timeout} '
                       'seconds').format(exception=e,
                                         timeout=exception_timeout))
                time.sleep(exception_timeout)
    except Exception as e:
        print(('Caught exception, {}'
               'resetting in {} seconds...').format(e, exception_timeout))
        time.sleep(exception_timeout)
        machine.reset()


if __name__ == '__main__':
    main()
