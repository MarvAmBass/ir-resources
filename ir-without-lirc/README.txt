## Use this to send IR Codes without LIRC

more infos about using IR without LIRC on a Linux System you find here: https://blog.bschwind.com/2016/05/29/sending-infrared-commands-from-a-raspberry-pi-without-lirc/

It's not that easy, since it requires very precise timing - you need to run your code in a special mode to achieve that.

### pigpio

pigio (https://github.com/joan2937/pigpio) is a library for this timing critical coding. install it first

    git clone https://github.com/joan2937/pigpio.git
    cd pigpio
    make
    sudo make install


### ir-slinger

bschwind created ir-slinger (https://github.com/bschwind/ir-slinger) this header file to help you when coding actual ir sending programms.


    git clone https://github.com/bschwind/ir-slinger.git
