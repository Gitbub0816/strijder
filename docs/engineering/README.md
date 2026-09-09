# Strijder engineering definition — revision A

**Release state: inferred design for engineering review, not fabrication or vehicle installation.**

This package translates the available conversations into schematic-level connectivity, interface requirements, calculations, and verification work. It does not substitute invented detail for missing memories. Personal-context retrieval was unavailable during this revision; the evidence register distinguishes direct user statements, repository claims, historical assistant reports, and new inference.

## Package

| Document | Engineering use |
|---|---|
| [Recovered specifications](RECOVERED_SPECIFICATIONS.md) | Evidence, original intent, conflicts, missing selections |
| [Power and protection](POWER_AND_PROTECTION.md) | Input protection, UPS, branch distribution, corrected current sizing |
| [Vehicle I/O and harness](VEHICLE_IO_AND_HARNESS.md) | Sense/control nets, diagnostics, camera/display links, connector constraints |
| [Compute and evidence sizing](COMPUTE_AND_EVIDENCE.md) | Throughput, recording capacity, write endurance, hold-up behavior |
| [Verification and release](VERIFICATION_AND_RELEASE.md) | Bench fixtures, acceptance gates, drawing release requirements |
| [Schematic sheets](schematics/README.md) | Plain-text PlantUML and public-renderer links |

## Schematic meaning

The sheets specify named nets, component roles, connection direction, and isolation boundaries. PlantUML does not provide ECAD electrical-rule checking, symbol-pin mappings, PCB footprints, or a manufacturing netlist. These are **functional electrical schematics**, not KiCad/Altium fabrication files. Refdes are sheet-local conceptual references until the ECAD design assigns global references.

Do not infer a connector cavity number from the order of boxes or an IC pin from a net label. No off-board interface is released until its connector, voltage, return, fault behavior, and protection are defined.

## Corrections to earlier planning numbers

The earlier 22 peripheral contacts and 4.2 A/contact figures were assistant-generated planning examples. They are not established Strijder specifications or verified maxima. The 75 W total was a historical estimate whose included loads are unresolved. A shared supply or return may carry the sum of several branches; parallel contacts do not necessarily share current equally. This package takes precedence over any stronger wording in earlier documents.

## Design freeze prerequisites

1. Select compute module, Windows display/compute placement, camera channels/transport, and radio hardware.
2. Resolve the two historical connector concepts and `Val1`/`Val2` ambiguity.
3. Measure steady, boot, transmit, encoding, inference, charging, and fault currents.
4. Approve independent lighting-control behavior and vehicle-specific interlocks.
5. Set minimum input voltage, transient envelope, battery temperature limits, and shutdown reserve.
6. Review electrical schematics and physical interfaces in ECAD before ordering boards or harnesses.
