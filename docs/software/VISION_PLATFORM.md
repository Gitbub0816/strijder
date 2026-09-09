# Vision platform software

## Runtime model

The embedded Vision Pro processing layer is Linux-based on NVIDIA-class hardware and operates as background infrastructure. The exact distribution, service manager, container strategy, and update mechanism remain TBD.

## Proposed service decomposition

| Service | Inputs | Outputs | Persistent state |
|---|---|---|---|
| Supervisor | Service health, power mode, policy | Restart/degraded-mode actions | Reset and fault history |
| Camera manager | Camera links/configuration | Timestamped streams, health | Channel identity/config |
| Recorder | Media streams, time | Encoded segments | Ring buffer index |
| Event manager | Manual/policy/CAD/vehicle triggers | Evidence windows | Event state |
| Evidence service | Segments, metadata, keys | Encrypted event packages/manifests | Evidence catalog/journal |
| Vision inference | Approved frames/models | Attributed observations | Model/version metadata |
| Vehicle gateway | CAN/OBD/sense, I/O messages | Normalized vehicle state | Short history/config |
| Policy/identity | Signed profiles, device keys | Effective policy, authorization | Last-known-good policy |
| Sync agent | Durable outbound/inbound jobs | Remote transfers | Retry queue/checkpoints |
| Health agent | Hardware/service metrics | Operator/admin health | Fault/event history |
| Local API | Authenticated client requests | Versioned responses/events | Minimal session state |

## Recording pipeline

### Goals

- continuous bounded recording;
- channel-independent failure handling;
- timestamps that remain orderable through clock correction;
- fast event preservation without re-encoding where possible;
- storage pressure visible before recording is lost;
- cryptographic linkage between media and manifests.

### Segment model

Each recording segment should carry:

- immutable segment ID;
- device and camera-channel ID;
- monotonic start/end time;
- wall-clock time, source, and uncertainty;
- codec/profile and frame dimensions;
- byte length and content hash;
- integrity/journal reference;
- storage state: ring, pinned, queued, transferred, expired, or faulted.

Segment duration and codec are TBD and must be selected using loss-boundary, indexing, storage, and encoder-overhead tests.

## Computer vision

The product reserves compute for intelligent dashcam functions, but no final model set was recovered. The architecture therefore defines constraints rather than claiming features:

- every output identifies model name/version and source camera;
- confidence values are metadata, not proof;
- nondeterministic observations do not directly command warning-light outputs or vehicle networks;
- raw evidence remains distinguishable from derived annotations;
- model updates are signed, staged, rollback-capable, and audited;
- performance degradation must not starve recording;
- training-data rights and deployment policy require separate approval.

Potential functions such as object detection, event classification, plate recognition, or driver monitoring are not baseline capabilities until explicitly approved and legally reviewed.

## Local API

The operator/MDT domain should access Vision through a mutually authenticated local API or message bus. Required properties:

- explicit semantic versioning;
- bounded and schema-validated messages;
- least-privilege client identities;
- replay protection for commands;
- correlation IDs and idempotency for mutations;
- health and degraded-state semantics;
- no general filesystem share for evidence;
- no unaudited remote shell.

## Configuration

Configuration layers, lowest to highest precedence:

1. immutable hardware capabilities;
2. signed product defaults;
3. signed fleet/agency policy;
4. signed vehicle assignment;
5. time-bounded authorized service override;
6. operator preferences that policy explicitly permits.

The effective configuration is materialized with source/version provenance. Invalid new policy does not replace the last-known-good policy.

## Updates

Proposed update flow:

1. retrieve signed release manifest;
2. verify device compatibility and policy window;
3. stage without disturbing active evidence;
4. validate hash/signature and available rollback space;
5. install only in an allowed power/operational state;
6. health-check the new version;
7. commit or automatically roll back;
8. journal outcome with release and hardware identity.

Vehicle I/O firmware follows a separate, more restrictive release and recovery process.

## Observability

Logs and metrics must not leak evidence, secrets, or unnecessary location/operator data. Minimum health surfaces:

- service state and restart reason;
- camera link/frame/encode status;
- storage capacity, errors, life, and protected-event backlog;
- power source, voltage, current, UPS reserve;
- CPU/GPU utilization and thermals;
- time synchronization quality;
- GNSS and radio state;
- I/O controller heartbeat and fault state;
- sync queue size, age, and failure category;
- active software/configuration/model versions.
