# System requirements

Requirement keywords use **shall** for baseline requirements, **should** for strong design goals, and **may** for optional capability. Status is included so proposed completeness is not confused with a recovered final specification.

## Functional requirements

| ID | Requirement | Status |
|---|---|---|
| F-001 | Vision shall record configured camera channels continuously while in an operational vehicle state. | Established concept |
| F-002 | Vision shall maintain a bounded local recording buffer and protect incident-associated segments from ordinary overwrite. | Reconstructed |
| F-003 | Vision shall function without cloud connectivity and queue permitted synchronization work. | Established |
| F-004 | Vision shall support local operator validation through policy-enabled methods including biometric mediation, NFC, or keycode. | Established concept |
| F-005 | Vision shall validate signed vehicle/fleet profiles before enforcing their policies. | Established concept |
| F-006 | Vision shall collect available vehicle diagnostics through an approved CAN/OBD/sense interface. | Established concept |
| F-007 | Vision shall expose camera, storage, location, network, power, and vehicle-interface health. | Reconstructed |
| F-008 | Vision Pro EVS shall separate embedded Linux processing from the operator's Windows/CAD interface. | Established |
| F-009 | Vehicle-control outputs shall be owned by a deterministic controller with explicit safe defaults and interlocks. | Proposed safety requirement |
| F-010 | High-current warning-light loads shall use independently protected power paths and shall not traverse the compute/peripheral interconnect. | Current engineering boundary |
| F-011 | Cadmium shall provide dispatcher and in-vehicle workflows with shared calls, units, statuses, maps, and messages. | Established/reconstructed |
| F-012 | Cadmium shall retain locally actionable assignments and queue outbound changes during WAN loss. | Proposed production requirement |
| F-013 | Vision may associate evidence events with Cadmium call and unit identifiers. | Reconstructed |
| F-014 | The platform shall support optional rear, side, or auxiliary cameras. | Established concept |
| F-015 | The platform may support optional live vehicle tracking where policy authorizes it. | Established concept |

## Evidence and security requirements

| ID | Requirement | Status |
|---|---|---|
| E-001 | Evidence at rest shall be encrypted. | Established concept |
| E-002 | Evidence exports shall contain tamper-evident hashes and an auditable manifest. | Established concept |
| E-003 | Export authorization shall be role based and may require multiple approvals. | Established concept |
| E-004 | Security-relevant actions shall be written to an append-only or tamper-evident journal. | Reconstructed |
| E-005 | Device and vehicle identities shall use protected cryptographic keys. | Reconstructed from signed vehicle keys/profiles |
| E-006 | Evidence synchronization shall be resumable and idempotent. | Proposed |
| E-007 | Ordinary service access shall not expose evidence decryption keys. | Proposed |
| E-008 | Time, location, operator, call, trigger, and vehicle-state metadata shall be attributable to their source and confidence. | Proposed |
| E-009 | A cloud administrator shall not be able to silently rewrite already-captured evidence. | Proposed |

## Availability and degraded-mode requirements

| ID | Requirement | Status |
|---|---|---|
| A-001 | WAN or cloud failure shall not stop local recording. | Established principle |
| A-002 | Cadmium failure shall not stop recording or deterministic warning-light controls. | Reconstructed boundary |
| A-003 | Vision-compute failure shall leave the vehicle I/O controller in a documented safe state. | Proposed safety requirement |
| A-004 | Loss of one camera shall not corrupt evidence from healthy channels. | Proposed |
| A-005 | Low voltage shall trigger deterministic load shedding and graceful evidence finalization. | Proposed |
| A-006 | The system shall expose fault state without creating a distracting operator workflow. | Proposed |
| A-007 | Updates shall be rollback-capable and shall not leave vehicle controls in an indeterminate state. | Proposed |

## Electrical requirements

| ID | Requirement | Status |
|---|---|---|
| P-001 | The initial design shall be evaluated against an approximately 75 W continuous planning load. | Established planning value |
| P-002 | Main power shall be sized at the lowest supported input voltage, not only nominal 12–14 V operation. | Proposed |
| P-003 | The preliminary main feed shall use at least two positive and two return contacts when size-20-class contacts are used. | Proposed from current calculation |
| P-004 | The UPS shall support a defined graceful-shutdown/recording interval; 20 minutes and 50–60 Wh usable are the present planning anchors. | Established planning values |
| P-005 | Every externally powered branch shall have a defined overcurrent protection strategy and fault isolation. | Proposed |
| P-006 | Power, ground, signal, shield, and chassis bonding shall be explicitly distinguished in the final interface-control drawing. | Proposed |
| P-007 | The system shall be evaluated for reverse polarity, cranking, overvoltage, load dump, conducted/radiated transients, ESD, and thermal derating. | Proposed validation requirement |

## Human-interface requirements

| ID | Requirement | Status |
|---|---|---|
| HMI-001 | Vehicle interactions shall use large, glanceable targets and minimize driver attention. | Proposed |
| HMI-002 | Safety-critical physical controls shall remain distinguishable by touch and shall not depend solely on a touchscreen. | Proposed |
| HMI-003 | Cadmium shall provide automatic day/night map presentation. | Established proof behavior |
| HMI-004 | Dispatch and MDT shall display consistent status semantics and colors. | Established proof behavior |
| HMI-005 | The visual direction shall be modern and personable, using metallic gold and pearl white where consistent with the final brand system. | Established direction |
| HMI-006 | The interface shall avoid chaotic, dense, legacy-CAD presentation. | Established constraint |

## Quality attributes

- **Auditability:** actions affecting evidence, policy, identity, or device state must be attributable.
- **Determinism:** physical outputs and shutdown behavior must not depend on generative or nondeterministic AI.
- **Maintainability:** shared contracts must not force Dispatch, MDT, Vision Core, and I/O firmware into a single deployment unit.
- **Observability:** health data must distinguish device faults, configuration faults, connectivity faults, and upstream service faults.
- **Privacy:** live audio, location, remote access, and cloud synchronization must be policy controlled and visible to authorized administrators.
- **Serviceability:** connectors must be keyed, labeled, strain relieved, and diagnosable without exposing protected evidence.
