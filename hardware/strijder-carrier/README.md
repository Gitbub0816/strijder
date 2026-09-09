# Strijder Vision Pro/EVS modular carrier — KiCad concept capture (rev A0)

One PCB, two populations. This KiCad project captures the Strijder Vision
carrier board concept for the two hardware product models, using a single
board design with documented do-not-populate (DNP) groups:

| Model | Population |
|---|---|
| **Strijder Vision Pro** | Jetson SOM domain, camera/GMSL domain, operator-validation (validator RS-485), comms (LTE/WiFi/GNSS), dual evidence NVMe, vehicle-I/O MCU core |
| **Strijder Vision EVS** | Everything in Pro **plus** the x86 Windows COM Express domain (+ its NVMe), CAD/Windows display connector, lighting controller/selector interfaces, interlock driver |
| Strijder Vision (base, cam-only) | Out of scope for this board by decision (2026-09-09) |

> **Engineering status:** concept capture. This project is a structured,
> ERC-ready starting point for detailed design — not a routed, reviewed, or
> releasable board. Every part marked `(prov.)` is a provisional selection
> per the dossier's no-invented-certainty rule
> ([docs/STATUS_AND_PROVENANCE.md](../../docs/STATUS_AND_PROVENANCE.md)).

## Files

| File | Content |
|---|---|
| `strijder-carrier.kicad_sch` | Flat concept schematic, all symbols embedded (no external libraries needed) |
| `strijder-carrier.kicad_pcb` | 200×140 mm outline, 12 copper layers, placed footprints, mounting holes — **not routed** |
| `strijder-carrier.kicad_pro` | Net classes (power, 90 Ω/100 Ω diff, CAN, 50 Ω coax) |
| `tools/generate_project.py` | Generator; regenerating overwrites the three files above |

Open with KiCad 7 or newer (KiCad 10 upgrades the format on save).

## What is pin-accurate vs logical

**Pin-accurate (CB-01 rev B bench core).** The five circuits of
[docs/engineering/circuit-base](../../docs/engineering/circuit-base/) are
reproduced verbatim from `output/pin-netlist.csv` — every ref, pin number
and net name matches, including diode `A/K` pin naming. The generator
asserts this on every run. These are: dual-source diode OR power entry,
5 V/3.3 V bench rails, protected P-MOSFET peripheral switch, two opto
sense inputs (IGN/SEL), and the hardware-silent CAN receiver. Per CB-01's
own notes, its linear rails are bench heritage; the production path
replaces them with the branch rails (U710/U711).

**Logical-interface blocks (everything else).** SOM socket, COM Express,
M.2 sockets, GMSL deserializer/serializer, PoC, MCU, power-tree parts and
the DEUTSCH connector wall are captured as functional blocks with logical
pins. Cavity-level/pin-level mapping to the real 260-pin SODIMM, 2×220-pin
COMe, M.2 keys etc. is deliberately deferred to detailed design against
the vendor design guides. This mirrors CB-01's "logical bench pin numbers"
convention.

## Compute module decisions

- **SOM socket:** 260-pin SODIMM (Jetson Orin family). Vision Pro targets
  **Jetson Orin Nano 2** (announced 2026-08-25); Vision EVS targets
  **Jetson Orin NX 16 GB**. Both are pin-compatible in this socket per
  NVIDIA DG-10931. *Verify Orin Nano 2 retains the socket in its design
  guide before layout release.*
- **Future path:** Jetson **Thor T2000/T3000** (announced 2026-07, available
  Q1 2027) are the preferred long-term modules, but their pinout/design
  guide is unpublished — a carrier revision is required once released.
- **Windows COM (EVS only):** COM Express Compact **Type 6** site. RAM is a
  16 GB SODIMM on the chosen COMe module (COM Express carries no
  carrier-level RAM slot by architecture). COMe 12 V rail is fed from the
  VSYS branch (8.5–20 V wide-input modules required).

## Storage

- 2× M.2 M-key 2280 NVMe on the Jetson domain (evidence, up to 8 TB each):
  J620 on PCIe x4, J621 on the second controller — lane budget must be
  verified against the selected module's UPHY configuration.
- 1× M.2 M-key 2280 NVMe on the COMe domain (Windows, ~1 TB): J612.

## Safety boundaries carried from the dossier

- Warning-light load current **never crosses this board** (requirement
  F-010): J806 carries lighting-controller electronics power and
  control/feedback only.
- The vehicle-I/O MCU (U730) with hardware watchdog (U732) owns
  deterministic outputs, independent of Linux/Windows/CAD (F-009, A-003).
- CB-01's CAN receiver is hardware-silent (TXD/S tied high); the MCU CAN
  TX path is intentionally absent until a diagnostic-transmit gate design
  exists (see VEHICLE_IO_AND_HARNESS.md).
- Main head forward camera occupies GMSL link A; FAKRA J650 is the
  alternate population for link A (choose one per build).

## PCB state

12 copper layers are configured per the size-vs-features expectation; the
board is **placement-only**: outline, mounting holes, connector wall
(DEUTSCH row on the left/bottom edges, FAKRA + SMA RF on the top edge,
M.2/COMe/SOM in the field). No routing, no zones, no stackup materials.
`*_TBD` footprints are dimensional placeholders — replace with
manufacturer footprints (TE SODIMM socket, COMe connectors, DEUTSCH
board headers, FAKRA jacks) before any layout work.

## Iterating on this design locally with KiCad + Claude

1. `git pull` this branch on the machine with KiCad 10.
2. Open `hardware/strijder-carrier/strijder-carrier.kicad_pro`.
3. In the PCB editor run **Update PCB from Schematic** to bind nets to the
   placed footprints.
4. A local Claude Code session with the `kicad-mcp` servers connected to
   KiCad's IPC API can then iterate live (cavity mapping, real footprints,
   routing) with the schematic/PCB open.

## Open items before detailed design (register)

1. Cavity-level pin mapping: SODIMM-260 (DG-10931), COMe AB/CD (PICMG
   COM.0 R3.1), M.2 keys, DEUTSCH cavity assignments.
2. Manufacturer part selection for every `(prov.)` reference and `*_TBD`
   footprint.
3. PCIe lane budget for dual evidence NVMe on the selected SOM.
4. PoC filter networks and coax impedance qualification for GMSL links.
5. Power-tree sizing against measured loads (POWER_AND_PROTECTION.md
   release blockers apply unchanged).
6. 40-position CAD display connector allocation (logical subset captured
   on J809).
7. Enclosure/thermal design; the 200×140 mm outline is provisional.
