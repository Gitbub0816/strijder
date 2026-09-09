# Operational use cases

These use cases describe product intent. Agency policy and jurisdictional requirements control actual deployment.

## UC-01: Start of shift

1. Vehicle power or ignition wakes the system.
2. The vehicle I/O controller establishes safe output defaults.
3. The Vision Core starts recording independently of WAN availability.
4. The operator authenticates locally using an allowed method such as NFC, biometric mediation, or keycode.
5. The system loads and verifies the signed vehicle/fleet policy.
6. Cadmium restores local unit context and synchronizes when connectivity is available.
7. A concise health view reports camera, storage, GPS, network, vehicle interface, and lighting-controller status.

## UC-02: Continuous recording and incident preservation

1. Camera channels continuously write to a bounded local ring buffer.
2. Each segment receives timestamps, channel identity, and integrity metadata.
3. An authorized manual action, configured trigger, or Cadmium association opens an evidence event.
4. Policy-defined pre-event and post-event segments are pinned against overwrite.
5. The event is journaled and encrypted locally.
6. The event synchronizes or exports only under policy and role authorization.

## UC-03: Dispatch a call

1. A dispatcher creates or receives a call in the Dispatch Console.
2. The call appears on the map with status `Pending`.
3. The dispatcher assigns an available unit.
4. The call becomes `Dispatched`; the unit becomes `Assigned`.
5. The MDT receives the assignment immediately or from its durable queue after reconnecting.
6. The operator accepts or updates status according to policy.
7. Dispatch sees status and location updates when connectivity exists.

## UC-04: Respond with navigation

1. The MDT shows the assigned call and destination.
2. Route guidance displays a polyline, current maneuver, maneuver arrow, and animated vehicle position.
3. The map changes between approved day and night styles.
4. Status progresses through `EnRoute`, `OnScene`, and `Cleared`.
5. Loss of WAN does not erase the assignment or current route already held locally.

## UC-05: Emergency-light operation

1. The operator requests a permitted lighting mode through the physical selector or approved operator interface.
2. The deterministic vehicle I/O controller evaluates ignition, voltage, interlocks, policy, and controller health.
3. The controller energizes only approved low-level control outputs or external power-module commands.
4. The high-current lighting power path remains independently fused and outside the compute interconnect.
5. State changes are journaled for diagnostics and, where policy allows, evidence context.

## UC-06: Vehicle fault or low voltage

1. Vehicle sensing detects an out-of-policy condition.
2. The system records the condition and warns the operator without obscuring primary driving information.
3. Nonessential loads may be shed in a deterministic order.
4. Recording and graceful evidence finalization receive priority.
5. The UPS supplies defined hold-up time if primary vehicle power is lost.

## UC-07: Evidence export

1. An authorized user identifies an incident package.
2. Role and policy checks determine whether export is allowed or requires a second approval.
3. Exported content is encrypted or placed in an approved evidence container.
4. A manifest binds files to hashes, device, event, time range, and export actor.
5. The export and every approval are appended to the audit trail.

## UC-08: No network

- recording continues;
- local authentication and signed policy enforcement continue;
- current Cadmium data remains usable;
- new messages and updates queue locally;
- cloud administration and remote live visibility are unavailable;
- synchronization resumes idempotently when the connection returns.

## UC-09: Service replacement

1. A technician places the system into an authorized service state.
2. Diagnostics identify the failed camera, display, storage, radio, or I/O branch.
3. The modular harness allows the affected device to be isolated.
4. Replacement hardware is provisioned with a signed identity and approved configuration.
5. Evidence keys and protected content are not exposed through ordinary service access.
