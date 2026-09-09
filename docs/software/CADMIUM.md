# Strijder Cadmium CAD

## Product boundary

Cadmium is Strijder's computer-aided/assisted dispatch product. It is integrated into Vision Pro EVS but is not responsible for dashcam capture, evidence custody, or low-level emergency-light control.

## Recovered application structure

The production-oriented solution was specified as `StrijderCadmium.sln` with:

| Project | Responsibility |
|---|---|
| `StrijderCadmium.Core` | Domain models, enums, interfaces, DTOs, validation, utilities. |
| `StrijderCadmium.Infrastructure` | SQLite/EF Core persistence, repositories, migrations, configuration, logging, service implementations. |
| `StrijderCadmium.Map` | Mapbox/WebView2, geocoding, routing, style switching, markers, callouts, layers, JavaScript bridge. |
| `StrijderCadmium.Dispatch` | WPF Dispatch Console executable. |
| `StrijderCadmium.Mdt` | WPF in-vehicle MDT executable. |

Established implementation constraints:

- .NET 8;
- WPF;
- Microsoft WebView2;
- clean architecture/MVVM;
- strict nullable reference types;
- asynchronous I/O with `async`/`await`;
- dependency injection through `Microsoft.Extensions.DependencyInjection`.

## Proof-versus-production shape

The proof was one Windows WPF executable with two switchable modes structured as if they were separate communicating applications:

- Dispatch Console;
- in-vehicle MDT.

They shared `Calls`, `Units`, and `Steps`, plus a shared `wwwroot/map.html`. Production intent separates the executables while keeping shared contracts and services.

![Cadmium deployment](https://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/Gitbub0816/strijder/main/docs/diagrams/cadmium-deployment.puml)

## Domain model

### Call

Minimum fields:

- immutable ID and display/case number;
- type, priority, summary, narrative;
- structured address and coordinates;
- created/updated times and revision;
- status;
- assigned units;
- caller/subject/location fields as policy permits;
- hazards, notes, and attachments as separately authorized data;
- audit and source metadata.

Recovered call statuses:

```text
Pending -> Dispatched -> EnRoute -> OnScene -> Cleared
```

Real production transitions may branch, revert, cancel, hold, or reopen and require an approved transition table.

### Unit

Minimum fields:

- immutable ID and display/call sign;
- unit type/capability;
- crew/operator session;
- vehicle/device association;
- current status and assignment;
- last position, heading, timestamp, and validity;
- connectivity and MDT health.

Recovered unit statuses:

```text
Available, Assigned, EnRoute, OnScene, OutOfService
```

### Navigation step

The shared `Step` model supports:

- sequence;
- instruction and maneuver type;
- geometry/location;
- distance and expected duration;
- road/name context;
- completed/current/upcoming state.

### Additional production entities

Proposed entities include `Assignment`, `StatusEvent`, `Message`, `LocationFix`, `AuditEvent`, `User`, `Role`, `Agency`, `Device`, and `SyncCheckpoint`.

## Dispatch Console

### Reference layout

- call queue with priority and age;
- central map with call/unit markers and approved layers;
- unit roster grouped by status/capability;
- selected-call details and assignment controls;
- messaging/event timeline;
- compact service/connectivity status.

### Required behaviors

- create, update, prioritize, locate, assign, and clear calls;
- view units and status/location freshness;
- assign/reassign units with conflict validation;
- send and receive messages;
- focus call/unit from list or map;
- preserve an auditable operational event stream;
- expose stale/offline state rather than imply live data.

## In-vehicle MDT

### Reference layout

- current assignment and priority;
- large unit-status controls;
- primary map and route;
- next maneuver and maneuver arrow;
- messages and concise call details;
- health/connectivity indicator;
- restricted secondary actions while moving.

### Recovered map behavior

- turn-by-turn route;
- route polyline;
- maneuver arrow;
- animated vehicle icon;
- dispatch markers, calls, and status colors;
- automatic day/night switching.

## Map implementation

The proof hosts `wwwroot/map.html` through WebView2 with host-to-web JSON messaging.

Recovered Mapbox styles:

- dark: `cmiao2pfk008v01s42pxq1ill`
- light: `cmiaph9hw009501s3043fd1ya`

The map component owns:

- initialization and style changes;
- calls and unit source/layers;
- selection and callouts;
- route geometry and maneuvers;
- vehicle position/heading animation;
- geocoding/routing adapters;
- errors and bridge readiness.

Tokens and secrets must not be committed to the repository. Map data licensing, caching, attribution, and offline behavior require explicit implementation.

## Persistence and synchronization

### Local

- SQLite through Entity Framework Core;
- migrations under source control;
- repositories or application ports hiding persistence details;
- transactional writes for call/status/assignment changes;
- durable outbound synchronization queue;
- last-known-good local state for MDT continuity.

### Remote

No final backend was recovered. Production needs:

- authenticated agency/tenant boundaries;
- ordered/idempotent event ingestion;
- durable fan-out to assigned MDTs;
- reconnect and catch-up;
- conflict/authority rules;
- audit retention;
- dispatch-center redundancy and backup operating procedure.

## UI direction

Recovered direction:

- metallic gold and pearl white;
- modern and personable;
- not chaotic or visually dated;
- dark and light map modes;
- consistent call/unit status colors.

The proof experienced a black/blank map-area defect that required corrected files and a new package. Production must expose map initialization/style/token/network errors rather than leaving an unexplained blank region.

## Testing

Minimum automated coverage:

- allowed and prohibited status transitions;
- assignment conflict rules;
- serialization/version compatibility;
- SQLite migrations and recovery;
- offline queue ordering/idempotency;
- WebView2 bridge payload validation;
- day/night style switching without losing layers/selection;
- map initialization and explicit error surface;
- reconnect/catch-up;
- stale location display;
- permission and audit behavior;
- Dispatch and MDT process independence.

## Cadmium-to-Vision integration

Permitted integration includes:

- device/vehicle/operator context;
- call ID and assignment association with an evidence event;
- operator-requested manual event mark;
- system health presentation;
- named, authorized vehicle-control requests through the I/O boundary.

Cadmium does not receive raw evidence decryption keys, mount the evidence store, or directly drive physical outputs.
