# ir-resources
ir related stuff - lirc remote configs, ir without lirc, ...


## Infos

### Encode RAW to NEC

_if you have a lirc remote file with raw data, you can simply use __irrecord -a remote_configfile.config__ to convert it to nec_

#### Doing it by Hand:

(https://blog.bschwind.com/2016/05/29/sending-infrared-commands-from-a-raspberry-pi-without-lirc/)

I was thrilled to find this matches up very nicely with the NEC protocol! You can see the 9 ms pulse at the beginning, followed by the 4.5 ms gap. The script is off by several hundred microseconds but it's close enough to see what's going on. The next step is to convert this series of pulses to binary.

The basics of the NEC protocol are simple:

* "logical 0" is a 562.5 microsecond pulse, followed by a 562.5 microsecond gap.
* "logical 1" is a 562.5 microsecond pulse, followed by a 1687.5 microsecond gap.

Keep in mind that in my pulse list above, a 0 is a pulse, and a 1 is a gap. So to start, chop off the leading 9 ms pulse and the 4.5 ms gap and then read the lines two at a time. The first two entries are:

    0 631
    1 497

That's a roughly 565 pulse followed by a 565 gap, so this is a 0. Next is:

    0 628
    1 1607

A 565 pulse followed by a 1687 gap (you can start to see why the numbers don't need to be exact). This is a 1. Next:

    0 635
    1 490

565 pulse followed by a 565 gap, that's a 0. And so on. Notice the signal also has a trailing 565 pulse at the end. Some signals have this, some don't, but the NEC protocol suggests that the signal should have it. We end up with

    01000001101101100101100010100111
