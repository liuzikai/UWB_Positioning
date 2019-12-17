<!--
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
-->

This is a project of UWB positioning system based on Decawave DWM1001 (DW1000). The main portion of this repository is basically a fork of [Decawave/mynewt-dw1000-apps](https://github.com/Decawave/mynewt-dw1000-apps). The filtering and positioning part is in cs498_positioning folder. See [cs498_positioning/README](cs498_positioning/README.md) there.

## Getting Started with DWM1001 (Blinky)

1. Download and install Apache Newt.

You will need to download the Apache Newt tool, as documented in the [Getting Started Guide](http://mynewt.apache.org/latest/get_started/index.html). 

Prerequisites: You should follow the generic tutorials at http://mynewt.apache.org/latest/tutorials/tutorials.html, particularly the basic Blinky example that will guide you through the basic setup.

2. Download the DW1000 Mynewt apps.

```no-highlight
    git clone git@github.com:Decawave/mynewt-dw1000-apps.git
    cd mynewt-dw1000-apps
```

3. Running the newt install command downloads the apache-mynewt-core, mynewt-dw1000-core, and mynewt-timescale-lib packages, these are dependent repos of the mynewt-dw1000-apps project and are automatically checked-out by the newt tools.

```no-highlight
    $ newt install
```

4. To erase the default flash image that shipped with the DWM1001.

```no-highlight
JLinkExe -device nRF52 -speed 4000 -if SWD
J-Link>erase
J-Link>exit
```

5. Build the new bootloader applicaiton for the DWM1001 target.

(executed from the mynewt-dw1000-app directory).

```no-highlight

newt target create dwm1001_boot
newt target set dwm1001_boot app=@apache-mynewt-core/apps/boot
newt target set dwm1001_boot bsp=@mynewt-dw1000-core/hw/bsp/dwm1001
newt target set dwm1001_boot build_profile=optimized 
newt build dwm1001_boot
newt create-image dwm1001_boot 1.0.0
newt load dwm1001_boot

```

6. Build the Blinky app.

```no-highlight
newt target create dwm1001_blinky
newt target set dwm1001_blinky app=apps/blinky
newt target set dwm1001_blinky bsp=@mynewt-dw1000-core/hw/bsp/dwm1001
newt target set dwm1001_blinky build_profile=debug
newt build dwm1001_blinky
newt create-image targets/dwm1001_blinky 1.0.0
newt load dwm1001_blinky
```