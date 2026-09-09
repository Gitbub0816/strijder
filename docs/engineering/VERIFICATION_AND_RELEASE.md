# Verification, drawing control, and release

Status: inferred engineering process, not evidence that tests have passed.

## Deliverable levels

| Level | Contents | Current package |
|---|---|---|
| Functional definition | Domains, named nets, expected behavior, risk register | Available |
| Circuit design | Exact symbols/pins, values, protection coordination, simulations | Not released |
| Physical design | PCB stackup/layout, harness cavities, mechanical drawings | Not released |
| Prototype validation | Measured reports, faults, waveform captures, firmware versions | Not performed |
| Production release | Qualified BOM, manufacturing tests, approval records | Not released |

## Bench fixture

Use an isolated test harness and dummy loads before attaching any vehicle or warning equipment. Required fixture functions: current-limited programmable source, fused branches, programmable ignition, electronic loads, controlled power interruption, simulated selector/interlock inputs, appropriate CAN simulator/termination, independently observable outputs, thermal probes, and current/voltage logging. Instrument voltage at both source and load; source-terminal readings conceal cable/connector drop.

No test procedure here authorizes bypassing a vehicle interlock, disabling OEM protection, or driving an actual actuator.

## Verification matrix

| ID | Test | Measurement/observation | Acceptance definition to approve |
|---|---|---|---|
| ENG-P01 | Input operating envelope | Startup, dropout, rail overshoot at load | Min/max voltage, hysteresis and restart policy |
| ENG-P02 | Reverse input/transients | Protected rail, clamp current, component stress | Selected automotive test envelope and safe outcome |
| ENG-P03 | Branch short/open | Fuse/e-fuse response, wire and contact temperature | Selectivity, no unsafe shared-rail collapse |
| ENG-P04 | Parallel contact imbalance | Individual currents and temperature | Derated per-contact limit including one-open fault |
| ENG-P05 | UPS transition and depleted pack | Rails, source current, evidence recovery | No backfeed; approved retention/shutdown interval |
| ENG-P06 | Charging plus maximum load | Total input power and thermal steady state | Source/harness/charger budget not exceeded |
| ENG-I01 | Ignition/input faults | MCU pin voltage, diagnostics, fallback | Safe open/short-to-battery/ground behavior |
| ENG-I02 | CAN connection | Bus errors, loading, termination, isolation | No disruption to representative vehicle network |
| ENG-I03 | Stale/replayed command | Actual output state and rejection log | Deterministic rejection without output glitches |
| ENG-I04 | MCU/Linux/Windows reset | Independent outputs and capture | Approved function-specific safe states |
| ENG-C01 | Camera unplug/replug | Other channels, link recovery, timestamps | Independent fault indication and no false footage |
| ENG-C02 | Cable/EMI stress | Frame errors, link lock, corrupted frames | Selected link margin and error policy |
| ENG-E01 | Power cut during every commit step | Media, journal and manifest recovery | No false sealed state or lost unrelated events |
| ENG-E02 | Tamper and export | Independent verifier, roles, audit | Modification detection and policy enforcement |
| ENG-T01 | Worst enclosure thermal case | Components, contacts, battery, load shed | Approved derating and temperature limits |
| ENG-S01 | Service replacement | Keys, serial association, evidence access | No unauthorized access; traceable repair |

## Fault-state decisions requiring the owner/upfitter

“Everything off” is not universally a safe failure state for emergency warning systems. Define behavior separately for physical selector loss, MCU reset, Linux failure, Windows failure, network loss, low battery and output-stage failure. Evaluate whether existing external warning-controller behavior/manual control must remain independent of Strijder. Do not implement a global fail-off policy from an architectural diagram alone.

## ECAD handoff checklist

- Approved functional requirement and revision for every sheet.
- Exact component manufacturer/order code, package, lifecycle and qualification evidence.
- Datasheet revision and rationale for absolute maximum, operating and derated values.
- Global refdes, physical symbol-pin mapping, no-connect and unused-input treatment.
- Connector front/rear view, pin numbering and mating part; independent review for mirror errors.
- Harness gauge, length, insulation, seal range, color, twist/shield and crimp tooling.
- Component/wire/fuse coordination, creepage/clearance as applicable and chassis bonding plan.
- Worst-case rail, ripple, thermal and tolerance calculations; power sequencing and reset timing.
- ECAD electrical-rule check, PCB design-rule check, controlled deviations.
- Test points and fixture access that do not expose evidence keys or bypass interlocks.
- Prototype BOM and assembly variants clearly separated from production selections.

## Change control

Any change to power input, camera count, compute mode, display, charging rate, wire/contact type or lighting topology reopens the power/harness review. Any change to retention, encode rate or camera count reopens SSD capacity/endurance and upload sizing. Any update affecting output state requires controller hazard and regression review.

Record test results with unit serial, PCB/harness revision, software/configuration, instruments, environmental conditions, setup diagram, expected behavior, actual waveforms/results, deviations and reviewer. A rendered PlantUML sheet is documentation evidence only, not proof of electrical correctness.
