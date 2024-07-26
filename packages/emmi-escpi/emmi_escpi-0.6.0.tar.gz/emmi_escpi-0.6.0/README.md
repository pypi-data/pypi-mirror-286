ESCPI -- Generic EPICS IOC for SCPI-Enabled Equipment
=====================================================

ESCPI (**E**PICS-**SCPI**) is a generic application for exporting 
[EPICS](https://epics-controls.org/) access to scientific equipment with an
[SCPI](https://en.wikipedia.org/wiki/Standard_Commands_for_Programmable_Instruments )
interface.

Quick'n Dirty
-------------

Assuming you have a Keith 3390 available at `10.0.0.18`, try this:

```
$ MAGICSPCI_ADDRESS=TCPIP::10.0.0.18::INSTR ESPCI_DEVICE_PREFIX=KMC3XPP_KEITH ./src/espci/application.py
```

Then access one of the variables:
```
$ caget KMC3SPP_KEITH:FREQ_RBV
```
