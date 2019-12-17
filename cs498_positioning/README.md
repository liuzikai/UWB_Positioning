This folder contains scripts running on the host computer to evaluate and analyze ranging and positioning of DWM1001.

# Authors
* Zikai Liu (zikail2@illinois.edu)
* Kerui Zhu (keruiz2@illinois.edu)

# Components
* README.md: this file.
* data/: store experiment data
* config.py: configuration of positions of reference nodes
* data_io.py: functions of storing and reading position data file
* kalman.py: functions of Kalman filtering (not using)
* main.py: main program of positioning
* main_ranging.py: main program of ranging
* port.py: deprecated
* pos_plot.py: functions of visualizing position
* positioning.py: functions of extracting data from telnet, filtering and calculating position from ranging data
* raw_processor.py: helper script to post-process raw data

# Setup Device Network
We have evaluate sample app of twr_nranges_tdma with single-side two-way ranging (twr_ss_nrng, as configured in apps/twr_nranges_tdma/pkg.yml). See apps/twr_nranges_tdma/README.md for more details.

Currently the tag device has to connect to the host computer. Output data is transmitted through Segger RTT and get relayed to telnet port by GDB (yes, you put the tag device in debug mode to collect data).

Using MyNewt toolchain, connect the tag node to the host computer, and run
```shell
newt run twr_tag_tdma 0.1.0
```

(Make sure the bootloader is already flashed as mentioned in README in upper level directory.)

In GDB, continue, and output will be relayed to telnet port. Then run scripts in this directory. Scripts may need to be modified based on your needs.

# About Algorithms
For 3D positioning, at least data from 4 reference nodes are needed. The script main.py won't produce output if the number of reference nodes is not enough. But it works with more than 4 reference nodes, and the accuracy is expected to better.

Position update frequency is much slower than raning frequency, so a bunch of data points are available to calculate one position. Medium filtering is applied.

The Trilateration algorithm plus the least-squares method is used to calculate position.

# License of Files in This Directory

Copyright 2019 ZIKAI LIU and KERUI ZHU

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
