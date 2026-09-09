# System architecture

## Architectural shape

Strijder Vision is a distributed vehicle system, not one monolithic computer. The reference architecture uses four fault-containment domains:

1. **Vision Core** — embedded NVIDIA/Linux compute for camera ingest, encoding, computer-vision processing, evidence services, telemetry, and synchronization.
2. **Vehicle I/O controller** — deterministic microcontroller domain for sensing, watchdogs, interlocks, and permitted warning-light control outputs.
3. **Operator/Cadmium domain** — Windows-based display/compute running the Cadmium MDT and approved vehicle UI.
4. **Remote services** — Cadmium Dispatch Console and optional fleet/evidence administration services.

![Functional hardware blocks](https://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/Gitbub0816/strijder/main/docs/diagrams/hardware-blocks.puml)

## Fault-containment domains

| Domain | Owns | Must not own |
|---|---|---|
| Vision Core | Camera capture, encoding, ring buffer, evidence packaging, telemetry, computer vision, synchronization orchestration. | Direct high-current warning-light switching; unrestricted safety-critical CAN writes. |
| Vehicle I/O | Physical switch inputs, approved outputs, watchdog, interlocks, voltage/ignition state, safe defaults. | Evidence custody, CAD business logic, general-purpose UI. |
| Windows/MDT | Operator interaction, Cadmium workflow, maps, messages, camera presentation, authorized requests. | Unmediated physical outputs; sole custody of evidence. |
| Cloud/dispatch | Call coordination, fleet policy distribution, remote health, approved evidence intake and administration. | Required dependency for local recording or safe vehicle control. |

## Vision Core services

The Linux compute layer is headless infrastructure. Proposed service boundaries are:

| Service | Responsibility |
|---|---|
| Device supervisor | Starts services, monitors health, coordinates restart and degraded mode. |
| Camera manager | Discovers camera links, configures streams, monitors loss, timestamps frames. |
| Recorder | Encodes streams and writes bounded recording segments. |
| Event manager | Converts triggers into evidence windows and pins relevant segments. |
| Evidence service | Encrypts, hashes, manifests, journals, and exposes controlled exports. |
| Vision inference | Runs approved perception models and emits attributed observations. |
| Vehicle gateway | Normalizes read-only diagnostics and exchanges authenticated messages with the I/O controller. |
| Identity/policy agent | Validates device identity and signed fleet policy. |
| Sync agent | Queues and resumes telemetry, policy, software, and evidence transfers. |
| Health agent | Reports camera, storage, thermal, power, radio, GPS, I/O, and service health. |
| Local API gateway | Authenticated, versioned interface to the Windows/MDT domain. |

These boundaries are proposed; no container runtime or process manager has been finalized.

## Vehicle I/O controller

The I/O controller is proposed as a separate safety-oriented MCU rather than a task inside the Linux computer. It should provide:

- ignition and battery-voltage sensing;
- physical lighting-selector input;
- interlock and auxiliary-sensor inputs;
- external power-module or relay-control outputs;
- output-current/fault feedback where supported;
- an independent watchdog and heartbeat policy;
- boot defaults that leave every controlled output in a documented state;
- authenticated, allow-listed commands from the operator/Vision domains;
- a local event log for state transitions and faults.

The controller should reject stale, malformed, unauthorized, or state-incompatible commands. High-level applications request named modes; they do not directly toggle arbitrary pins.

## Windows operator domain

The recovered design identifies a `CAD/Windows Display` connection. The unresolved hardware choice is whether Windows compute is integrated into the display or installed as a separate serviceable module.

The domain presents:

- Cadmium MDT;
- map and turn-by-turn route guidance;
- call/unit status and messaging;
- camera preview or auxiliary-camera switching;
- concise device/vehicle health;
- authorized evidence-event marking;
- permitted warning-light mode requests.

The Windows UI consumes normalized APIs. It must not mount evidence storage as an ordinary writable volume.

## Remote domains

### Cadmium Dispatch

Dispatch manages calls, units, statuses, messaging, location display, and assignment delivery. Production topology remains TBD; the proof used local shared objects and a WebView2 map.

### Optional fleet/evidence administration

The original site contemplates an optional cloud admin console. Logical responsibilities include:

- fleet and vehicle inventory;
- signed policy and configuration distribution;
- device health and software rollout;
- authorized evidence intake, retention, and export;
- role and approval administration;
- audit search and reporting.

The cloud provider, tenancy model, evidence region, and disaster-recovery targets remain TBD.

## Network and trust boundaries

- Vehicle internal links are not automatically trusted merely because they are physically inside the vehicle.
- Device-to-device messages should use mutual identity, anti-replay data, versioned schemas, and explicit authorization.
- WAN-facing services terminate through an authenticated egress/API layer; no general remote shell is exposed by default.
- Vehicle diagnostics are read-only unless a specific write command has a safety case, authorization rule, and validation plan.
- Evidence movement is distinct from live-preview or health telemetry.
- Policy updates are signed and versioned; local last-known-good policy remains available offline.

## Dependency rules

```text
Cloud loss      -> local recording, I/O, auth, and current MDT context continue
CAD loss        -> recording and I/O continue
Windows loss    -> Vision Core recording and I/O continue
Vision loss     -> I/O enters defined independent safe behavior
Camera loss     -> other channels and system health continue
GPS loss        -> recording continues; location is marked unavailable/degraded
Storage warning -> operator alert, retention policy, and graceful protection behavior
```

See [degraded operation](MODES_AND_DEGRADED_OPERATION.md) for the complete state model.
