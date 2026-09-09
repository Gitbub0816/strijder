# Interface catalog

This is a logical interface catalog, not a final wire protocol or API contract.

## Physical interfaces

| Interface | Endpoints | Purpose | Status |
|---|---|---|---|
| Vehicle Power | Vehicle harness ↔ power module | Battery/ignition input, returns, optional wake/health. | Established group; final pinout TBD |
| Validator | Validator ↔ controller/core | Local operator or peripheral validation. | Established group; semantics TBD |
| CAN/OBD/Sense | Vehicle ↔ protected gateway | Diagnostics and approved vehicle-state sensing. | Established group |
| Aux Sensor | External sensor ↔ I/O | Configurable input and power. | Established group |
| Interlock Actuator | I/O ↔ external actuator/module | Approved deterministic output/control. | Established group |
| Lighting Controller | I/O/core ↔ lighting power controller | Named modes, feedback, low-level control. | Established group |
| Lighting Selector | Physical selector ↔ I/O | Operator mode request and indicator state. | Established group |
| Main Dashcam Head | Vision Core ↔ dashcam/operator head | Media, control, power, status. | Established group |
| CAD/Windows Display | Vehicle system ↔ Windows operator display | Data, control, display power/interface. | Established group |
| Aux Camera Display | Camera/core ↔ auxiliary display | Selected video, control, power. | Established group |
| Camera links | Cameras ↔ Vision Core | High-speed media plus optional PoC. | Earlier design used four FAKRA links |
| LTE antenna | Modem ↔ external antenna | Cellular RF. | Earlier design used SMA |

## Logical local APIs

### Vision Local API

Proposed resource groups:

- `/v1/health`
- `/v1/cameras` and `/v1/cameras/{channel}/preview`
- `/v1/events` and `/v1/events/{id}`
- `/v1/vehicle/state`
- `/v1/operator/session`
- `/v1/policy`
- `/v1/sync/status`
- `/v1/control/requests`

The path names are placeholders. Requirements are versioning, mutual authentication, least privilege, bounded response sizes, and explicit degraded states.

### Vision ↔ I/O messages

Minimum message types:

- heartbeat and controller status;
- input-state snapshot and edge event;
- named-mode request and disposition;
- output-state feedback;
- voltage/ignition/power-state report;
- fault and reset reason;
- configuration version and compatibility.

Every control request should include source identity, sequence/nonce, monotonic expiry, requested named mode, and reason. The controller returns accepted/rejected state plus the policy/interlock basis.

### Cadmium local contracts

Shared domain objects include:

- `Call`
- `Unit`
- `Step` (navigation maneuver)
- `Assignment`
- `Message`
- `LocationFix`
- `StatusEvent`

Recovered statuses:

```text
Call: Pending, Dispatched, EnRoute, OnScene, Cleared
Unit: Available, Assigned, EnRoute, OnScene, OutOfService
```

## WebView2 map bridge

The Cadmium proof uses `wwwroot/map.html` hosted in WebView2 and JSON messaging between WPF and JavaScript.

### Host-to-map messages

- initialize style and access configuration;
- set calls and units;
- select/focus feature;
- display route geometry and maneuver;
- update vehicle position and heading;
- switch day/night style;
- toggle approved layers.

### Map-to-host messages

- map ready/error;
- call/unit selected;
- background location selected where allowed;
- viewport changed;
- route or style error;

Messages need a version, type, correlation ID where applicable, and validated payload. Arbitrary JavaScript execution from application data is prohibited.

## Remote interfaces

Final remote protocols are TBD. The architecture assumes:

- authenticated CAD event synchronization;
- health/telemetry submission;
- signed policy/configuration retrieval;
- resumable evidence upload;
- software/update manifest retrieval;
- remote live access only when explicitly enabled and audited.

Remote interfaces must distinguish operational priority. A large evidence upload must not starve current CAD or health traffic.
