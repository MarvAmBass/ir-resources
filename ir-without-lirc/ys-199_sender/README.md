# ir-nec-send

This program is designed to send the nec codes of my ys-199 hdmi switch remote via a ir diode connected to a gpio.

_Please note: the irslinger.h is taken from https://github.com/bschwind/ir-slinger and is under licenced under the UNLICENSE_

Note: there might be other binary codes possible too, if they don't work you can modify some variables in the c file to fit the lirc remote file you've been using. it should work i think.

## Build

### Install dependency: pigpio

pigio (https://github.com/joan2937/pigpio) is a library for this timing critical coding. install it first

    git clone https://github.com/joan2937/pigpio.git
    cd pigpio
    make
    sudo make install

### Build this project

    gcc ir-nec-send.c -lm -lpigpio -pthread -lrt -o ir-nec-send

## Usage

    sudo ir-nec-send <gpio_with_ir-diode> <binary_nec_code>
    sudo ir-nec-send 3 10100100010001001001
