# Preliminary bill of materials

## BOM policy

This is an architecture BOM, not a purchasing BOM. An exact manufacturer part number appears only where prior design work identified a connector family. All other entries specify selection requirements and remain TBD.

Quantities are per equipped vehicle unless noted.

## Compute, storage, and control

| Qty | Assembly | Minimum role/specification | Selection status |
|---:|---|---|---|
| 1 | NVIDIA compute module | Linux-capable embedded AI/video compute with sufficient camera ingest/encode, secure boot support, industrial lifecycle preferred. | Exact SKU TBD |
| 1 | Vision carrier board | Power sequencing, module I/O, storage, camera interfaces, Ethernet/USB as required, hardware identity. | Custom/TBD |
| 1 | Windows MDT compute | Runs .NET 8 WPF Cadmium MDT and WebView2/Mapbox; may be display-integrated. | Form factor/SKU TBD |
| 1 | Vehicle I/O MCU | Deterministic controller with watchdog, protected vehicle I/O, authenticated update, safe boot defaults. | MCU/SKU TBD |
| 1 | High-endurance SSD | Encrypted local recording/evidence storage with health telemetry and power-loss behavior appropriate to workload. | Capacity/endurance/SKU TBD |
| 1 | Secure key device | Hardware-protected device identity and key operations. | TPM/secure element TBD |
| 1 | Service/debug interface | Authenticated, physically controlled manufacturing/service access. | Connector/protocol TBD |

## Cameras, displays, audio, and controls

| Qty | Assembly | Minimum role/specification | Selection status |
|---:|---|---|---|
| 1 | Main dashcam head | Primary forward HDR capture, status/event interface, rugged mounting. | Sensor/lens/enclosure TBD |
| 0–3 | Auxiliary cameras | Rear/side/other views; sealed automotive link; independently diagnosable. | Optional; TBD |
| 1 | Primary CAD/operator display | Rugged touch display, day/night readability, mounting and thermal design for vehicle use. | Size/luminance/SKU TBD |
| 0–1 | Auxiliary-camera display | Low-latency selected camera view. | Optional; TBD |
| 1+ | Microphone/audio front end | Policy-controlled audio capture with clear channel identity. | Count/placement TBD |
| 1 | Lighting selector | Tactile or otherwise glanceable physical mode selection and indicators. | Mechanical/electrical design TBD |
| 0–1 | Manual event control | Clearly identifiable evidence-event mark input. | Could be integrated; TBD |
| 1 | Operator validator | NFC/keycode/other local validation interface as policy permits. | Exact modality/SKU TBD |

## Communications and positioning

| Qty | Assembly | Minimum role/specification | Selection status |
|---:|---|---|---|
| 1 | Cellular modem | Fleet-grade WAN connectivity; carrier and regional approvals required. | Modem/SIM/eSIM TBD |
| 1 | LTE antenna interface | Early concept used SMA. Diversity/MIMO needs final RF architecture. | Family partly established, SKU TBD |
| 1 | GNSS receiver/antenna | Vehicle positioning and trustworthy time input with fix-quality reporting. | TBD |
| 1 | Wi-Fi/Bluetooth radio | Local provisioning, approved peripherals, depot transfer where enabled. | TBD |
| 0–1 | Dedicated vehicle Ethernet switch | Only if selected cameras/displays require it; managed and automotive-rated preferred. | Optional/TBD |

## Vehicle and warning-light I/O

| Qty | Assembly | Minimum role/specification | Selection status |
|---:|---|---|---|
| 1 | Protected CAN/OBD gateway | Isolated/protected transceiver path; read-only by default. | Protocol/count TBD |
| 1 | Input protection bank | Automotive transient/ESD protection and conditioning for ignition, interlocks, auxiliary inputs. | Custom/TBD |
| 1 | Output driver bank | Protected low-side/high-side or external-module control with diagnostics. | Custom/TBD |
| 1 | Lighting power controller | Independently fused high-current switching or approved vendor controller. | Must be separate from compute interconnect; TBD |
| 1 | Interlock interface | Protected inputs/outputs with deterministic behavior. | Custom/TBD |
| 1 | Vehicle harness set | Keyed, labeled, protected, serviceable harnesses. | Final ICD required |

## Power and thermal

| Qty | Assembly | Minimum role/specification | Selection status |
|---:|---|---|---|
| 1 | Vehicle power front end | Reverse-polarity, surge/transient, inrush, filtering, protected switching. | Topology/components TBD |
| 1 | Main DC/DC stage | Supports measured load over final vehicle input and temperature range. | Voltage/current/SKU TBD |
| 1 | UPS power-path/BMS | Seamless hold-up and controlled shutdown telemetry. | Architecture TBD |
| 1 | Backup pack | Planning example 12.8 V, 6 Ah LiFePO4 (~77 Wh nominal); 50–60 Wh usable target. | Not production-selected |
| 1 set | Branch protection | Per-load fuses/e-fuses/current limits and telemetry. | Ratings TBD |
| 1 | Thermal solution | Passive plate/heat spreader or controlled fan as testing requires. | TBD |
| N | Temperature sensors | Compute, storage, power, pack, and enclosure monitoring. | TBD |

## Connector and harness families

### Early rugged connector concept

| Qty | Label | Family |
|---:|---|---|
| 1 | Main power | DEUTSCH DT, 6 position |
| 1 | General data | DEUTSCH DTM, 12 position |
| 1 | Main head | DEUTSCH HDP20, 20 position |
| 1 | Interlock | DEUTSCH DTM, 6 position |
| 2 | `Val1`/`Val2` | DEUTSCH DTM, 4 position |
| 4 | Camera links | FAKRA/mini-FAKRA concept |
| 1 | LTE antenna | SMA concept |

### Later functional connector allocation

| Qty | Interface | Positions |
|---:|---|---:|
| 1 | Vehicle Power | 5 |
| 1 | Validator | 6 |
| 1 | CAN/OBD/Sense | 6 |
| 1 | Auxiliary Sensor | 3 |
| 1 | Interlock Actuator | 4 |
| 1 | Lighting Controller | 16 |
| 1 | Lighting Selector | 16 |
| 1 | Main Dashcam Head | 20 |
| 1 | CAD/Windows Display | 40 |
| 1 | Auxiliary Camera Display | 8 |

## Enclosures and installation

| Qty | Assembly | Requirement | Status |
|---:|---|---|---|
| 1 | Core enclosure | Rugged, tamper-evident, thermally managed, serviceable, labeled. | Material/IP/mount TBD |
| 1 | Power/UPS enclosure | Electrical and battery fault containment with protected service access. | TBD |
| 1 | I/O enclosure | Close to controlled harnesses while isolated from heat/noise as required. | TBD |
| 1 set | Vehicle mounts | Crash-aware and vibration-tested; must not obstruct airbags or visibility. | Vehicle-specific/TBD |
| 1 set | Tamper seals/labels | Assembly identity and evidence/service indication. | TBD |

## Cost status

No defensible production BOM price was recovered. Pricing must follow part selection, expected annual volume, nonrecurring engineering, tooling, certification, contract manufacturing, cloud/evidence costs, warranty reserve, installation labor, and spares strategy.
