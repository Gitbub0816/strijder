# Installation and service concept

## Installation package

Every supported vehicle configuration needs a controlled installation package containing:

- supported make/model/year/upfit scope;
- assembly and harness part numbers/revisions;
- mounting drawings and fastener specifications;
- power source, grounding/bonding, fuse, and wire schedule;
- connector/cavity tables and routing diagrams;
- camera positions, fields of view, and calibration targets;
- antenna placement and separation requirements;
- airbag, visibility, heat, water, and moving-component exclusions;
- lighting-controller/interlock integration and test matrix;
- software/configuration versions;
- commissioning checklist and acceptance record;
- removal/restoration instructions.

Generic “12 V vehicle” installation instructions are insufficient.

## Proposed installation sequence

1. Verify vehicle identity, supported configuration, and installation kit revision.
2. Disconnect/isolate power according to vehicle/upfitter procedure.
3. Inspect planned mount, harness, antenna, and camera routes.
4. Install core, power/UPS, I/O, displays, controls, and cameras.
5. Route, protect, label, and strain-relieve harness branches.
6. Verify every connector and cavity before applying power.
7. Measure ground/bond integrity and check for shorts.
8. Apply protected bench/vehicle power with current limiting where procedure permits.
9. Provision immutable device/vehicle identity and signed configuration.
10. Calibrate cameras and validate GNSS/radios.
11. Exercise every lighting mode, interlock, fault indication, and safe default.
12. Verify recording, event preservation, playback/export test package, and hard-power recovery.
13. Verify Cadmium connectivity, offline operation, map, routing, statuses, and messaging.
14. Capture installation photos, measurements, serials, versions, and technician authorization.
15. Seal protected compartments and obtain customer acceptance.

## Commissioning acceptance

### Electrical

- key-off and key-on current;
- boot/peak current;
- operating voltage and branch rails;
- UPS source transition and run time;
- shutdown current and completed power-off;
- no compute reset during lighting/radio activity;
- correct fuse and harness identification.

### Recording/evidence

- every installed channel identified and aligned;
- durable recording health matches UI;
- manual/configured event trigger;
- pre/post-event preservation;
- manifest/hash verification;
- export authorization and audit entry;
- recovery after power interruption.

### Vehicle controls

- selector inputs and indicators;
- allowed lighting modes;
- every interlock and denied-state indication;
- controller loss/heartbeat fault;
- open/short-load behavior where diagnostics support it;
- safe key-off/boot/reset state.

### Cadmium/operator

- operator authentication;
- assigned vehicle/unit context;
- dispatch/MDT message exchange;
- call and unit status transitions;
- dark/light map, calls, units, route, maneuver, vehicle animation;
- WAN-loss queue and reconnect;
- no unexplained blank-map state.

## Service model

### Roles

- **Operator:** health check and approved basic troubleshooting only.
- **Fleet technician:** harness/module diagnostics and approved replacement.
- **Evidence administrator:** evidence access and policy-controlled export, not vehicle repair.
- **System administrator:** fleet/configuration/software operations, not automatic evidence access.
- **Manufacturer/depot:** board-level repair, secure reprovisioning, forensic fault analysis.

### Service-state controls

- explicit authorized service session;
- vehicle stationary and other policy preconditions;
- controlled output test modes;
- no unrestricted raw output toggling;
- diagnostic access without routine evidence decryption;
- start/end and material actions journaled;
- automatic timeout and return to safe state.

## Replaceable-unit workflow

1. Confirm fault using health data and harness test procedure.
2. Protect or synchronize evidence according to policy.
3. Enter service state and isolate energy.
4. Replace only the identified field-replaceable unit.
5. Verify connector locks, seals, harness routing, and fasteners.
6. Provision/authorize replacement identity.
7. Run subsystem plus regression acceptance tests.
8. Record old/new serials, reason, technician, time, software/configuration, and result.
9. Return failed secure components through controlled handling.

## Diagnostic principles

- distinguish absent power, invalid rail, communications fault, configuration mismatch, and device failure;
- expose raw measurements to authorized technicians without making operators interpret electronics;
- preserve reset reason and last-known fault across reboot;
- identify stale telemetry;
- never recommend bypassing an interlock as a troubleshooting step;
- prevent a disconnected camera or failed SSD from appearing healthy.

## Maintenance schedule placeholders

Final intervals require environmental and reliability data. The service program should cover:

- daily/shift automated self-test;
- periodic camera cleanliness/alignment check;
- harness, mount, connector, and antenna inspection;
- UPS health/capacity test;
- storage-life review;
- software/configuration compliance;
- evidence export verifier test;
- lighting/interlock functional test;
- security certificate/key lifecycle;
- end-of-support and decommissioning.

## Decommissioning

- remove vehicle/fleet assignment;
- revoke device credentials;
- preserve/export evidence under policy;
- perform verifiable secure erase or destroy protected storage;
- render backup pack safe and route it through approved recycling;
- remove equipment and restore vehicle wiring/mounts;
- document final state, serials, custody, and disposal.
