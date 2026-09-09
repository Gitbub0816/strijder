# Safety, compliance, and validation plan

## Status

This is an applicability and verification plan, not a declaration of compliance. The applicable obligations depend on the first jurisdiction, customer, vehicle class, installation location, radio configuration, handled data, and procurement contract.

## Safety architecture principles

1. High-level Linux, Windows, CAD, cloud, and computer-vision functions do not directly switch high-current warning equipment.
2. Physical outputs are mediated by a deterministic I/O controller with safe defaults, watchdog behavior, and local interlocks.
3. Recording/evidence, operator/CAD, vehicle I/O, and cloud are separate failure domains.
4. Loss of WAN or cloud does not disable local recording, authentication, or safe I/O behavior.
5. The system never presents a healthy/recording indication when the required durable operation is failing.
6. Driver-facing interactions are limited, glanceable, and constrained by vehicle state and agency policy.
7. Updates are authenticated, staged, rollback-capable, and prohibited in unsafe operating states.

## Preliminary hazard register

| Hazard | Example cause | Potential effect | Baseline mitigation | Verification |
|---|---|---|---|---|
| Uncommanded light output | Software defect, stale/replayed request, wiring short | Unsafe signaling/confusion | Separate I/O controller, freshness/auth, interlocks, protected outputs, feedback | Fault injection and state-table tests |
| Failure to activate requested mode | Open wire, controller fault, low voltage | Reduced warning visibility | Output diagnostics, feedback, operator fault, independent vendor controller behavior | Open-load/low-voltage tests |
| Driver distraction | Dense UI, alerts, video interaction | Collision risk | Glanceable layout, lockouts, physical controls, alert prioritization | Human-factors/road simulation |
| Loss of evidence | Storage/power/camera failure | Missing incident record | Health monitoring, UPS, channel isolation, explicit recording state | Power-cut, storage-endurance, camera-loss tests |
| False evidence integrity | UI claims success before durable seal | Evidentiary challenge | Transactional event state, manifest verification, no false-success UI | Crash/recovery and independent verification |
| Vehicle battery depletion | Parked recording or failed shutdown | No-start condition | Ignition policy, voltage thresholds, load shedding, UPS isolation | Parked-current and shutdown testing |
| Thermal event | Compute/charger/battery heat | Damage or fire | Thermal sensing, qualified pack/BMS, power limiting, containment | Worst-case thermal/fault testing |
| Vehicle-network interference | Improper CAN termination/write | Vehicle fault | Protected gateway, read-only default, interface validation | Bus-load/error-injection tests |
| Unauthorized remote access | Credential or service compromise | Surveillance, evidence/control misuse | Mutual auth, least privilege, audited remote features, no default shell | Penetration and authorization testing |
| Incorrect CAD state | Lost/out-of-order updates | Dispatch confusion | Durable events, revisions, idempotency, stale-state indicators | Offline/reconnect/partition tests |
| Mount or harness failure | Vibration, impact, chafe | Injury, short, system loss | Vehicle-specific mounts, strain relief, protection, inspection | Mechanical/environmental testing |

## Candidate standards and policies for applicability review

### Vehicle electrical and environmental

- SAE J1455 environmental practices for heavy-duty vehicle electronic equipment may provide an environmental test framework depending on vehicle/application. [SAE overview](https://www.sae.org/)
- ISO 16750-2 addresses electrical loads for road-vehicle electrical/electronic equipment by mounting/application context. [ISO overview](https://www.iso.org/)
- ISO 7637 series should be reviewed for conducted/transient disturbances on vehicle supply and signal lines.
- CISPR 25 and ISO 11452 series should be reviewed for emissions and immunity.
- ISO 20653 or an equivalent ingress classification should be selected by installation zone.
- ISO/SAE 21434 should be reviewed for road-vehicle cybersecurity engineering applicability.
- ISO 26262 applicability should be assessed if any function can affect vehicle safety; even where not formally applicable, a structured hazard analysis is warranted.

### Radio and positioning

- Cellular, Wi-Fi, Bluetooth, and other intentional radiators require region-appropriate equipment authorization and integration review. The FCC maintains the U.S. equipment-authorization framework. [FCC](https://www.fcc.gov/engineering-technology/laboratory-division/general/equipment-authorization)
- Certified radio modules do not automatically certify the complete host, antenna, cabling, labeling, or simultaneous-transmission configuration.

### Battery and shipping

- Final cell/pack safety standards depend on chemistry, installation, charger, and market.
- Shipping the lithium battery requires dangerous-goods and test-summary review, including UN 38.3 applicability.
- The pack needs a qualified BMS, electrical/thermal protection, mounting, service procedure, and end-of-life strategy.

### Public-safety information

- If Cadmium or evidence services handle Criminal Justice Information, the current FBI CJIS Security Policy and agency-specific implementation rules require formal review. [FBI CJIS resources](https://le.fbi.gov/cjis-division/cjis-security-policy-resource-center)
- CAD integration with emergency communications, NCIC/state systems, 911/PSAP infrastructure, or records systems requires separate interface, accreditation, and operational review.
- FIPS-validated cryptography may be contractually or regulatorily required; applicability is not decided here.

### Emergency warning equipment and installation

- Warning-light colors, flash patterns, siren behavior, switching, interlocks, and authorization vary by jurisdiction and vehicle type.
- Installation must be reviewed against vehicle manufacturer guidance, upfitter manuals, airbag zones, visibility requirements, electrical capacity, and customer policy.
- Compliance of a vendor lightbar/controller does not automatically cover a custom control integration.

### Evidence, privacy, and labor

- Audio recording, live location, remote access, retention, disclosure, public-records handling, biometric authentication, and employee monitoring vary by jurisdiction and customer policy.
- Evidence policy must define preservation, legal hold, export, access, redaction, disclosure, and deletion.

## Validation program

### Phase 0: requirements and analysis

- identify first customer, jurisdiction, vehicle, and upfitter;
- freeze use cases and prohibited actions;
- produce system hazard analysis and threat model;
- define operational design domain and degraded modes;
- select applicable standards with qualified counsel/labs;
- approve interface-control and power-budget baselines.

### Phase 1: bench engineering

- power input, reverse polarity, inrush, brownout, overvoltage, transient, and shutdown;
- steady/peak power measurements for every mode;
- camera link, synchronization, image-quality, and channel-loss tests;
- storage endurance, corruption, and power-cut recovery;
- I/O state-machine, watchdog, feedback, and fault injection;
- radio coexistence and preliminary emissions;
- thermal characterization and load shedding;
- cryptographic/evidence manifest verification;
- offline/reconnect and queue idempotency.

### Phase 2: hardware-in-loop and vehicle

- representative vehicle harness and network simulator;
- ignition/crank/load scenarios;
- external lighting controller and interlock simulation;
- GNSS/cellular loss and degraded conditions;
- day/night display and driver-interaction study;
- camera alignment, vibration, and moving-scene tests;
- parked operation and battery-depletion protection;
- installation/service time and error-proofing.

### Phase 3: environmental and security qualification

- selected temperature, vibration, mechanical shock, ingress, fluid, corrosion, EMC, ESD, and electrical-transient tests;
- independent penetration test;
- secure boot/update/rollback and key-management exercises;
- evidence tamper/truncation/reordering tests;
- radio/certification testing;
- battery safety and transport documentation.

### Phase 4: controlled pilot

- limited vehicles, trained operators, rollback plan, and daily health review;
- shadow-mode CAD/evidence integration before operational reliance;
- documented incident/escalation channel;
- quantitative success and stop criteria;
- change freeze for safety-relevant controller behavior during pilot.

## Release gates

No operational release should occur until:

- requirements and hazards are approved;
- all physical interfaces have controlled drawings;
- final power/thermal budgets are measured;
- degraded modes and operator indicators are verified;
- evidence integrity can be independently verified;
- cybersecurity findings are closed or formally accepted;
- installation instructions and vehicle approvals exist;
- compliance applicability is reviewed by qualified parties;
- manufacturing test, serialization, provisioning, and traceability are operational;
- incident response, update, rollback, and support processes are staffed.
