# Status, provenance, and limits

## Purpose

This dossier consolidates the Strijder Vision design into one reviewable source. It is intentionally broader than the static site currently in the repository and intentionally more cautious than a production specification.

## What is established

The following points are treated as established design history:

- Strijder originated as an all-in-one in-vehicle safety/security dashcam product.
- The scope expanded into Strijder Vision: a rugged public-safety vehicle computer combining recording, evidence, communications, diagnostics, mapping, tracking, and optional cloud administration.
- Strijder Vision Pro EVS is the high-compute Emergency Vehicle System configuration.
- The intensive Vision Pro processing layer uses an NVIDIA-class processor and Linux and is intended to operate behind the scenes rather than expose a normal client-facing desktop.
- Cadmium is the CAD subsystem only. It consists of a Dispatch Console and in-vehicle MDT and integrates into Vision Pro EVS.
- Cadmium proof work used Windows WPF, WebView2, Mapbox, shared domain models, and two switchable modes in one proof executable while retaining an eventual separation into communicating applications.
- The vehicle system must operate online and offline.
- The original site promises continuous dashcam recording, diagnostics, local authentication, evidence journaling, tamper-evident hashes, encrypted export, role-based approval, and optional cloud administration.
- Two connector/harness concepts were discussed. Both are retained in the connector document rather than collapsed into a fabricated final pinout.
- The initial planning load was approximately 75 W. A 20-minute hold-up requires 25 Wh ideally; prototype discussions targeted roughly 50–60 Wh usable and considered a 12.8 V, 6 Ah LiFePO4 pack (about 77 Wh nominal).
- Current preliminary peripheral allocation is 11 positive supply contacts plus 11 matching returns, subject to final loads and contact selection.

## What is not established

The following are not recoverable as final decisions and must not be inferred from the diagrams:

- exact NVIDIA module or carrier-board part number;
- camera sensors, lenses, resolution, frame rate, codec, or number of simultaneously encoded streams;
- exact display size, luminance, touch technology, mounting pattern, or Windows compute SKU;
- final connector manufacturer/series for the later named connector family;
- complete pin-by-pin wiring schedule;
- final rail voltages, fuse values, wire gauges, thermal limits, or transient-protection components;
- lightbar vendor protocols, siren integration, relay/solid-state output ratings, or agency-specific interlocks;
- evidence retention durations, encryption algorithms, key hierarchy, or cloud vendor;
- production CAD backend, tenancy model, dispatch-center redundancy, and interfaces to 911/PSAP systems;
- target certifications, procurement classifications, or legal compliance conclusions;
- production BOM cost, sale price, subscription structure, or warranty terms.

## Interpretation rule

If a document contains both an established decision and a proposed implementation, the proposal is subordinate. A proposal must not be treated as approval merely because it appears in an architecture diagram.

## Existing repository versus later design

The original website describes “Strijder Vehicle Safety” with gold/silver styling and a gold/white emblem. Later branding discussion hard-locked a different direction: the exact dimensional S/triangular geometry, forward tilt, a copper-to-violet liquid-metal/glass finish, black background, and no shield or sword. The repository asset and the later direction conflict and require a deliberate brand decision; neither has been silently discarded.

## Engineering disclaimer

This dossier is a system-design baseline, not a released hardware design. Vehicle electrical systems, emergency warning equipment, evidence systems, lithium battery packs, radio equipment, and public-safety CAD deployments require qualified engineering review, hazard analysis, environmental testing, cybersecurity review, legal review, and jurisdiction-specific approval before field use.
