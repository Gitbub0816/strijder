# Vehicle I/O, harness, camera and display engineering

Revision: concept A, 2026-09-09. **Inferred engineering proposal, not a fabrication drawing or released vehicle modification.**

## 1. Basis and boundary

The historical dossier identifies a Linux/NVIDIA Vision Core, separate Windows/Cadmium operator computer, four early camera ports, physical lighting selector, lighting controller, vehicle sense, validator and interlock connectors. It does not identify final electrical levels, device models, wire gauges, bus messages or cavity assignments. See [connector history](../hardware/CONNECTORS_AND_HARNESS.md) and [logical interfaces](../architecture/INTERFACES.md).

This document develops those groups into reviewable circuits and interfaces. Reference designators and net names below are newly proposed; none is claimed to have been recovered from the conversation. All numerical connector position counts are inherited concepts, not verified sufficient pin budgets. Undefined validator/actuator semantics block circuit release.

Editable functional schematic sheets:

- [Vehicle I/O](schematics/vehicle-io.puml)
- [Camera/display links](schematics/camera-display-links.puml)

These are signal-level functional schematics. They do not contain complete electrical CAD symbols, footprints, component values or an ERC-verifiable netlist.

## 2. Proposed I/O sheet partition

| Refdes/group | Function | Implementation gate |
|---|---|---|
| J201 | Vehicle CAN/sense functional connector | Historical six positions; actual map TBD |
| J202 | Physical lighting selector | Historical 16 positions; discrete versus bus unresolved |
| J203 | Lighting controller control/feedback | Historical 16 positions; electronics power only |
| J204 | Auxiliary sensor | Historical three positions; does not imply a particular sensor interface |
| J205 | Interlock interface | Historical four positions; actuator type and safe state unknown |
| J206 | Validator | Historical six positions; meaning must be confirmed |
| U201 | Deterministic I/O MCU | Timers, watchdog, protected boot and enough independent ports; exact MCU TBD |
| U202 | Vehicle-side CAN transceiver | Silent/listen-only capability; voltage and bus-fault envelope to be selected |
| U203 | Ignition comparator/input conditioner | Hysteresis, bounded thresholds and power-off behavior |
| U204 | Independent supervisor/watchdog | Reset and output-inhibit path independent of application execution |
| U205 | Selector input-conditioning bank | Channel count follows selector decision |
| U206 | External-control driver or protocol transceiver | Not populated until lighting vendor interface is known |
| U207 | Interlock driver assembly | Hold unpopulated pending actuator hazard analysis |
| D201 / FL201 | CAN-rated protection / optional EMC filter | Capacitance, common-mode range and layout verified on selected network |
| R201–R204, C201, D202 | Ignition divider, current limiting, filter, clamp | Values depend on input envelope and chosen U203 |

No MCU GPIO is permitted to connect directly to battery-level vehicle wiring. Protect connector-side circuits before routing into logic. Keep power return, quiet signal reference and shield/chassis labels distinct; define the bond deliberately rather than relying on mounting screws.

## 3. Ignition and external-input circuit intent

Proposed ignition path: `IGN_RAW` → series current-limiting resistance R201 → protected divider R202/R203 and RC node C201 → comparator U203 → `IGN_VALID` → MCU U201 and power-state supervisor. D202 represents coordinated transient/clamp protection, not an assumed single diode solution. R204 establishes the comparator output state when U203 is unpowered if its output architecture permits it. Actual component allocation may change after design calculations.

Size the divider using `Vnode = Vinput × Rbottom / (Rtop + Rbottom)`, including resistor tolerance, clamp leakage and comparator input current. Check every resistor's working voltage and transient energy; split resistance into series parts where required. Select hysteresis so cranking excursions cannot repeatedly toggle a clean ignition state. Calculate RC delay and debounce against the required shutdown/wake latency. A clamp into an unpowered logic rail must not back-power U201; either provide a validated discharge/clamp destination or use a front end specifically supporting the fault.

External discrete channels follow the same protected pattern, but active-high, active-low, open-collector and dry-contact inputs require different bias arrangements. Do not fit universal pull-ups until the peripheral specification is known. For each input publish guaranteed asserted/deasserted voltage ranges, invalid band, source impedance, maximum input current, debounce and fault response.

| Named net | Electrical interpretation | Required behavior |
|---|---|---|
| `IGN_RAW` | Unconditioned vehicle ignition sense | Not a logic supply; protection rated to specified vehicle envelope |
| `IGN_VALID` | Local conditioned logic | Stable hysteretic state; report invalid supply separately |
| `SEL_RAW[n]` | External selector request | Protected input or replaced by selected field-bus pair |
| `SEL_VALID[n]` | Conditioned selector request | Impossible combinations become explicit faults |
| `AUX_RAW` | Unclassified sensor conductor | Do not energize until voltage and signaling are identified |
| `INTERLOCK_FB` | Actual actuator/interlock feedback | Unknown feedback must not be treated as permission |
| `IO_HEALTHY` | Supervisor/application health qualification | Not the sole basis for preserving emergency-light availability |
| `AUTO_CMD_ENABLE` | Gate for computerized requests | Hardware-defined inactive reset state |
| `LIGHT_CMD` | Logical mode command bundle | Not a load-power conductor; physical encoding TBD |
| `LIGHT_FB` | Measured/acknowledged state bundle | Distinguish command accepted from actual load functioning |

## 4. Vehicle bus boundary

J201 vehicle pair `VEH_CAN_H/L` → D201 protection → optional FL201 → U202 → `VEH_RXD` into U201. A separate `VEH_TXD` path is disabled by default using transceiver silent mode with a hardware-defined reset bias. Passive monitoring is the initial proposal. OBD identifies a diagnostic access context, not permission to transmit arbitrary diagnostic or control frames.

For a concrete component reference, TI's TCAN1051-Q1 family provides silent mode, passive unpowered behavior and several voltage/interface variants. This makes it a candidate for evaluating the monitoring boundary, not a selected BOM part. Exact suffix, voltage compatibility and protection must be reviewed against the installation. [TI TCAN1051-Q1 datasheet](https://www.ti.com/lit/ds/symlink/tcan1051-q1.pdf)

Do not bridge vehicle CAN electrically to a private lighting CAN network. If the lighting controller uses CAN, use a separate transceiver/controller channel and explicitly translate authorized application messages. A CAN transceiver does not authenticate commands. Do not add an unconditional termination resistor to an existing vehicle bus; provision termination only after topology, existing endpoints and stub length are confirmed. A galvanically isolated variant requires an isolated supply and an intentional reference/EMC strategy, not just a digital isolator inserted into one signal.

Any later diagnostic transmission requires a vehicle-specific allowlist, defined operating conditions, rate limit, session authorization and bench verification. Hardware gate release is a deliberate configuration/service step. Authentication of software requests does not establish vehicle compatibility or functional safety.

## 5. Lighting command, load-power and override separation

The compute enclosure supplies only the controller electronics if needed. Warning-light load energy follows **vehicle source → source fuse → external rated lighting power controller → individually protected load branches → lamps → rated return**. J203 must not become an undocumented path carrying the entire lightbar current.

U201 resolves permitted computer requests against physical selector state and valid interlocks. Its link to the Vision Core carries named modes and acknowledgements rather than arbitrary GPIO writes. Packets need version, source identity, sequence, monotonic expiry, mode, integrity protection and disposition. A local UART CRC detects corruption but does not authenticate its sender; trust and authentication depend on the selected transport and threat model.

There must be an independently reviewable operator-control path that survives Linux and Windows failure. Candidate A is a vendor-supported direct selector into the external controller, with U201 observing/asking for approved modes. Candidate B is a dedicated safety-reviewed selector resolver within the lighting subsystem, independent of U201 application failure. This is **not** permission to parallel two drivers onto the same line. The arbitration interface, electrical ownership and manual priority must be documented before wiring.

| Fault | Proposed requirement | Unresolved release decision |
|---|---|---|
| Vision Core/Windows crash | Physical lighting operation remains available; stale computer requests expire | Expiry interval and UI indication |
| I/O reset/watchdog | Automatic request outputs enter defined inactive state | External lighting behavior and manual continuity |
| Broken selector conductor | Report invalid where detectable | Whether wiring supports supervised/open-circuit discrimination |
| Lost feedback | Indicate command/feedback mismatch | Whether operating mode may continue |
| Shorted control conductor | Contain electrically; prevent a compute brownout | Vendor input response and remedial mode |
| Lighting load short | Affected branch isolates without dropping compute | Fuse/switch coordination and return routing |
| Interlock invalid | No newly enabled actuator action | Hazard analysis may require hold, release or another state |

“Everything off” and “hold last state” are not universally safe emergency-vehicle policies. Final behavior must be resolved per function, including warning-light visibility and the meaning of interlocks. The dossier does not establish authority to actuate brakes, steering, drivetrain or engine immobilization. No such outputs are proposed here.

## 6. Camera electrical alternatives

The four historical FAKRA camera ports preserve a count, not a codec or pinout. FAKRA is a connector family; it does not establish serializer compatibility, PoC voltage or whether a camera is analog or digital.

| Architecture option | Schematic implication | Blocking selection |
|---|---|---|
| Serialized coax + PoC | Per-channel protected DC injection/filter; compatible serializer/deserializer; CSI output to carrier | Link family, sensor, cable, PoC network, driver support |
| Serialized coax + separate power | Media coax plus separate fused supply/return pair per camera | Harness expansion, grounding and connector split |
| Network cameras | Ethernet physical layer and camera supply or compliant PoE equipment | Ordinary versus automotive Ethernet, encoding, latency and security |
| USB/local cameras | Supported USB topology and protected power switching | Cable reach, locking connector, bandwidth and installation environment |

A specific feasibility reference is TI DS90UB960-Q1, a four-input FPD-Link III deserializer with dual CSI-2 ports and PoC-compatible link support. It illustrates a possible four-camera hub; it is not automatically compatible with any camera, NVIDIA carrier or requested resolution. The PoC filtering/power circuit remains external design work. [TI DS90UB960-Q1 datasheet](https://www.ti.com/lit/ds/symlink/ds90ub960-q1.pdf)

Proposed channel `i`: U301i protected camera-power branch → L301i/associated qualified PoC filter → `CAM_i_COAX`; AC media coupling into compatible U302 hub; remote camera has matching power extraction, local regulation and serializer. `CAM_i_FAULT` and `CAM_i_LINK_LOCK` are separate status concepts. A powered camera may have no valid video; a locked link may carry frozen frames. Track frame timestamps/counters and image delivery independently.

PoC inductors, coupling capacitors and ESD devices must be chosen for the actual link-frequency spectrum, bias current, impedance and voltage transients. Do not treat the diagram as permission to inject 12 V into an unspecified camera. Short one channel and prove other channels continue. A four-camera system does not necessarily mean four cameras plus the main dashcam head; the head may contain channel 1, or it may introduce an additional camera. This count must be resolved before bandwidth and power budgets are frozen.

## 7. Displays and cabling

The 40-position CAD/Windows display concept has two mutually exclusive primary implementations: an integrated Windows panel computer receiving protected power and a network data link; or a separate Windows computer driving a touch display through supported video and touch interfaces. Do not connect raw CSI camera data to HDMI or DisplayPort. The eight-position auxiliary display also lacks a specified transport and cannot be assumed to carry any chosen video format.

Proposed names are `MDT_PWR/RTN`, `MDT_DATA`, `DISPLAY_VIDEO`, `TOUCH_DATA`, `AUX_DISPLAY_PWR/RTN` and `AUX_VIDEO`. These denote interface bundles, not single connector contacts. Choose dedicated high-speed connectors or validate the full mixed connector/cable channel. Contact count alone does not establish differential impedance, shielding or bandwidth.

An auxiliary live-view display driven only by Vision Core loses picture when that core fails. If independent rear/side viewing is required, select a camera system with a supported separate output/path or a dedicated receiver/selector; do not passive-split a high-speed coax stream. Record glass-to-glass latency and boot time requirements before choosing the topology.

## 8. Harness drawing release checklist

For each J201–J206 and camera/display connector, release a cavity-view drawing with exact manufacturer, mating half, key, contact, seal, wire gauge, insulation, color, twist, shield, branch source, wire length and test points. Include mating-face versus wire-entry orientation and unused-cavity seals. Specify whether chassis shield bonds are direct, capacitive or isolated at each end after EMC evaluation.

The earlier 22 peripheral power-path contact estimate is only an allocation proposal. It neither proves that each connector fits all signals nor establishes safe current sharing between parallel contacts. Do not reuse the earlier 4.2 A/contact figure as a qualified limit. Current capacity depends on actual contacts, populated adjacent cavities, temperature, wire size, imbalance and single-contact faults. Main source contacts are distinct from summed peripheral contacts. PoC shields are part of the designed current return and RF path, not a generic extra ground pin.

## 9. Verification matrix

| ID | Test | Acceptance evidence before release |
|---|---|---|
| IO-01 | Sweep ignition and external input voltages, powered/unpowered | Documented thresholds; no MCU overstress/back-power; bounded debounce |
| IO-02 | Reset, stuck software and watchdog event | Automatic-command inhibit at defined time; physical path remains functional |
| IO-03 | Open/short/cross-short every external signal on bench | Safe documented behavior and no propagation outside protection boundary |
| IO-04 | Passive vehicle CAN interface, including boot/power loss | No transmitted dominant frames; acceptable bus loading and no unintended termination |
| IO-05 | Malformed, duplicate, delayed and expired local requests | Reject/reason logged; no unintended output transitions |
| IO-06 | Simultaneous selector and computer requests | Deterministic approved priority, with command/feedback agreement |
| IO-07 | One camera short/unplug/frozen-frame event | Remaining channels continue; distinct and timely fault reporting |
| IO-08 | Max configured camera rate plus display previews | No silent frame loss; measured latency, temperature and storage headroom |
| IO-09 | Lighting load switching at worst installed harness length | No compute reset, false ignition edges or corrupted media |
| IO-10 | Harness vibration, moisture and connector temperature tests | Selected installation envelope met; no intermittent contacts or overheating |
| IO-11 | Windows and Vision Core failures separately | Claimed recording, physical-lighting and auxiliary-display independence demonstrated |

All test voltage/current/temperature limits must come from the final selected parts and installation specification. Bench fault injection precedes any live vehicle connection. This package specifies evidence to collect; it does not claim compliance or completed tests.
