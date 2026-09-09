# Power entry, backup supply, and peripheral protection

Status: **conceptual engineering derivation, not a released electrical design**. Prepared 2026-09-09 from the repository's [power history](../hardware/POWER_ARCHITECTURE.md), [connector history](../hardware/CONNECTORS_AND_HARNESS.md), and the present conversation. Net names and reference designators below are proposed drawing conventions, not verified PCB or harness assignments.

## 1. Evidence boundary and corrections

The user confirms that Strijder Vision combines in-vehicle computing, dashcam functions, lighting controls, and CAD. Earlier assistant messages and the reconstructed dossier contain a nominal 12–14 V vehicle supply, 75 W load, 20-minute backup objective, and a 12.8 V / 6 Ah pack example. Those are **unverified planning anchors**, not independently recovered user-approved electrical requirements. No production load inventory, selected converter, released connector pinout, battery qualification, or thermal test report is present.

Three earlier numerical statements must not become procurement requirements:

- **22 peripheral power contacts** was an illustrative allocation of 11 supply and 11 return contacts. It is not a complete system pin count and does not include every upstream feed, battery connection, shield, or possible camera-power interface.
- **4.17 A/contact** is the ideal equal division of `75 W / 9 V / 2`; it is neither a proven worst case nor a contact rating.
- **5 A/contact** cannot be accepted as sufficient without input losses, charger load, tolerance, current imbalance, ambient temperature, bundling, and open-contact behavior.

This document supersedes those interpretations for engineering use without erasing their historical record. A minimum operating input of 9 V is only a calculation case. Nominally 12 V vehicles still need a specified crank, jump-start, reverse battery, and surge envelope. Compatibility with a nominal 24 V vehicle is **not established**.

## 2. Conceptual sheets

- [Power front end and backup power path](schematics/power-front-end.puml)
- [Repeated protected peripheral branch](schematics/peripheral-branch.puml)

The PlantUML sheets describe **schematic-level connectivity and component roles**. They do not contain complete manufacturer pin connections, parasitics, gate networks, controller compensation, PCB creepage/clearance, wire gauges, or production values. They are not substitutes for an ECAD schematic, electrical-rules check, simulation, or vehicle qualification.

## 3. Net and domain definition

| Net | Definition | Release condition |
|---|---|---|
| `VBAT_RAW` | Vehicle positive at J101, downstream of source-adjacent harness fuse F100 | Vehicle supply envelope and installation fuse location specified |
| `PWR_RTN` | Intentional vehicle power return; connected to supply negative through dedicated harness path | Return ampacity, voltage drop, and chassis bond approved |
| `VBAT_FUSED` | After optional board/service fuse F101 | Fuse coordination with F100 demonstrated |
| `VBAT_PROT` | Reverse-polarity/overvoltage protected output | Selected controller/FET topology verified over faults |
| `VBAT_FILTERED` | Damped input-filter output | Converter/filter interaction stable |
| `PACK_OUT` | Backup pack output after BMS and source-adjacent pack fuse F102 | Pack vendor, chemistry, charging and disconnect behavior approved |
| `VSYS_BACKED` | Source-selected vehicle/backup bus, **not necessarily regulated** | Switchover, reverse isolation, and operating span verified |
| `VPERIPH_n` | Regulated rail selected for peripheral group n | Required voltage, tolerance, power, and sequence defined |
| `VBR_n` | Switched/current-protected branch output | Harness and peripheral operating/fault limits established |
| `CHASSIS` | Enclosure/shield termination domain | Bond/EMC strategy reviewed; never assumed to replace PWR_RTN |
| `IGN_SENSE` | Conditioned ignition signal, not a peripheral power supply | Thresholds, debounce, transient protection and parked current defined |

`PWR_RTN` is not an isolated safety ground. An optional galvanically isolated peripheral requires its own secondary return net and explicit barrier design. USB, video shields, CAN ground, antenna shields, and mounting hardware can create unintended parallel return paths; drawings and testing must account for them.

## 4. Power-entry circuit intent

1. **F100, harness source fuse:** physically close to the battery tap; protects the installed conductor before it reaches the enclosure. Board protection cannot clear a short upstream of the board.
2. **F101, board/service fuse:** optional coordinated protection, not automatically the same rating as F100. Do not routinely fuse the sole ground return independently of the positive feed.
3. **D101, transient suppression network:** shunts input transients to PWR_RTN. Device polarity and topology must be coordinated with reverse-battery protection; a unidirectional TVS ahead of polarity protection can conduct heavily during reversal. Standoff, clamp voltage at actual surge current, energy, temperature, and upstream clearing behavior remain TBD.
4. **U101 with Q101/Q102:** reverse-current and reverse-polarity protection plus controlled disconnect for unacceptable input. External back-to-back MOSFET orientation, controller variant, gate clamps, sense resistors, and overvoltage divider must follow the selected reference circuit. Do not infer an unlimited surge capability from a controller's maximum supply rating.
5. **L101/C101/C102 and damping:** input EMI filtering designed with actual converter input impedance, wiring inductance, and suppressor placement. A filter can ring or destabilize a constant-power converter; values require simulation and measurement.
6. **U103 source manager:** selects protected vehicle supply or battery discharge path without unintentionally connecting sources together. Includes reverse blocking toward vehicle and charger. Its discharge path is not the charging path.
7. **U104 rail conversion:** regulated buck or buck-boost stages selected from the full `VSYS_BACKED` span. A 12 V output may need buck-boost operation when the source falls below 12 V. Compute and display products may instead require other rails or native wide-range inputs.
8. **U105 always-on supervisor:** measures source validity and reserve, sequences loads, and requests evidence flush/shutdown. Hardware power-good/reset paths must work when application software is unavailable.

The lighting **control electronics** may be a protected low-power branch. Lamp power, siren amplifiers, motors, and other high-current actuators require their own assessed distribution, source fuse, return path, suppression, and load switching. This sheet neither routes warning-light current through the compute enclosure nor authorizes vehicle interlock actuation.

## 5. Backup supply intent

U102 is a chemistry-specific charger with temperature supervision and input-current budgeting. A BMS alone is not a charger. Charge enable must consider battery temperature, pack state, vehicle voltage, parked-vehicle policy, and the remaining vehicle-input power budget. Disable or throttle charging during crank/low input before sacrificing recording power. Prevent circulating current from pack through the system bus back into its own charger input.

The historical LiFePO4 pack example does not establish permissible low-temperature charging, mounting, crash protection, or service strategy. Pack limits must come from the selected pack manufacturer. Provide a source-adjacent pack fuse, service disconnect, temperature sensing, and accessible pack identity/health information. Pack removal, BMS cutoff, and depleted-pack boot must be explicitly tested.

Shutdown sequence, proposed: source loss → debounce/validate → suspend charging → shed optional loads → notify recorder and MDT → flush evidence and persistent state → obtain bounded acknowledgement or timeout → remove main rails → retain only approved supervisor load. The exact reserve threshold and timeout are requirements to determine, not invented timing values. Warning-light availability must not depend on this compute shutdown sequence.

## 6. Current and energy calculations

Use load-side output powers consistently; do not add converter losses twice if a measured input power already includes them.

```text
I_vehicle = [sum(P_load_i / eta_i) + P_charge_out / eta_charge + P_aux_input] / V_vehicle
I_return_segment = sum(currents actually sharing that return segment)
V_load = V_source - I * (R_supply + R_return + R_contacts + R_switches)
P_contact = I_contact^2 * R_contact
I_inrush_cap = C_load * dV/dt      (plus active-load current during ramp)
E_hold = 0.5 * C * (V_start^2 - V_end^2)
E_pack_nominal >= P_backed * t / (eta_discharge * f_temperature * f_aging * f_usable)
```

Illustrative input stress, **not specification**: assuming 75 W output, 90% aggregate conversion efficiency, 20 W delivered charging at 90%, and 1 W auxiliary input consumption:

```text
P_input = 75/0.90 + 20/0.90 + 1 = 106.56 W
I_input at 9 V = 11.84 A
Ideal two-contact sharing = 5.92 A/contact
Same example with charging disabled = 9.37 A total, 4.69 A/contact ideal
```

Consequently the old 4.2 A/contact conclusion cannot bound this entirely plausible scenario. The example does not prescribe a 20 W charger or 90% efficiency.

For two resistive paths, `I1 = Itotal * R2/(R1+R2)`. With illustrative path resistances 10 mΩ and 15 mΩ, a total 11.84 A divides about 7.10 A and 4.74 A. A single open leaves 11.84 A in the survivor until protection reacts. A shared branch eFuse does **not** detect which parallel contact is overloaded when total current remains below its trip threshold. Select single suitably rated contacts where practical; otherwise qualify sharing and survivor behavior or provide separately supervised/protected paths. Analyze positive and return contacts independently.

At 75 W for 20 minutes, ideal load energy is 25 Wh. With hypothetical discharge efficiency 0.90, cold factor 0.80, aging factor 0.80, and usable-depth factor 0.80, nominal energy required is about **54.3 Wh**, before explicit additional reserve. A nominal 76.8 Wh example could meet that arithmetic but is not proof of runtime or safety. Measure runtime against actual load and actual temperature/end-of-life assumptions.

## 7. Repeated peripheral branch circuit

For branch n, assign U2nn to its protected high-side switch/eFuse, R2nn to current measurement or setpoint components, C2nn to downstream capacitance, D2nn to connector transient protection, and J2nn to the harness connection. The example drawing uses branch 1 reference designators. Final ECAD must resolve every physical pin.

- Choose a branch input rail that matches the peripheral; do not label a raw source-selected bus as regulated 12 V.
- Put hardware current limiting/short shutdown ahead of the harness. Determine whether the chosen device blocks reverse current when disabled; add back-to-back switching if required.
- Set startup ramp from measured load capacitance and active boot demand. Coordinate fault blanking with safe operating area and wire protection.
- Prefer bounded retry or latch-off for persistent shorts; repeated automatic retries can heat a harness or faulted device.
- Carry supply and return through deliberately allocated contacts. Size any combined return segment for the **sum** of its loads.
- Measure switched voltage as well as current to distinguish off, disconnected, undervoltage, and overloaded states where possible.
- Default nonessential branch enables off during supervisor reset. Essential recording rail restart policy and hard-short response must be explicitly defined.
- Suppress inductive loads at the appropriate load/driver location with a clamp compatible with the required release time; an ordinary peripheral rail TVS is not a complete actuator driver.

Power-over-coax can eliminate separate camera power wires but does not eliminate camera power demand or the need to rate coax center contact, shield return, injection network, and protection. No exact camera-power/contact count can be released until camera link architecture is selected.

## 8. Candidate component roles and primary references

These are research examples, **not a purchased BOM or interchangeable drop-in parts**.

| Role | Example/reference | What remains to select |
|---|---|---|
| Reverse-battery/source protection U101 | TI LM7480-Q1 family | Variant, external FET voltage/SOA/RDS(on), topology, surge handling, gate networks |
| Source selection U103 | TI automotive priority power-mux application brief | Source priorities, controller choice, switching thresholds, cross-source isolation |
| Protected rail branch U201 | TI TPS25982 eFuse as a functional example | Vehicle qualification, rail voltage margin, current range, fault mode, package/thermal suitability |
| Battery U102/BAT101 | No part selected | Chemistry, qualified pack, charge policy, BMS, transport/service constraints |
| Converter U104 | No part selected | Output inventory, input span, efficiency map, EMI, startup and thermal envelope |
| D101/F100/L101 | No part selected | Coordinated surge, short-circuit, EMC and installation requirements |

The LM7480-Q1 controls external back-to-back MOSFETs for ideal-diode and power-path protection; its specified supply range is 3–65 V. System survival depends on the complete surrounding circuit. [TI product page](https://www.ti.com/product/LM7480-Q1) and [datasheet](https://www.ti.com/lit/ds/symlink/lm7480-q1.pdf).

TI documents priority power selection using ideal-diode arrangements; use the full reference and selected controller datasheets to derive source isolation and thresholds. [TI application brief](https://www.ti.com/document-viewer/lit/html/SLVAFK0).

TPS25982 is a 2.7–24 V eFuse family with configurable fault behavior. It is listed here to illustrate protected-branch functions, **not** as an automotive-qualified raw-battery interface. Verify the exact suffix and rating before use. [TI product page](https://www.ti.com/product/TPS25982). Protection coordination and fault dissipation require more than a nominal current-limit setting. [TI Basics of eFuses](https://www.ti.com/lit/slva862).

## 9. Verification and release matrix

No pass/fail number below is intentionally invented. Each TBD limit must become a signed requirement before qualification, with test equipment, waveform, source impedance, wiring and temperature documented.

| Test | Measurement / injected condition | Acceptance basis |
|---|---|---|
| Load inventory | Boot, record all cameras, inference, max brightness, radio TX, charge, shutdown | Peak/continuous rail table signed; branch and upstream margin established |
| Input sweep | Minimum to maximum approved operating voltage | No unintended reset; temperatures and rail tolerance within released limits |
| Reverse polarity | Approved voltage/duration and source impedance | No hazardous heating or damage; defined recovery; no backfeed |
| Surge/jump-start/crank | Selected vehicle/OEM transient profiles | Required functional class achieved; component electrical/SOA limits respected |
| Input/filter stability | Step load, source impedance variation, hot plug | No destructive ringing, oscillation, or false protection trips |
| Rail short | Each harness far end shorted to return and applicable adjacent nets | Isolation within wire/component energy limits; unaffected branches remain in required state |
| Parallel-contact fault | Open and increased resistance on each supply and return path | Survivor protected; no unnoticed thermal overload |
| Return fault | Dedicated return open/high resistance | No unsafe current rerouting through USB/shields/CAN/mounting paths |
| Source transfer | Vehicle drop/return, dead/removed pack, BMS trip | No prohibited rail discontinuity or charger feedback path |
| Pack runtime | Required load at temperature and end-of-life equivalents | Backup interval plus shutdown reserve demonstrated |
| Parked drain | All shutdown states including network wake faults | Approved vehicle battery budget maintained |
| Thermal soak | Populated connector, installed harness and enclosure at maximum ambient | Derated contact, wire, FET, converter and cell temperatures met |
| Evidence integrity | Repeated loss during recording/finalization | Defined recoverability and bounded data loss demonstrated |
| Lighting coexistence | Switching external high-current loads | No compute corruption; independent lighting-control requirements maintained |

**Release blockers:** signed rail/load table; actual peripheral list; supply/transient envelope; connector manufacturer and cavity assignment; harness gauge/length; contact derating; battery selection; charge strategy; independent lighting power design; thermal model; fuse coordination; ECAD schematic/ERC; layout review; bench/vehicle test reports. Until resolved, neither the maximum current on one pin nor the final total power-pin count is known.
