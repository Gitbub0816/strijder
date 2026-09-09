# Compute, camera, and evidence engineering

Status: inferred requirements and worked sizing examples. NVIDIA/Linux background compute, Windows Cadmium, and a four-camera connector concept were reported in prior conversation; exact chips, stream counts, codecs, and storage were not recovered.

## Board/domain allocation

| Domain | Required function | Interface to other domains | Must be resolved |
|---|---|---|---|
| Vision carrier | Module sequencing, camera ingest, SSD, network and health | Authenticated local API; protected vehicle gateway | NVIDIA SKU, pin multiplexing, carrier reference-design constraints |
| Recording storage | Bounded segment writes and protected events | Block storage to Vision only; controlled export API | Interface, capacity, endurance, power-loss behavior |
| Windows operator | Cadmium WPF/WebView2 maps and vehicle UI | Ethernet/USB/other selected transport; separate supply | Integrated display computer versus separate host |
| I/O controller | Physical selector, input conditioning, permitted output modes | Bounded command/state protocol | MCU, watchdog, transport, vendor warning-controller protocol |
| Radios/GNSS | Operational synchronization and location/time | Module-specific buses and external RF ports | Certified module, antennas, power peaks, clock quality |

Separate operating systems do not prove electrical independence. Verify shared regulators, reset lines, network switches and ground returns for common-cause faults.

## Camera pipeline specification worksheet

For each installed channel record: sensor part, lens/FOV, mount, resolution, frame rate, pixel format, HDR exposure behavior, serializer/deserializer, link length, PoC voltage/current, encode profile, target/maximum bitrate, microphone association, time source, calibration version, and fault indication.

### Raw versus encoded throughput

For active pixels only:

`raw_bits_per_second = width × height × fps × bits_per_pixel`

Example, four 1920×1080 channels at 30 fps and 12-bit samples:

- Per channel: 746.496 Mbit/s.
- Four channels: 2.986 Gbit/s, before transport framing and blanking.
- A 16-bit memory representation: 497.664 MB/s across four streams before copies and processing.

These are workload examples, not selected camera specifications. Validate actual CSI lane rates, serializer limits, memory copies, GPU preprocessing, and concurrent encoder limits for the selected module. Encoded evidence bandwidth is much smaller than raw ingest bandwidth; do not size camera links from SSD recording bitrate.

## Recording storage calculations

Decimal units, continuous recording:

`GB_per_day = aggregate_Mbit_per_second × 10.8`

| Example configuration | Aggregate encoded rate | GB/day | Days in 800 GB recording allocation |
|---|---:|---:|---:|
| Four channels × 4 Mbit/s | 16 Mbit/s | 172.8 | 4.63 |
| Four channels × 8 Mbit/s | 32 Mbit/s | 345.6 | 2.31 |
| Four channels × 12 Mbit/s | 48 Mbit/s | 518.4 | 1.54 |

800 GB is an illustrative allocation within a larger SSD, not an approved capacity. Reserve storage separately for OS, updates/rollback, free-space margin, indexes, logs, protected events, and upload backlog. Audio, containers, indexes, thumbnails and variable-bitrate peaks are additional.

### Incident reserve

At an aggregate 32 Mbit/s, a 20-minute event is approximately 4.8 GB. One hundred such events require approximately 480 GB if stored independently. Referencing pinned ring-buffer segments can avoid duplicate media writes, but eviction, reference counts and transaction recovery must be correct. Decide whether overlapping events share immutable segments.

### Endurance

32 Mbit/s implies about 126.1 TB/year of media writes before write amplification and metadata. Over five years that is about 630.7 TB. Select SSD endurance using measured host writes, workload duty cycle, write amplification, temperature and reserve; nominal capacity alone is insufficient. Do not assume consumer “power-loss protection” marketing means acknowledged writes survive arbitrary removal.

## Synchronization and depot transfer

For backlog `B` GB and effective upload `R` Mbit/s:

`transfer_hours = B × 8000 / R / 3600`

A 100 GB backlog requires about 11.1 hours at 20 Mbit/s effective throughput, or 2.22 hours at 100 Mbit/s. Simultaneous new uploads, cellular contention and operational traffic extend this. Configure separate queues for urgent CAD messages, health/policy, event metadata and bulk media. Upload scheduling must not contend with capture for unbounded memory or SSD I/O.

## Evidence commit protocol — proposed

1. Allocate segment identity and capture-time provenance.
2. Write media into a temporary segment; track actual successful writes.
3. Close/flush media using selected filesystem/storage durability guarantees.
4. Compute content hash and commit immutable media metadata.
5. Atomically publish a manifest/journal state that references only committed segments.
6. Mark an event sealed only when all required media and metadata are durable.
7. Upload resumably; validate remote receipt against manifest before local-policy disposition.

Power failure at each boundary must produce either a recoverable partial segment or a valid committed segment, never a false sealed event. Hashes detect modification relative to a trusted manifest; they do not by themselves prove camera authenticity, correct time, or complete capture.

## Timestamp contract

Store monotonic time, UTC estimate, source, synchronization uncertainty, boot/session ID, channel sequence and dropped-frame counters. Wall-clock corrections must not reorder journal history. Cross-camera synchronization requirements depend on actual use; timestamp proximity is not proof of simultaneous exposures.

## Resource acceptance worksheet

| Scenario | Capture/encode | Inference | Storage | Network | Pass evidence |
|---|---|---|---|---|---|
| Full operation | All selected channels | Maximum approved models | Ring + protected event | CAD + bulk upload | Frame loss, latency, power and temperature within approved limits |
| Storage pressure | All channels | Normal | Near configured limit | Offline | No protected-event eviction; explicit degraded status |
| Thermal stress | Priority capture maintained | First candidate for throttling | Durable writes | Reduced bulk | Measured stable derating without false recording status |
| Windows reboot | Unaffected if architecture supports independence | Normal | Normal | Local UI reconnects | No recorder restart caused by display reset |
| WAN loss/reconnect | Unaffected | Normal | Growing bounded backlog | Replay/idempotent catch-up | No duplicate CAD mutations or missed evidence receipt |
| Hard power loss | Finalization or documented partial segment | Stopped | Recovery scan | Off | Verifiable manifest state after reboot |

No numerical performance threshold becomes binding until the selected components, operating range and operator use cases are approved.
