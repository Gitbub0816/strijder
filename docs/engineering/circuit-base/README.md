# CB-01 circuit base — revision B

[Open the five-sheet electrical drawing set (PDF)](output/strijder-circuit-base-rev-b.pdf).

This is a **newly proposed, low-power bench control/interface circuit**, not a recovered Strijder production schematic. It replaces the earlier PlantUML sheets as the starting point for actual circuit review. Those earlier sheets remain architecture references, not electrical schematics.

The drawings use electrical symbols, explicit connections, semiconductor pin numbers, component values, diode polarity, global net labels and reference designators. This is a concrete circuit base to transfer into KiCad later. It is **not** a KiCad file, PCB layout, ERC-checked design, tested prototype or vehicle-installation release.

## Drawing set

| Sheet | Circuit | Vector preview |
|---|---|---|
| 01 | Fused dual-source diode OR, common return and transient shunt | [SVG](output/sheet-01.svg) |
| 02 | 5 V linear regulator, 3.3 V LDO, bypass and reverse-discharge diode | [SVG](output/sheet-02.svg) |
| 03 | P-channel high-side MOSFET, NPN gate driver, gate clamp and default-off bias | [SVG](output/sheet-03.svg) |
| 04 | Two resistor-fed optocoupler inputs, reverse LED protection and logic filtering | [SVG](output/sheet-04.svg) |
| 05 | Hardware-silent CAN transceiver with all eight pins assigned | [SVG](output/sheet-05.svg) |

Supporting files:

- [Design decisions, calculations and bring-up](DESIGN_NOTES.md)
- [Manufacturer references and pin checks](SOURCES.md)
- [Component schedule / BOM](output/bom.csv)
- [Pin-to-net connection list](output/pin-netlist.csv)
- [Structured component/net data](output/netlist.json)
- [Editable drawing generator](draw_circuits.py)

## Deliberately bounded prototype

| Parameter | Proposed bench envelope — not a recovered specification |
|---|---|
| Source voltage | 12–16 V DC, current-limited laboratory supply |
| Total supply current | At most 1 A combined across both inputs; not a fuse-enforced precision limit |
| Regulator loading | U201 total output at most 200 mA, including downstream U202 input current |
| 3.3 V loading | At most 50 mA total; already included in U201 budget |
| Switched peripheral | One 0.5 A maximum continuous resistive/low-capacitance load |
| Sense inputs | Two; proposed 9–16 V asserted, 0–1 V absent, intermediate band unspecified |
| MCU | External, self-powered 3.3 V MCU/controller; common ground, power-off-tolerant inputs required |
| CAN | Short, already-terminated bench bus; passive reception only |
| Environment | Indoor bench, proposed 0–40 °C ambient; no qualification performed |

These values **do not resize Strijder's eventual 75 W-class planning concept** and do not answer the full-suite peripheral contact budget. This board is a low-power subsystem base. No selected camera, display, compute module or lighting vendor interface has been silently substituted into the product requirements.

Not implemented here: the high-power compute supply, charge controller/BMS, priority power mux, battery reserve monitoring, camera serializer/PoC circuitry, Windows/display power, lighting command protocol, independent manual override, interlock actuation or MCU firmware. Each needs a separately selected interface and drawing. A resistor-load output is not permission to connect a lightbar or actuator.

## Read and reproduce

Matching net labels connect electrically across sheets; filled junction dots join wires. Connector numbers are proposed **logical bench pin numbers**, not cavity assignments for the older vehicle harness. Semiconductor pin numbers apply only to the exact package/variant listed. Diode `A/K` names denote anode/cathode, not a universal numeric footprint mapping.

Regenerate with `python3 docs/engineering/circuit-base/draw_circuits.py`. Dependencies: `reportlab`, `PyMuPDF` and DejaVu Sans regular/bold fonts in `/usr/share/fonts/truetype/dejavu` (adjust `FONT_DIR` if necessary). This draws circuits directly as vectors; it does not use Graphviz, Java, PlantUML or image generation. Regeneration does not transmit the design to a public service.

The same script exports the BOM and declared pin netlist. It checks duplicate reference designators, nets with fewer than two terminals and selected critical pin assignments. **These checks do not extract connectivity from drawing geometry or perform ECAD electrical-rule checking.** The PDF/SVGs and netlist were reviewed for correspondence, but independent engineering review and real tests remain required.

## Preview — discrete peripheral switch

![MOSFET peripheral switch electrical circuit](output/sheet-03.svg)
