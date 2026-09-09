# CB-01 revision B — circuit reasoning and bench checks

All calculations below are preliminary design calculations, not measurements. User requirements establish the Strijder computing/dashcam/lighting/CAD scope; they do not establish these component selections. This revision intentionally develops a low-power control-board subset with specific wiring.

## 1. Power entry and backup boundary

J101 and J102 are independent source ports. Each has one positive and one return terminal. F101/F102 are inline source-adjacent 1 A fuse proposals. D101/D102 anodes face the sources; cathodes join VSYS. This blocks the ordinary forward charging path between sources but has diode leakage and no absolute reverse-isolation claim. The higher source voltage minus its diode drop supplies the board; closely matched sources can share unequally. It is not vehicle-first priority or a charging circuit.

Start with a single current-limited 12 V laboratory supply. Use another supply to emulate the backup only after reviewing their ground/earth connections. Do not use an unprotected lithium pack. The eventual battery must have independent charging, BMS, temperature limits and undervoltage disconnect. None is hidden inside J102.

At 1 A and an assumed 0.6 V forward drop, an active input diode dissipates approximately 0.6 W. This is a conservative sizing example, not a guaranteed drop. Measure diode temperature with the actual mounting and current. C101 stores only `0.5 × 100 µF × 16² = 12.8 mJ`; it is local decoupling, not a useful backup energy reserve.

D103 is after the diodes, so normal reversed input polarity does not directly forward-bias this shunt. Its cathode is VSYS and its anode is GND. There is no sustained-overvoltage cutoff and no validated transient-energy/fuse coordination. Do not apply vehicle load-dump, jump-start or destructive fault tests to this base. Source current limits may prevent a fuse from opening; a fuse is not an accurate current limiter.

## 2. Rail and thermal budget

U201 is deliberately a simple linear bench supply rather than an invented high-power buck converter. Its inefficiency must not be carried into the full Strijder power architecture. U202 derives 3.3 V from +5V. Total U201 load includes CAN VCC current, U202 input current and every other 5 V load; do not add the 3.3 V budget a second time.

Proposed ceilings are 200 mA through U201 and 50 mA through U202, not the silicon's headline current ratings. A conservative thermal calculation uses VSYS=16 V even though the series input diode normally lowers it:

| Item | Preliminary calculation |
|---|---|
| U201 main dissipation | `(16 − 5) × 0.20 = 2.20 W` |
| Bias/loss allowance | Budget another 0.15 W for this thermal estimate; check vendor maximum ground current |
| U201 thermal path target | Junction-to-case plus interface ≤6 K/W; sink-to-air ≤15 K/W |
| Predicted junction at 40 °C ambient | `40 + 2.35 × 21 ≈ 89.4 °C`, if the selected mounting achieves the thermal target |
| U202 main dissipation | `(5 − 3.3) × 0.05 = 0.085 W` |

Fit a heatsink before loading U201. Check its package thermal data and electrical tab connection before choosing the mounting hardware. Use a thermocouple and verify regulation as temperature stabilizes. A claimed heatsink rating is not proof of actual installed airflow or contact quality. Lower load if the case exceeds 80 °C; use the measured thermal path to assess junction temperature. No enclosure thermal design has been performed.

Place C201/C202 close to U201 pins and C204/C205 close to U202. C203 is an output bulk capacitor. D201 is anode +5V, cathode VSYS, to bypass reverse regulator discharge when the input falls. Do not externally drive either rail; U202 has no independent reverse-power blocking circuit. External MCU GPIO must be power-off tolerant, or board/MCU sequencing must prevent back-power through signal pins. Common GND does not make two independently powered logic devices automatically sequence-safe.

## 3. Peripheral switch

Q301 source is BR_SOURCE, drain BR_OUT and gate BR_GATE. The package tab is drain. Q302 pulls its gate toward GND through R302 when BR_EN is high. R301 pulls gate back to source when Q302 is off; R304 holds the NPN base low if the controller is disconnected. D301 limits negative gate-to-source voltage, with cathode at source and anode at gate.

At source=15.5 V and approximately 12 V across the conducting zener, R302 current is roughly `(15.5 − 12 − 0.2)/1000 = 3.3 mA`. R301 carries about `12/100000 = 0.12 mA`; zener current is approximately the difference. This is below the zener's nominal characterization current, so do not assume exactly 12 V. The un-clamped operating rail itself is below the MOSFET's ±20 V gate limit, but transient behavior still needs measurement.

For source=11.4 V with the zener inactive, the gate pull-down divider gives approximately `(11.4 − 0.2) × 100k/101k = 11.1 V` of gate drive. Wiring drop and transistor saturation affect this. At 3.3 V enable, using 0.85 V base-emitter voltage, R303 supplies about 2.45 mA before subtracting approximately 0.085 mA through R304. This is ample for the expected few-milliampere collector load; confirm it on the bench.

At 0.5 A and 20 mΩ, ideal room-temperature fully-enhanced MOSFET conduction loss is only 5 mW. That is not a switching-loss or short-circuit result. Slow gate turn-off, output capacitance, wiring inductance and fuse-clearing time may dominate stress. Initial load is resistive; no PWM. Do not add bulk output capacitance, motors, relay coils or an externally powered peripheral without reworking the protection. The single PMOS body diode conducts from BR_OUT back to BR_SOURCE if the output is externally raised.

F301's proposed 0.75 A nominal rating allows margin above a 0.5 A continuous load, but fuse derating and ambient behavior still need a selected part. It does not promise semiconductor survival during a short. A protected automotive high-side switch/eFuse with current sensing and defined inrush behavior is a later replacement, not an implemented feature.

## 4. Optocoupler inputs

Each input has two 680 Ω series resistors and a reverse-parallel 1N4148 across the optocoupler LED. Splitting the resistance shares dissipation and voltage stress. With LED forward voltage assumed 1.2 V:

| Input | Approximate LED current | Dissipation per 680 Ω resistor |
|---|---:|---:|
| 9 V | 5.74 mA | 0.022 W |
| 12 V | 7.94 mA | 0.043 W |
| 16 V | 10.88 mA | 0.081 W |

The 0.5 W resistors have considerable steady bench margin; they are not qualified automotive pulse resistors. Check tolerance, LED forward voltage and optocoupler CTR versus temperature and age. Pull-up current is about `3.3/10k = 0.33 mA`; the initial CTR requirement at 9 V is roughly `0.33/5.74 = 5.75%` before margins. This rough ratio is not a guarantee of saturated output voltage across conditions; verify output LOW against the selected MCU threshold.

The 10 kΩ/10 nF output network gives a nominal 100 µs rising time constant. Specify Schmitt inputs and at least 20 ms software debounce for these proposed slow sense channels. They are not precision ignition comparators: behavior between the proposed absent/asserted bands is intentionally undefined. A long wire shorted to supply looks asserted; this circuit cannot diagnose every wiring fault.

Both LED returns and transistor emitters connect to GND in this base. The optocoupler separates signal energy internally, but there is no galvanic isolation of the assembled system. Splitting ground later changes return topology and requires a new isolation design.

## 5. CAN boundary

U501 uses the VIO variant, powered by +5V at pin 3 and +3V3 at pin 5. S pin 8 and TXD pin 1 are permanently tied to +3V3. There is no software-controllable transmit path. RXD pin 4 reaches the external MCU through R501. The MCU must have a CAN controller and be configured to decode the correct bitrate in listen-only mode. A raw GPIO reader is not a CAN stack.

The base omits a vehicle-specific TVS/filter network and galvanic isolation; only short-cable bench reception is within scope. Use an already-terminated bus with two endpoint resistors and a common reference. Avoid connecting a PC-grounded setup to vehicle wiring. R501 is modest series isolation, not guaranteed power-off backfeed protection; choose a power-off-tolerant receiver input or manage sequencing. Verify the additional RC delay against the selected MCU's input capacitance and bitrate.

## 6. Connector assignment and current interpretation

| Connector | Pin allocation | Proposed ordinary continuous-current budget |
|---|---|---|
| J101 | 1 VIN_A; 2 GND | Each contact must accommodate up to the 1 A total-board ceiling when source A alone supplies it |
| J102 | 1 VIN_B; 2 GND | Same 1 A source ceiling; no assumption of 50/50 sharing |
| J301 | 1 BR_OUT; 2 GND | Up to 0.5 A per contact |
| J302 | 1 BR_EN; 2 GND | Enable signal is approximately 2.5 mA when asserted; not a peripheral supply |
| J401 | 1 IGN_RAW; 2 SEL_RAW; 3 GND | Approximately 10.9 mA per input at 16 V; shared return can carry their sum |
| J402 | 1 IGN_N; 2 SEL_N; 3 GND | Logic interface, not load supply |
| J501 | 1 CAN_H; 2 CAN_L; 3 GND | Bus interface; common-mode/ground-fault current is not bounded by normal receiver current |
| J502 | 1 CAN_RX; 2 GND | Logic interface, not load supply |

CB-01 has six dedicated load/source power-path contacts across J101, J102 and J301, of which two belong to the single switched peripheral. It also has signal-reference contacts. This count **must not be reported as the full Strijder suite's peripheral power pin count**. There are no paralleled contacts in this base. The highest assigned ordinary power-contact current is 1 A at a source port; this is a chosen test envelope, not a connector certification or the eventual suite maximum.

Select actual terminal blocks/housings, mating contacts and wire after checking temperature derating, clearance, wire clamping and fault protection. Keep source/peripheral return currents out of narrow logic return paths. No mechanical cavity-view drawing is released yet.

## 7. Required bench verification — not yet performed

1. Unpowered: compare each physical semiconductor to its manufacturer's exact package diagram. Check diode bands, capacitor polarity, reference designators and continuity against the pin netlist. Check no power-to-ground short.
2. Leave peripheral and external MCU disconnected. Apply 12 V from one supply with 100 mA current limit; raise the limit only after confirming no unexpected current, heating or oscillation. Expect approximately 5 V and 3.3 V within selected-device tolerances.
3. Fit U201 heatsink and apply dummy rail loads in steps without exceeding the combined 200 mA/50 mA budgets. Sweep source 12–16 V and measure rail ripple, voltage and temperatures. Do not infer a pass from the nominal calculation.
4. Test source B independently, then approved dual-source bench wiring. Remove either source and monitor VSYS and rails. Confirm no unintended charging/backfeed, while allowing specified diode leakage. Backup takeover depends on available source voltage.
5. Connect a 33 Ω, at least 15 W resistor at J301; it remains below 0.5 A over this source envelope. Observe Q301 VGS and branch voltage with BR_EN low, high and disconnected. Keep hot resistor clear of wiring. No destructive short test is authorized by this procedure.
6. Sweep each sense input 0, 1, 9, 12 and 16 V using a current-limited test source. Measure LED/input current, LOW/HIGH logic levels and edge chatter. Verify both inputs together and board/MCU power sequencing.
7. On a short isolated bench setup, use a separate two-node CAN bus with proper endpoint termination. Verify known frames appear on RXD and the receiver introduces no dominant transmission during power-up, reset or power loss.
8. Record instrument settings, measured values, waveforms, serial/lot identifiers, ambient/case temperature and pass/fail. Any discrepancy requires a drawing revision. None of these tests was performed in this software environment.

## 8. KiCad handoff and product continuation

Importing the CSV/JSON does not create a valid KiCad design automatically. Create native symbols, check every pin against the exact MPN/package, assign footprints and run ERC. Map diode A/K to the chosen footprint's numeric pads. Treat the old architecture drawing refdes as separate scope; CB-01 numbering is authoritative only within this subassembly.

For the product implementation, next select the compute module/carrier, camera/link standard, display architecture, lighting controller protocol and qualified battery subsystem. Then replace this small linear supply and generic output switch with the sized protected distribution and supervised interfaces those loads require. Preserve the independent operator-lighting behavior specified in the engineering dossier; CB-01 does not yet implement that function.
