# Source-backed specification and recovery register

Status: **engineering reconstruction, not production release**. Prepared 2026-09-09.

## 1. What was actually recovered in this revision

The original repository, the September 2026 dossier, and the conversation visible during this revision were inspected. A targeted search for older Strijder hardware conversations was attempted, but the personal-context service returned **“Personal context is unavailable for this conversation.”** Consequently, this revision does not claim to have independently recovered November 2025–August 2026 transcripts, original electrical drawings, an approved purchasing BOM, or a component-level netlist.

This limitation does not prevent useful engineering inference. It does require maintaining a distinction between requirements visible in user messages, promises present in an original artifact, historical summaries authored by an assistant, and newly proposed engineering implementation.

The existing dossier uses the word **Established** for both repository evidence and reported historical decisions. For the engineering package, use the more specific evidence classes below; the older label alone is not proof of owner approval or hardware validation.

| Class | Meaning | Permitted use |
|---|---|---|
| U | Explicit user statement visible in the current conversation | Product-scope requirement; do not extend it beyond what was said. |
| R | Content verified in the original repository artifact | Historical product requirement/promise, not evidence of implementation or testing. |
| H | Historical claim in the September dossier or earlier assistant response, without underlying transcript recovered this turn | Preserve as a candidate design baseline and confirm before release. |
| P | Engineering inference or proposal authored to make the concept reviewable | Analyze and draw as a proposal; never attribute it to an old user decision. |
| V | Verified measurement, released schematic, vendor-approved interface, or completed qualification result | No electrical design item in this revision has this status. |

## 2. Evidence locations and dates

| ID | Source | Date and limits |
|---|---|---|
| SRC-U1 | Visible user correction: “Strijder vision is the in-vehicle computing and dashcam and light controls” followed by “Plus CaD. Not car.” | Visible in the current conversation; exact original message timestamp is not exposed. |
| SRC-U2 | User request to document scope, design, architecture, BOMs and diagrams in this repository, and latest request for schematics in `docs/engineering` | Current work scope; permission to infer does not convert inference into recovered history. |
| SRC-R1 | [Original website](../../index.html), introduced in [commit 5515f375c18d28d14b8d2e7d92634ea6c3ebc6cd](https://github.com/Gitbub0816/strijder/commit/5515f375c18d28d14b8d2e7d92634ea6c3ebc6cd) | Git author timestamp 2025-11-07T12:52:24-06:00. This establishes the artifact's recorded commit date, not dates of all design discussions. |
| SRC-H1 | [September dossier](../README.md), [commit f6d5ff2aafc808f38bb2daf654e476a2e7590bbc](https://github.com/Gitbub0816/strijder/commit/f6d5ff2aafc808f38bb2daf654e476a2e7590bbc) | Git author timestamp 2026-09-08T17:20:55-07:00. Contains retrospective claims; original messages are not bundled. |
| SRC-H2 | [Historical timeline](../product/HISTORY_AND_BRAND.md), [hardware architecture](../hardware/HARDWARE_ARCHITECTURE.md), [connectors](../hardware/CONNECTORS_AND_HARNESS.md), [power](../hardware/POWER_ARCHITECTURE.md), [BOM](../hardware/BOM.md) | Same retrospective dossier. A month in the timeline is a historical assertion, not a independently verified message timestamp. |
| SRC-H3 | Earlier assistant responses visible in the current conversation | Useful record of prior suggestions and summaries, but not independent evidence of the older conversation they describe. |

## 3. Directly supported top-level requirements

| Requirement ID | Requirement or product promise | Class/source | Engineering consequence (inference) |
|---|---|---|---|
| REC-001 | Strijder Vision combines in-vehicle computing, dashcam, lighting controls and CAD. | U / SRC-U1 | Provide separately identifiable compute, media, vehicle-control and dispatch interfaces. |
| REC-002 | Strijder is distinct from Sights. | U / SRC-U1 and preceding explicit correction | Do not import pedestrian route recording, accessibility navigation or Sights architecture as Strijder requirements. |
| REC-003 | On-device security, diagnostics and dashcam evidence must work without cloud connectivity. | R / SRC-R1 hero and feature sections | Local storage, local policy and disconnected operation must be possible; cloud cannot be the sole authorization dependency. |
| REC-004 | High-dynamic-range recording, tamper-evident hashes and role-based export approvals. | R / SRC-R1 “Secure Dashcam” | Define capture pipeline, media integrity records and authorization-controlled export; HDR sensor choice and cryptography remain open. |
| REC-005 | Read CAN/OBD where applicable, with configurable policies and silent evidence capture. | R / SRC-R1 “Diagnostics + Alerts” | Document vehicle compatibility and acquisition constraints; this does not authorize arbitrary CAN transmit or vehicle actuation. |
| REC-006 | Local validation via biometrics/NFC/keycode, with fleet profile keys securely stored on device. | R / SRC-R1 “Offline-First Auth” | Support a local validator abstraction and protected credentials; all three modalities are not automatically mandatory in every SKU. |
| REC-007 | Signed profiles and vehicle keys, local policy enforcement, optional cloud admin console. | R / SRC-R1 “Security” | Separate policy authorization from connectivity, and define key provisioning/revocation. |
| REC-008 | Event journaling, retention controls, encrypted exports with audit trail and automated incident packages. | R / SRC-R1 “Evidence” | Define retention state, export transaction integrity, incident identity and audit persistence. |
| REC-009 | Engineering documents and schematic definitions belong in `docs/engineering`; diagrams should use editable PlantUML and rendered assets. | U / SRC-U2 and preceding diagram request | Preserve diagram sources, link rendered outputs and label proposed electrical architecture. |

These are design requirements or website promises. The static website does not establish that any firmware, hardware, CAD system or security control has been implemented.

## 4. Historical hardware baseline awaiting transcript or owner confirmation

| Item | Retained specification | Class/source | Release constraint |
|---|---|---|---|
| Product hierarchy | Strijder → Vision → Vision Pro EVS; Cadmium is the CAD subsystem. | H / SRC-H1, SRC-H3 | User confirms CAD is included, but detailed naming/hierarchy needs source-level confirmation. |
| Vision compute | NVIDIA-class embedded processing running Linux, normally headless. | H / SRC-H2; timeline attributes this to May 2026 | No exact NVIDIA SKU, carrier, RAM or compute performance requirement recovered. |
| Operator/CAD compute | Separate Windows/operator environment where appropriate. Cadmium proof described as .NET 8 WPF with WebView2 and Mapbox. | H / SRC-H1 | No released MDT motherboard, display link or Windows power budget. |
| Recording storage | Local solid-state recording/evidence storage. | H / SRC-H1 | Capacity, write endurance, retention, removable/fixed packaging and power-loss protection are open. |
| Camera topology | Early panel lists four FAKRA camera ports; main head and optional auxiliary cameras also described. | H / SRC-H2 | Four ports do not settle whether the main head is one of four or an additional camera. Do not silently design five capture channels. |
| Main display | Primary CAD/Windows display; later connector inventory gives 40 positions. | H / SRC-H2 | Connector position count does not establish native video protocol, size, resolution, brightness or integrated compute. |
| Auxiliary display | Optional selected-camera display; later connector inventory gives eight positions. | H / SRC-H2 | Video transport, latency and power demand remain open. |
| Radios | Cellular, Wi-Fi, Bluetooth and GNSS/GPS; early LTE port labeled SMA. | H / SRC-H1, SRC-H2 | Modem, carriers, antenna count, MIMO/diversity and RF coexistence not selected. |
| Vehicle I/O | Validator, CAN/OBD/sense, auxiliary sensor, interlock actuator, lighting controller and lighting selector. | H / SRC-H2 | Electrical classes, signal directions, safety function and device compatibility remain open. |
| Power envelope | Approximately 75 W initial planning load. | H / SRC-H2; timeline attributes planning to August 2026 | Not a measured load, not a certified maximum, and not a valid fuse or contact rating on its own. |
| Hold-up | Approximately 20 minutes; 25 Wh ideal at 75 W; 50–60 Wh usable and 75–100 Wh nominal were planning envelopes. | H / SRC-H2 | Which loads remain on during hold-up is unresolved. Usable energy must be measured at worst-case temperature, age and load. |
| Backup example | 12.8 V, 6 Ah LiFePO4, 76.8 Wh nominal. | H / SRC-H2 | Example only, not a selected pack, BMS, charging profile or approved battery assembly. |
| Peripheral power contacts | 11 positive contacts plus 11 returns across nine peripheral groups. | H / SRC-H3, explicitly an earlier assistant allocation | This was a proposal; it must not be represented as an old validated pinout or total system connector requirement. |

## 5. Connector information retained without pretending to have a pinout

### Earlier rugged panel concept

| Label | Retained family/positions | Evidence |
|---|---|---|
| `DT6_Power` | DEUTSCH DT, six positions | H / SRC-H2 |
| `DTM12_Data` | DEUTSCH DTM, 12 positions | H / SRC-H2 |
| `HDP20_MainHead` | DEUTSCH HDP20, 20 positions | H / SRC-H2 |
| `SMA_LTE` | SMA antenna connector | H / SRC-H2 |
| `DTM6_Interlock` | DEUTSCH DTM, six positions | H / SRC-H2 |
| `DTM4_Val1`, `DTM4_Val2` | Two DEUTSCH DTM, four positions each | H / SRC-H2; `Val` meaning explicitly unresolved |
| `FAKRA_Cam1` through `FAKRA_Cam4` | Four FAKRA/mini-FAKRA concept links | H / SRC-H2; connector family does not choose transport or PoC |

### Later functional inventory

| Interface | Retained position count | What the count does not tell us |
|---|---:|---|
| Vehicle Power | 5 | Rail count, wake semantics, fuse rating or number of parallel contacts. |
| Validator | 6 | Modality, protocol or supply voltage. |
| CAN/OBD/Sense | 6 | Bus count, diagnostic protocol, termination or allowed transmit behavior. |
| Auxiliary Sensor | 3 | Analog/digital type, grounding, range or sensor excitation. |
| Interlock Actuator | 4 | Whether this is direct coil drive, control signaling or feedback. |
| Lighting Controller | 16 | Protocol, output ratings or external load power routing. |
| Lighting Selector | 16 | Discrete versus networked control or indicator wiring. |
| Main Dashcam Head | 20 | Camera count, data transport, source of power or capture location. |
| CAD/Windows Display | 40 | Display-only versus integrated MDT, high-speed topology or pin current. |
| Auxiliary Camera Display | 8 | Transport, latency, power or optional control functions. |

All counts in this table are **H / SRC-H2**. They describe an inventory, not a released interface-control drawing. The later “Style A” dimensions—2.00 mm pitch, 15.0 mm board-to-panel spacing, 1.5 mm panel thickness and 2.0 mm shell protrusion—have the same evidence class. No contact metallurgy, mating drawing, impedance specification, sealing or qualified current-versus-temperature curve accompanies them.

The earlier and later inventories are alternatives in design history, not two sets of connectors to add together automatically. Final selection must reconcile their roles and packaging before a harness is ordered.

## 6. Specific numerical claims that must not become engineering guarantees

1. **75 W / 12 V = 6.25 A** is arithmetic for a defined 75 W load at a defined rail. It does not establish all-peripheral consumption, surge demand, conversion loss or low-voltage vehicle input behavior.
2. **75 W / 9 V / 2 = 4.17 A** assumes the 75 W is drawn at that rail and divides perfectly between two contacts. It is not a qualified maximum per pin. If 75 W is downstream output power, input current also depends on conversion efficiency and auxiliary consumption.
3. Two parallel contacts do not guarantee equal current. Contact and wire resistance, temperature and a disconnected branch affect sharing. A production design must either qualify the allowed imbalance/fault case or avoid relying on unverified parallel-contact capacity.
4. A **22-contact peripheral allocation** excludes the main vehicle feed, signal contacts, shields and other connections. Cameras using PoC still have power-carrying coax conductors and return paths; “no extra power pins” does not mean no power-path sizing.
5. The prior **30-contact separate-camera variant** assumes exactly four independently powered cameras. Until the main-head/four-port relationship is settled, even that arithmetic is conditional.
6. **76.8 Wh nominal** is not 76.8 Wh deliverable to the loads. Battery voltage window, BMS limits, conversion efficiency, temperature, aging and reserve policy reduce useful energy.
7. Connector family names and position counts do not provide a purchasing BOM. Full housing, contact, seal, lock and mating-part selections require mechanical and electrical qualification.

## 7. Engineering decisions that can be inferred, but remain proposals

The user explicitly requested inferred engineering documents. The following are justified **P** choices for a reviewable reference architecture, not recovered historical decisions:

- Partition vision processing, operator software, power supervision and deterministic vehicle I/O so a display or operating-system failure does not automatically become a vehicle-control failure.
- Put input protection, monitored power distribution and a supervised backup-power path ahead of the computing loads.
- Use independently protected peripheral branches with defined returns and diagnosable faults.
- Keep emergency-light load power off a small generic computer peripheral connector unless an independently reviewed high-current design explicitly supports it.
- Treat vehicle-network acquisition as non-actuating until an approved vehicle/interface specification grants otherwise.
- Separate evidence recording state from export approval and WAN availability.
- Represent circuit values, part numbers, fuse ratings and exact connector cavities as TBD unless derived from a documented requirement and checked against selected component data.
- Use PlantUML for functional electrical sheets and interface relationships; do not claim those sheets are CAD netlists, PCB layouts or manufacturing schematics.

## 8. Missing information with the highest engineering impact

| Needed decision or artifact | Why it changes the design |
|---|---|
| Exact vehicle voltage class and operating/transient envelope | Governs input protection, converter and capacitor ratings, cable/fuse design and hold-up transition. |
| Compute module and worst-case sustained workload | Governs rails, current, cooling, camera ingest, codecs and battery budget. |
| Main head versus four external camera definition | Governs camera quantity, serializer/deserializer count, lanes, PoC and storage throughput. |
| Camera resolution, frame rate, HDR, codecs and retention | Governs sensor/interface selection, storage capacity/endurance and network export rate. |
| Display specification and location of Windows compute | Governs connector content, data transport, power and thermal design. |
| Lighting vendor/protocol and boundary of Strijder authority | Governs I/O circuitry, independent controls, isolation, failure behavior and validation. |
| Interlock function and safe states | Governs whether any actuator is permitted, feedback requirements and hazard analysis. |
| Approved per-port loads and output rail voltages | Governs contact count, cable gauge, branch protection and supply sizing. |
| Confirmed connector mechanical/electrical drawings | Governs footprints, cavities, creepage/clearance, impedance, sealing and harness tooling. |
| Hold-up load-shedding policy and battery environment | Governs chemistry/pack/BMS/charger choice and measured usable energy. |
| Original BOM, CAD files, transcripts or dated owner approvals | Allows H candidates to be resolved without creating false certainty. |

## 9. Promotion and change-control rule

A candidate specification is promoted only when its source is recorded: an explicit owner requirement, a dated original design artifact, or a completed engineering selection/verification record. Record the source, revision, decision owner and any affected schematic sheets. If new evidence conflicts with this register, retain the superseded claim and the reason for the change; do not silently overwrite historical uncertainty.

Until those gates are met, this package is suitable for architecture review, requirements reconciliation and planning the next design phase—not PCB fabrication, purchasing a production harness, installing vehicle actuators or claiming safety/compliance certification.
