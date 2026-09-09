# Evidence and security architecture

## Established product promises

The original Strijder site describes:

- high-dynamic-range dashcam recording;
- tamper-evident hashes;
- role-based export approvals;
- event journaling and retention controls;
- encrypted exports with audit trails;
- automated incident packages;
- signed profiles and vehicle keys;
- local policy enforcement;
- optional cloud administration;
- local validation using biometrics, NFC, or keycode;
- fleet profile keys protected on-device.

These are product requirements/concepts. The current repository does not contain an implemented evidence engine or key-management system.

## Evidence lifecycle

![Evidence lifecycle](../diagrams/rendered/evidence-lifecycle.svg)

### Capture

- Each source has a stable device/channel identity.
- Media receives monotonic timing and available synchronized time provenance.
- Capture health is explicit; the UI must not show “recording” when durable writes are failing.

### Buffer

- Ordinary segments enter a bounded ring buffer.
- Retention policy is versioned and attributable.
- Storage pressure triggers deterministic behavior and visible health state.

### Preserve

- An authorized trigger opens an evidence event.
- Policy-defined pre/post segments are pinned.
- Event metadata identifies trigger source and context provenance.
- Derived AI labels remain annotations, not modifications to original media.

### Seal

- Segment content hashes and metadata are bound into a manifest.
- A device-protected identity signs or authenticates the event record.
- Journal ordering prevents silent deletion/replacement from appearing normal.
- Final cryptographic algorithms and key hierarchy remain TBD and require expert review.

### Synchronize

- Upload is encrypted, resumable, and idempotent.
- Each chunk/object is verified before completion.
- Receipt is recorded without deleting the local event prematurely.
- Evidence transfer has lower network priority than current operational CAD traffic where necessary.

### Review/export

- Authorization is role and policy based.
- Certain exports may require a second approval.
- Export produces a manifest, hashes, actor, time, reason, and source event.
- Export never silently changes the original.

### Retain/delete

- Retention is driven by approved agency policy and legal holds.
- Deletion or cryptographic erasure is authorized, journaled, and distinguishable from corruption.
- No fixed retention duration is established in this dossier.

## Threat model summary

| Threat | Example | Required controls |
|---|---|---|
| Physical tampering | Remove storage, substitute camera, access debug port | Tamper evidence, protected keys, signed device identity, locked service state |
| Malicious peripheral | Spoof camera/controller/display | Mutual device identity, allow-listed hardware/config, schema validation |
| Network attacker | Replay control request, intercept evidence | Mutual authentication, encryption, nonces/sequences, expiry, integrity verification |
| Compromised Windows UI | Attempt raw evidence or arbitrary I/O access | Least-privilege API, no mounted evidence store, named requests only |
| Compromised Linux service | Attempt unsafe physical output | Separate I/O controller and interlock enforcement |
| Insider misuse | Unauthorized export/live access | Roles, dual approval where needed, audit, policy, alerting |
| Cloud compromise | Rewrite policy/evidence | Signed policy, protected evidence manifests, immutable/audited records, last-known-good config |
| Clock manipulation | Misstate incident time/order | Monotonic ordering plus time-source/uncertainty metadata |
| Denial of service | Fill storage or saturate WAN | Quotas, priority queues, bounded buffers, health alerts |
| Update compromise | Install modified software/model | Signed manifests, compatibility checks, staged rollout, rollback |

## Identity domains

Separate identities are needed for:

- manufacturer/provisioning authority;
- fleet/agency;
- vehicle;
- Vision Core;
- I/O controller;
- Windows/MDT;
- camera/peripheral where supported;
- operator;
- dispatcher/admin/service user;
- software/configuration/model release.

One shared fleet secret is insufficient for attribution or containment.

## Authentication and authorization

### Local operator

Biometric, NFC, or keycode mechanisms validate a local operator session according to signed policy. Biometric templates should remain within the platform authenticator where possible; the product should receive an assertion rather than raw biometric material.

### Service

Service access is time bounded, role limited, and logged. It should permit diagnostics without permitting ordinary evidence decryption or unrestricted vehicle outputs.

### Remote

Remote live access, evidence export, policy changes, and software rollout are separate permissions. Administrative role alone does not imply all four.

## Cryptographic design still required

A production security design must select and document:

- secure/measured boot and hardware root of trust;
- device enrollment, certificate rotation, and revocation;
- encryption-at-rest method and per-device/per-event keys;
- signing/MAC scheme for manifests and journal entries;
- key escrow/recovery and agency separation;
- export-container format and independent verification tool;
- secure erase and decommissioning;
- update framework and rollback protection;
- audit immutability and retention.

## Privacy controls

Live audio, remote camera access, precise location, operator identity, and vehicle diagnostics are independently configurable policy domains. The UI and audit system must make active capture/access visible where law and operational policy require it.

## Security validation

- hardware debug and storage-removal attack tests;
- replay, downgrade, impersonation, malformed-message, and authorization tests;
- evidence modification/truncation/reordering verification;
- interrupted upload/export recovery;
- compromised Windows-client containment;
- Linux-to-I/O authorization and safe-state tests;
- key rotation/revocation/decommissioning exercises;
- penetration testing before any operational pilot.
