# Mechanical and thermal design

## Packaging goals

- ruggedized for vehicle vibration and temperature cycling;
- serviceable by replaceable module rather than exposed board repair;
- tamper-evident around evidence storage and debug access;
- thermally safe at maximum compute, encoding, display, radio, and charging load;
- compatible with camera sightlines, driver visibility, airbags, vehicle controls, and maintenance access;
- sealed appropriately for each installation zone;
- labeled and keyed so field harnesses cannot be interchanged.

## Proposed physical partition

1. **Core enclosure:** Vision compute, carrier, storage, and internal service/security components.
2. **Power/UPS enclosure:** protected input, DC/DC, energy storage, fusing/e-fuses, and telemetry.
3. **I/O enclosure:** vehicle sensing, deterministic controller, protected outputs, and lighting-controller interface.
4. **Operator assembly:** primary Windows/CAD display, physical controls, and optional integrated compute.
5. **Main camera head:** forward camera, audio/status/event controls as selected.
6. **Auxiliary display/cameras:** individually mounted and replaceable.

Combining enclosures may reduce cost and harnessing but must not erase fault containment or make battery/service access expose evidence storage.

## Thermal design cases

The thermal model must include:

- parked vehicle solar soak;
- cold start;
- maximum NVIDIA compute mode;
- simultaneous camera encoding and AI inference;
- display at maximum brightness;
- cellular transmit and evidence upload;
- UPS charging after depletion;
- failed or obstructed fan where active cooling exists;
- enclosure installation behind panels or in restricted airflow.

No processor thermal design power or ambient limit is final until the compute SKU and mounting location are selected.

## Cooling strategy

Preferred order:

1. chassis-coupled passive heat spreading;
2. conduction to an external finned enclosure where installation permits;
3. controlled internal air movement with fan-health telemetry;
4. deterministic performance reduction and load shedding before unsafe temperature.

Evidence finalization and deterministic I/O receive priority over optional inference or preview workloads.

## Mechanical verification

- connector insertion/extraction and retention;
- cable bend radius, strain relief, chafe, and service loops;
- fastener retention and torque marking;
- vibration, mechanical shock, drop/handling, and resonant-mode testing;
- thermal cycling and temperature-rise measurement;
- ingress appropriate to installation zone;
- salt, fluid, dust, and cleaning-agent exposure where applicable;
- camera alignment retention and calibration reproducibility;
- display readability, glare, night dimming, and touch operation;
- tamper evidence and authorized service opening;
- vehicle-specific airbag, visibility, and crash-safety review.
