# Engineering roadmap

This roadmap converts the recovered vision into decision gates. Dates are intentionally omitted until staffing, funding, and target-customer commitments are known.

## Phase 1: baseline decisions

- select first customer profile, jurisdiction, and vehicle platform;
- freeze product names and resolve gold/white versus copper/violet brand direction;
- approve functional requirements and prohibited actions;
- decide Vision versus Vision Pro feature boundaries;
- select proof-only versus production Cadmium backend goals;
- complete hazard analysis, threat model, and standards applicability review.

**Exit:** approved product requirements, operational scenarios, hazard register, and architecture decision record.

## Phase 2: electrical and compute proof

- benchmark candidate NVIDIA modules for simultaneous capture/encode/inference;
- benchmark candidate Windows compute/display;
- select preliminary cameras, links, and storage;
- measure actual steady, peak, boot, radio, and display loads;
- freeze vehicle input range and UPS behavior;
- prototype deterministic I/O controller and simulated lighting power module;
- test power loss and evidence finalization.

**Exit:** measured power/thermal budget, selected development hardware, passing bench safety boundaries.

## Phase 3: interface and harness freeze

- resolve Generation A versus Generation B connector implementation;
- choose every connector/contact and camera link;
- produce cavity-level interface-control drawings;
- define grounding, shielding, fusing, wire gauges, and harness construction;
- complete enclosure and mount design;
- run pre-compliance electrical, vibration, thermal, ingress, and EMC tests.

**Exit:** controlled hardware drawings, harness prototype, verified margins.

## Phase 4: platform software alpha

- implement Linux supervisor, camera manager, recorder, event/evidence service, policy, health, and sync queue;
- implement I/O firmware with named modes, watchdog, interlocks, and safe boot;
- implement authenticated Vision local API;
- implement secure provisioning and signed update proof;
- build independent evidence verifier.

**Exit:** end-to-end capture, preserve, seal, export, and verify on bench hardware; I/O remains safe through injected failures.

## Phase 5: Cadmium alpha

- create the five-project .NET 8 WPF solution;
- separate Dispatch and MDT executables;
- implement SQLite/EF Core persistence and migrations;
- implement shared WebView2/Mapbox bridge and explicit map errors;
- implement calls, units, assignments, messages, statuses, route, and offline queue;
- define and build the production synchronization service or controlled simulator.

**Exit:** two-station Dispatch/MDT scenario works through disconnection, restart, catch-up, and conflict tests.

## Phase 6: integrated vehicle prototype

- install into representative nonoperational/test vehicle;
- commission cameras, power, radios, displays, I/O, and lighting-controller simulator/vendor system;
- run ignition, crank, thermal, parked, WAN-loss, and fault scenarios;
- conduct human-factors review;
- verify service replacement and decommissioning.

**Exit:** vehicle-level requirements and hazard mitigations demonstrated with traceable evidence.

## Phase 7: qualification and controlled pilot

- independent cybersecurity assessment;
- selected environmental, EMC, electrical, radio, and battery qualification;
- customer policy/CJIS/privacy/legal review as applicable;
- manufacturing test, provisioning, traceability, update, and support readiness;
- limited pilot with stop criteria and rollback plan.

**Exit:** approved pilot report and explicit production/no-production decision.

## Work intentionally deferred

- speculative recognition or surveillance features without legal/product approval;
- body-camera product scope;
- unrestricted vehicle-network writes;
- automated vehicle actuation;
- generalized consumer-market installation;
- production claims before qualification.
