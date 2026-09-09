# Manufacturer reference register

Reviewed 2026-09-09. These sources support component properties and pin assignments, not approval of the complete Strijder circuit. Calculations and topology choices in this revision are new engineering proposals. Manufacturer diagrams are not copied into this repository.

| Drawing references | Manufacturer source | Checked design facts |
|---|---|---|
| D101, D102 | [ST STPS5L60 datasheet](https://www.st.com/resource/en/datasheet/stps5l60.pdf) | Single Schottky; 60 V class, axial DO-201AD variant; cathode band. Published current rating is not board ampacity. |
| D103 | [Littelfuse SMBJ18A](https://www.littelfuse.com/products/overvoltage-protection/tvs-diodes/surface-mount/smbj/smbj18a) | Unidirectional transient suppressor; 18 V standoff; pulse rating does not establish load-dump endurance. |
| U201 | [TI LM340/LM7805 datasheet](https://www.ti.com/lit/ds/symlink/lm340.pdf) | TO-220: input 1, ground 2, output 3; input/output bypass, reverse-discharge protection and heatsinking requirements. Exact selected order code LM7805CT/NOPB. |
| U202 | [Microchip MCP1700 datasheet](https://ww1.microchip.com/downloads/aemDocuments/documents/APID/ProductDocuments/DataSheets/MCP1700-Data-Sheet-20001826F.pdf) | Table 3-1: TO-92 ground 1, input 2, output 3. Input range 2.3–6 V; 1 µF ceramic output supported. Selected 3.3 V variant MCP1700-3302E/TO. |
| Q301 | [Infineon IRF4905PbF datasheet](https://www.infineon.com/dgdl/irf4905pbf.pdf) | P-channel, TO-220 G/D/S ordering, drain tab, body diode; 20 mΩ maximum at VGS = −10 V under specified test conditions. Gate threshold is not full enhancement. |
| Q302 | [onsemi 2N3904 datasheet](https://www.onsemi.com/pdf/datasheet/2n3904-d.pdf) | TO-92 emitter 1, base 2, collector 3; 40 V collector-emitter class. Other transistor families/packages may reverse lead order. |
| D301 | [Vishay BZX55 datasheet](https://www.vishay.com/docs/85604/bzx55.pdf) | BZX55C12 nominal 12 V; zener tolerance/test current matter; cathode toward PMOS source. |
| U401, U402 | [Vishay VO617A datasheet](https://www.vishay.com/docs/83430/vo617a.pdf) | DIP-4 LED anode 1, cathode 2, transistor emitter 3, collector 4. CTR grouping is specified at defined test conditions; drawing uses VO617A-3. |
| U501 | [TI TCAN1051 family datasheet](https://www.ti.com/lit/ds/symlink/tcan1051-q1.pdf) | SOIC VIO variant: TXD 1, GND 2, VCC 3, RXD 4, VIO 5, CANL 6, CANH 7, S 8. S high disables driver and preserves receiver. |

U501's electrical behavior is supported by the vendor's silent-mode definition; firmware cannot change the hard-wired S net. This does not imply the entire board is automotive-qualified or that connection to an arbitrary vehicle is permissible.

Passive BOM entries are value/rating specifications, not finalized purchasing selections. Fuses need DC interruption and clearing-curve selection, capacitors need voltage/temperature/ESR review, connectors need actual housings and contacts, and the heatsink requires mechanical selection. D201 (1N5819) and D401/D402 (1N4148) are generic family selections: select a named manufacturer and verify its axial package drawing before assembly. No substitute is automatically pin-compatible.
