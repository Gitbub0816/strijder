# Strijder Vision engineering dossier

This directory is the canonical written description of the Strijder Vision suite currently recoverable from prior design work and the original repository.

## Reading order

1. [Status and provenance](STATUS_AND_PROVENANCE.md)
2. [Vision and scope](product/VISION_AND_SCOPE.md)
3. [Product history and brand](product/HISTORY_AND_BRAND.md)
4. [Requirements](product/REQUIREMENTS.md)
5. [Engineering roadmap](product/ROADMAP.md)
6. [System architecture](architecture/SYSTEM_ARCHITECTURE.md)
7. [Hardware architecture](hardware/HARDWARE_ARCHITECTURE.md)
8. [Power architecture](hardware/POWER_ARCHITECTURE.md)
9. [Connectors and harness](hardware/CONNECTORS_AND_HARNESS.md)
10. [Preliminary BOM](hardware/BOM.md)
11. [Cadmium CAD](software/CADMIUM.md)
12. [Evidence and security](software/EVIDENCE_AND_SECURITY.md)
13. [Safety, compliance, and validation](safety/SAFETY_COMPLIANCE_VALIDATION.md)
14. [Installation and service](operations/INSTALLATION_AND_SERVICE.md)
15. [Decision register](DECISION_REGISTER.md)
16. [Glossary](GLOSSARY.md)
17. [Diagram gallery](diagrams/README.md)

## Document status vocabulary

| Label | Meaning |
|---|---|
| **Established** | Explicitly present in the repository or recovered as a prior Strijder decision. |
| **Reconstructed** | A high-confidence synthesis of multiple established decisions, but not recovered verbatim as a single approved specification. |
| **Proposed** | A reference engineering choice added to make the design complete and reviewable. It is not yet an approved product decision. |
| **TBD** | Unknown, unresolved, or dependent on testing, certification, vendor selection, or user approval. |
| **Superseded** | Preserved historical design that was later replaced or expanded. |

## Core diagrams

| View | Source | Rendered image |
|---|---|---|
| Product family | [product-family.puml](diagrams/product-family.puml) | [SVG](diagrams/rendered/product-family.svg) |
| System context | [system-context.puml](diagrams/system-context.puml) | [SVG](diagrams/rendered/system-context.svg) |
| Hardware blocks | [hardware-blocks.puml](diagrams/hardware-blocks.puml) | [SVG](diagrams/rendered/hardware-blocks.svg) |
| Power distribution | [power-distribution.puml](diagrams/power-distribution.puml) | [SVG](diagrams/rendered/power-distribution.svg) |
| Connector topology | [connector-topology.puml](diagrams/connector-topology.puml) | [SVG](diagrams/rendered/connector-topology.svg) |
| Cadmium deployment | [cadmium-deployment.puml](diagrams/cadmium-deployment.puml) | [SVG](diagrams/rendered/cadmium-deployment.svg) |
| Evidence lifecycle | [evidence-lifecycle.puml](diagrams/evidence-lifecycle.puml) | [SVG](diagrams/rendered/evidence-lifecycle.svg) |
| Degraded operation | [degraded-operation.puml](diagrams/degraded-operation.puml) | [SVG](diagrams/rendered/degraded-operation.svg) |
