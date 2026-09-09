# Decision register and open questions

## Established decisions

| ID | Decision | Status |
|---|---|---|
| D-001 | Sights is unrelated to Strijder and excluded from this architecture. | Established |
| D-002 | Strijder Vision is the in-vehicle platform; Cadmium is CAD only. | Established |
| D-003 | Vision Pro EVS performs heavy embedded processing on NVIDIA-class Linux hardware. | Established |
| D-004 | The embedded processing layer operates behind the scenes; it is not the operator's ordinary desktop UI. | Established |
| D-005 | Cadmium provides separate Dispatch Console and in-vehicle MDT responsibilities. | Established |
| D-006 | Cadmium proof architecture is .NET 8 WPF with WebView2 and Mapbox. | Established |
| D-007 | The vehicle platform is offline capable and continues core local functions without cloud connectivity. | Established |
| D-008 | Evidence features include journaling, retention controls, tamper-evident hashes, encrypted exports, audit trails, and role-based export approval. | Established concept |
| D-009 | Vehicle profile authentication can be local using biometrics, NFC, or keycode. | Established concept |
| D-010 | Approximately 75 W is the initial system planning load. | Established planning value |
| D-011 | A prototype UPS should provide roughly 50–60 Wh usable; 75–100 Wh was considered for margin. | Established planning range |
| D-012 | Actual emergency-light load current must not traverse the compute/peripheral interconnect. | Current engineering boundary |
| D-013 | PlantUML is the canonical diagram source; rendering uses the public PlantUML server. | Established repository rule |

## Superseded or competing concepts

| ID | Earlier concept | Later/evolved concept | Resolution |
|---|---|---|---|
| H-001 | Eleven external connectors: DT6 Power, DTM12 Data, HDP20 Main Head, SMA LTE, DTM6 Interlock, two DTM4 validator/valve connections, and four FAKRA cameras. | Ten functional connector groups: Vehicle Power, Validator, CAN/OBD/Sense, Aux Sensor, Interlock Actuator, Lighting Controller, Lighting Selector, Main Dashcam Head, CAD/Windows Display, Aux Camera Display. | Preserve both. Final harness architecture TBD. |
| B-001 | Existing gold/white logo and gold/silver site. | Later hard-lock: dimensional S/triangle, copper-to-violet liquid metal/glass on black, forward tilt, no shield/sword. | Brand owner decision required. |
| C-001 | One WPF executable with switchable dispatch/in-vehicle proof modes. | Separate Dispatch and MDT executables sharing libraries and services. | Proof remains historical; production target is separated applications. |

## Open engineering decisions

| ID | Question | Why it matters | Closure evidence |
|---|---|---|---|
| O-001 | Which NVIDIA compute module and lifecycle grade? | Performance, thermals, availability, camera lanes, cost. | Benchmarks plus lifecycle/vendor review. |
| O-002 | Is the Windows MDT compute integrated into the display or separate? | Power, harness, cooling, serviceability. | Mechanical/electrical architecture review. |
| O-003 | What cameras and transport are used? | Image quality, PoC, cable length, synchronization, evidence volume. | Sensor/lens/serializer trade study and road tests. |
| O-004 | Which later connector family and exact contacts? | Pin ratings, sealing, keying, repair tooling. | Approved interface-control drawing. |
| O-005 | What is the minimum operating voltage and cranking behavior? | Determines current, converter sizing, hold-up, reset behavior. | Vehicle transient profile and power tests. |
| O-006 | Which loads are included in the 75 W budget? | Determines fusing, contacts, wiring, UPS. | Measured subsystem power budget. |
| O-007 | Does camera power use PoC? | Changes power-pin count and camera-fault isolation. | Camera/link selection. |
| O-008 | What warning-light vendors and protocols are in scope? | Output hardware and certification vary significantly. | Integration matrix and agency requirements. |
| O-009 | What actions may Cadmium request from vehicle controls? | Safety and cybersecurity boundary. | Approved command authorization matrix. |
| O-010 | What evidence retention and export policies apply by customer? | Storage capacity and compliance. | Policy profiles and legal review. |
| O-011 | What cloud/control-plane deployment is selected? | Tenancy, availability, cost, sovereignty. | Architecture decision record. |
| O-012 | What standards and procurement regimes apply to the first target customer? | Defines validation and documentation obligations. | Target-market and jurisdiction decision. |
