# Hardware architecture

## Overview

The Vision Pro EVS hardware is reconstructed as a modular vehicle system around a protected power domain, NVIDIA/Linux Vision Core, deterministic vehicle I/O controller, Windows/Cadmium display domain, camera network, and radios.

![Hardware block diagram](https://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/Gitbub0816/strijder/main/docs/diagrams/hardware-blocks.puml)

## Major assemblies

### 1. Protected power and UPS assembly

Responsibilities:

- battery and ignition input;
- reverse-polarity and transient protection;
- input filtering and protected rail generation;
- branch switching and overcurrent protection;
- ignition/wake state reporting;
- backup-energy management;
- orderly shutdown hold-up;
- voltage, current, and temperature telemetry.

The initial planning load is approximately 75 W. Final input range, transient standards, fuse values, and conversion topology are TBD.

### 2. Vision Core

Established direction:

- NVIDIA-class high-performance processing;
- Linux operating system;
- background/headless operation rather than a client-facing desktop;
- local solid-state evidence storage;
- camera ingest and encoding;
- computer-vision processing capacity;
- GPS, radio, vehicle, and evidence integration.

Open selections include exact module, industrial lifecycle, carrier, camera interfaces, storage media, cooling, and update/secure-boot implementation.

### 3. Vehicle I/O controller

Proposed as a physically and logically separate MCU assembly providing:

- ignition, voltage, auxiliary, and interlock sensing;
- physical lighting-selector inputs;
- deterministic warning-light mode resolution;
- protected low-level control outputs;
- feedback/fault inputs;
- CAN/LIN/serial interfaces as required;
- hardware watchdog;
- safe behavior independent of Linux, Windows, CAD, or WAN.

It does not directly carry the full lightbar current. Dedicated fused vehicle power and an external power-control stage carry high-current loads.

### 4. Main dashcam head

The recovered harness includes a `Main Dashcam Head` connection. Its precise physical composition is TBD, but its logical functions may include:

- primary forward camera;
- microphones/status indicators;
- manual event-mark control;
- operator-facing camera/status feedback;
- local sensor inputs;
- media and control link to Vision Core.

The earlier harness called this `HDP20_MainHead`; the later allocation assigns 20 positions.

### 5. CAD/Windows display

The later harness assigns 40 positions to the CAD/Windows display. It hosts or connects to:

- Windows compute;
- touch display and physical controls;
- Cadmium MDT;
- map and navigation presentation;
- messaging and unit status;
- system health and permitted camera/control UI.

Whether compute is display-integrated or separate remains open.

### 6. Auxiliary-camera display

The later harness assigns eight positions for an auxiliary display. Intended use is a low-latency view of a selected rear/side/auxiliary camera without making the CAD UI responsible for all video presentation.

### 7. Cameras

The early hardware concept had four `FAKRA_Cam` connections. The design supports a main dashcam and optional rear, side, or auxiliary cameras.

Unresolved camera parameters:

- sensor and lens;
- HDR performance;
- day/night or IR behavior;
- resolution and frame rate;
- link type/serializer;
- synchronization;
- power-over-coax versus separate power;
- heater requirements;
- enclosure ingress and impact rating.

### 8. Communications and positioning

Established conceptual radios/features:

- cellular;
- Wi-Fi;
- Bluetooth;
- GPS/GNSS;
- external LTE antenna connection in the early design (`SMA_LTE`).

Exact modem, carrier certification, antenna diversity, GNSS dead reckoning, and RF coexistence design remain TBD.

### 9. Vehicle interfaces

The hardware provides separate interfaces for:

- CAN/OBD/sense;
- validator;
- auxiliary sensor;
- interlock actuator;
- lighting controller;
- lighting selector.

All external lines require an electrical classification: power, ground return, chassis/shield, digital input, analog input, communications, low-side/high-side output, or protected sense.

## Isolation and independence goals

- Each camera fault should be electrically isolated where practical.
- Storage failure should not disable vehicle I/O.
- Windows/display failure should not disable recording.
- Vision Core failure should not create uncontrolled I/O outputs.
- Lighting power faults should not brown out evidence compute.
- Radio faults or absent antennas should not prevent local functions.
- A service connector should not bypass evidence protection or vehicle-control authorization.

## Hardware health measurements

Recommended measurements include:

- input voltage and protected-rail voltages;
- total and branch currents;
- battery/UPS state and temperatures;
- compute, storage, enclosure, and power-stage temperatures;
- fan speed or cooling health where active cooling is used;
- storage life indicators and write errors;
- camera link lock and frame counters;
- GNSS fix quality and antenna state;
- modem status and signal measurements;
- I/O controller reset/watchdog reason;
- output-command versus output-feedback agreement.

## Service boundaries

Serviceable field-replaceable units should be defined after mechanical packaging is chosen. Candidates are power/UPS module, Vision Core, SSD/evidence module, Windows display, main dashcam head, auxiliary display, each external camera, cellular/GNSS antenna assembly, I/O controller, and lighting power controller.
