# Glossary

| Term | Meaning in this project |
|---|---|
| CAD | Computer-aided/assisted dispatch. |
| Cadmium | The Strijder CAD product only. |
| Dispatch Console | The dispatcher-facing Cadmium Windows application. |
| MDT | Mobile Data Terminal; the in-vehicle Cadmium application. |
| EVS | Emergency Vehicle System; the integrated Vision Pro configuration. |
| Vision Core | Embedded Linux/NVIDIA processing domain handling recording, perception, evidence, and vehicle integration services. |
| Main Head | Primary dashcam/operator head connection in the vehicle harness. |
| Evidence event | A bounded interval and associated metadata preserved from the continuous recording buffer. |
| Ring buffer | Bounded local recording storage in which ordinary footage is overwritten according to policy. |
| Interlock | A deterministic rule preventing or conditioning an output based on vehicle state or authorized operator action. |
| Vehicle I/O controller | Safety-oriented controller that owns physical inputs/outputs, watchdog behavior, and permitted lighting/interlock actions. |
| PoC | Power over coax; camera power sharing the camera coaxial connection where supported. |
| CAN/OBD | Vehicle data interfaces. Access is vehicle- and manufacturer-dependent and must not be assumed writable. |
| Degraded mode | A defined operating condition after loss of a subsystem such as WAN, CAD, cloud, GPS, or a camera. |
