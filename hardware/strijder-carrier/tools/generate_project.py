#!/usr/bin/env python3
"""Generate the Strijder Vision Pro/EVS modular carrier KiCad project.

Emits a self-contained KiCad project (schematic with embedded symbols,
PCB with inline footprints, project file). The CB-01 rev B circuit base
(docs/engineering/circuit-base) is reproduced pin-for-pin from its
published pin netlist; the surrounding carrier blocks are captured at the
logical-interface level with provisional part selections, per the
dossier's no-invented-certainty rule.

Regenerate:  python3 hardware/strijder-carrier/tools/generate_project.py
Output:      hardware/strijder-carrier/strijder-carrier.kicad_sch/.kicad_pcb/.kicad_pro
"""

import csv
import json
import os
import uuid

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, ".."))
REPO = os.path.abspath(os.path.join(OUT, "..", ".."))
CB01_NETLIST = os.path.join(REPO, "docs", "engineering", "circuit-base", "output", "pin-netlist.csv")

NS = uuid.UUID("9b1de6b0-6a4f-4bd6-9e70-1a2b3c4d5e6f")


def uid(*key):
    return str(uuid.uuid5(NS, "|".join(str(k) for k in key)))


def f(v):
    s = f"{v:.4f}".rstrip("0").rstrip(".")
    return s if s else "0"


# ---------------------------------------------------------------- symbols
# Each symbol: name -> dict(left=[(number, name)], right=[(number, name)],
#                           ref_prefix, width (body half-width in mm))
# Pins: length 2.54, vertical pitch 2.54, centered vertically.

SYMBOLS = {}


def sym(name, ref, left, right, halfw=None):
    n = max(len(left), len(right), 1)
    if halfw is None:
        halfw = 10.16 if (left and right and (max(len(p[1]) for p in left + right) > 4)) else 3.81
    SYMBOLS[name] = dict(ref=ref, left=left, right=right, halfw=halfw, n=n)


def pin_offsets(s):
    """Return {number: (px, py_symbolframe)} in symbol coords (y up)."""
    out = {}
    n = s["n"]
    top = (n - 1) * 2.54 / 2.0
    for i, (num, _nm) in enumerate(s["left"]):
        out[num] = (-(s["halfw"] + 2.54), top - i * 2.54)
    for i, (num, _nm) in enumerate(s["right"]):
        out[num] = (s["halfw"] + 2.54, top - i * 2.54)
    return out


# --- CB-01 exact parts -------------------------------------------------
sym("Fuse", "F", [("1", "~")], [("2", "~")])
sym("D_AK", "D", [("A", "A")], [("K", "K")])
sym("C", "C", [("1", "~")], [("2", "~")])
sym("R", "R", [("1", "~")], [("2", "~")])
sym("TP", "TP", [("1", "~")], [])
sym("CONN_2", "J", [("1", "1"), ("2", "2")], [])
sym("CONN_3", "J", [("1", "1"), ("2", "2"), ("3", "3")], [])
sym("LM7805", "U", [("1", "IN"), ("2", "GND")], [("3", "OUT")], 5.08)
sym("MCP1700_TO92", "U", [("2", "VIN"), ("1", "GND")], [("3", "VOUT")], 5.08)
sym("PMOS_GDS", "Q", [("1", "G")], [("3", "S"), ("2", "D")], 5.08)
sym("NPN_EBC", "Q", [("2", "B")], [("3", "C"), ("1", "E")], 5.08)
sym("OPTO4", "U", [("1", "A"), ("2", "K")], [("4", "C"), ("3", "E")], 5.08)
sym("TCAN1051", "U",
    [("1", "TXD"), ("4", "RXD"), ("5", "VIO"), ("8", "S")],
    [("3", "VCC"), ("7", "CANH"), ("6", "CANL"), ("2", "GND")], 7.62)

# --- carrier logical blocks (provisional) ------------------------------
sym("SOM_ORIN", "J", [
    ("1", "VDD_IN_5V"), ("2", "GND"), ("3", "POWER_EN"), ("4", "SYS_RESET_N"),
    ("5", "FORCE_RECOVERY_N"), ("6", "SHUTDOWN_REQ_N"), ("7", "SLEEP_WAKE_N"),
    ("8", "UART0_DEBUG_TX"), ("9", "UART0_DEBUG_RX"), ("10", "UART1_IOMCU_TX"),
    ("11", "UART1_IOMCU_RX"), ("12", "I2C0_CAM"), ("13", "FAN_PWM"), ("14", "FAN_TACH"),
], [
    ("20", "PCIE0_X4_TX"), ("21", "PCIE0_X4_RX"), ("22", "PCIE0_REFCLK"),
    ("23", "PCIE0_RST_N"), ("24", "PCIE0_CLKREQ_N"),
    ("25", "PCIE1_X1_TX"), ("26", "PCIE1_X1_RX"), ("27", "PCIE1_REFCLK"),
    ("28", "PCIE1_RST_N"), ("29", "PCIE1_CLKREQ_N"),
    ("30", "CSI_PORT0_4L"), ("31", "CSI_PORT1_4L"),
    ("32", "USB2_0"), ("33", "USB3_0"), ("34", "GBE_MDI"), ("35", "DP0_OUT"),
], 17.78)
sym("COME_T6", "J", [
    ("1", "VCC_12V"), ("2", "GND"), ("3", "PWR_OK"), ("4", "PWRBTN_N"),
    ("5", "SYS_RESET_N"), ("6", "SUS_S3_N"), ("7", "SUS_S5_N"), ("8", "WDT"),
    ("9", "SMB_CLK"), ("10", "SMB_DAT"), ("11", "SPI_BIOS"), ("12", "FAN_PWM"),
], [
    ("20", "PCIE_A_X4"), ("21", "PCIE_B_X1"), ("22", "DDI0_DP"), ("23", "EDP_LVDS"),
    ("24", "USB3_0"), ("25", "USB3_1"), ("26", "USB2_0"), ("27", "USB2_1"),
    ("28", "GBE0_MDI"), ("29", "SATA0"), ("30", "HDA_AUDIO"), ("31", "THRM_N"),
], 17.78)
sym("M2_MKEY", "J", [
    ("1", "3V3"), ("2", "GND"), ("3", "PERST_N"), ("4", "CLKREQ_N"), ("5", "PEWAKE_N"),
], [
    ("10", "PCIE_TX"), ("11", "PCIE_RX"), ("12", "REFCLK"), ("13", "DEVSLP"), ("14", "LED_N"),
], 12.7)
sym("M2_BKEY", "J", [
    ("1", "3V3"), ("2", "GND"), ("3", "W_DISABLE_N"), ("4", "RESET_N"), ("5", "USB2_D"),
], [
    ("10", "USB3"), ("11", "SIM_VCC"), ("12", "SIM_RST"), ("13", "SIM_CLK"),
    ("14", "SIM_IO"), ("15", "ANT_MAIN"), ("16", "ANT_DIV"),
], 12.7)
sym("M2_EKEY", "J", [
    ("1", "3V3"), ("2", "GND"), ("3", "W_DISABLE1_N"), ("4", "W_DISABLE2_N"),
], [
    ("10", "PCIE_X1_TX"), ("11", "PCIE_X1_RX"), ("12", "REFCLK"), ("13", "USB2_D"),
    ("14", "ANT0"), ("15", "ANT1"),
], 12.7)
sym("SIM_SOCKET", "J", [
    ("1", "VCC"), ("2", "RST"), ("3", "CLK"),
], [
    ("4", "IO"), ("5", "GND"), ("6", "DET"),
], 8.89)
sym("GNSS_MOD", "U", [
    ("1", "VCC_3V3"), ("2", "GND"), ("3", "RF_IN"), ("4", "V_BCKP"),
], [
    ("5", "TXD"), ("6", "RXD"), ("7", "PPS"), ("8", "RESET_N"),
], 10.16)
sym("SMA", "J", [("1", "SIG")], [("2", "SHLD")], 5.08)
sym("FAKRA", "J", [("1", "SIG")], [("2", "SHLD")], 5.08)
sym("GMSL_DESER4", "U", [
    ("1", "VDD"), ("2", "GND"), ("3", "LINK_A"), ("4", "LINK_B"), ("5", "LINK_C"),
    ("6", "LINK_D"), ("7", "PWDN_N"),
], [
    ("10", "CSI_OUT0_4L"), ("11", "CSI_OUT1_4L"), ("12", "I2C"), ("13", "LOCK_N"), ("14", "ERRB_N"),
], 15.24)
sym("POC_QUAD", "U", [
    ("1", "VIN"), ("2", "GND"), ("3", "EN"), ("4", "I2C"),
], [
    ("10", "OUT_A"), ("11", "OUT_B"), ("12", "OUT_C"), ("13", "OUT_D"),
], 12.7)
sym("GMSL_SER", "U", [
    ("1", "VDD"), ("2", "GND"), ("3", "VID_IN"), ("4", "I2C"),
], [("10", "GMSL_OUT")], 12.7)
sym("IOMCU", "U", [
    ("1", "VDD_3V3"), ("2", "VSS"), ("3", "NRST"), ("4", "BOOT0"), ("5", "SWDIO"),
    ("6", "SWCLK"), ("7", "WDI_OUT"), ("8", "UART_SOM_TX"), ("9", "UART_SOM_RX"),
    ("10", "I2C_TELEM"),
], [
    ("20", "CAN_RX_IN"), ("21", "IGN_N_IN"), ("22", "SEL_N_IN"), ("23", "BR_EN_OUT"),
    ("24", "RS485_RO"), ("25", "RS485_DI"), ("26", "RS485_DIR"), ("27", "ILK_EN_OUT"),
    ("28", "ILK_FB_IN"), ("29", "LC_TX"), ("30", "LC_RX"), ("31", "LC_FLT_IN"),
    ("32", "LC_EN_OUT"), ("33", "SENSE_BUS"), ("34", "AUX_AIN"), ("35", "EVENT_MARK_IN"),
], 17.78)
sym("WATCHDOG", "U", [("1", "VDD"), ("2", "GND")], [("3", "WDI"), ("4", "RESET_N")], 8.89)
sym("RS485", "U", [
    ("1", "VCC"), ("2", "GND"), ("3", "RO"), ("4", "DI"), ("5", "DIR"),
], [("6", "A"), ("7", "B")], 8.89)
sym("SENSE8", "U", [
    ("1", "3V3"), ("2", "GND"), ("3", "IN0"), ("4", "IN1"), ("5", "IN2"), ("6", "IN3"),
], [
    ("10", "OUT_BUS"), ("11", "IN4"), ("12", "IN5"), ("13", "IN6"), ("14", "IN7"),
], 12.7)
sym("LSDRV", "U", [("1", "VDD"), ("2", "GND"), ("3", "EN")], [("4", "DRV"), ("5", "FB")], 8.89)
sym("FRONTEND", "U", [
    ("1", "VBAT_IN"), ("2", "IGN_IN"), ("3", "GND"),
], [("4", "VOUT_PROT"), ("5", "FLT_N")], 12.7)
sym("PWRPATH", "U", [
    ("1", "VIN_VEH"), ("2", "VIN_PACK"), ("3", "GND"),
], [("4", "VOUT"), ("5", "STAT")], 12.7)
sym("CHARGER", "U", [
    ("1", "VIN"), ("2", "GND"), ("3", "I2C"),
], [("4", "VBAT_PACK"), ("5", "STAT")], 12.7)
sym("EFUSE", "U", [
    ("1", "IN"), ("2", "EN"), ("3", "GND"),
], [("4", "OUT"), ("5", "FLT_N")], 10.16)
sym("BUCK", "U", [
    ("1", "VIN"), ("2", "EN"), ("3", "GND"),
], [("4", "VOUT"), ("5", "PG")], 10.16)
sym("TELEM", "U", [
    ("1", "VS"), ("2", "GND"), ("3", "I2C"),
], [("4", "SENSE1"), ("5", "SENSE2"), ("6", "SENSE3")], 10.16)
sym("CONN_4", "J", [("1", "1"), ("2", "2")], [("3", "3"), ("4", "4")], 5.08)
sym("CONN_6", "J", [("1", "1"), ("2", "2"), ("3", "3")], [("4", "4"), ("5", "5"), ("6", "6")], 5.08)
sym("CONN_8", "J",
    [(str(i), str(i)) for i in range(1, 5)],
    [(str(i), str(i)) for i in range(5, 9)], 6.35)
sym("CONN_16", "J",
    [(str(i), str(i)) for i in range(1, 9)],
    [(str(i), str(i)) for i in range(9, 17)], 7.62)
sym("CONN_20", "J",
    [(str(i), str(i)) for i in range(1, 11)],
    [(str(i), str(i)) for i in range(11, 21)], 7.62)
sym("FAN_HDR", "J", [("1", "GND"), ("2", "12V")], [("3", "TACH"), ("4", "PWM")], 6.35)
sym("SWD_HDR", "J", [("1", "3V3"), ("2", "GND")], [("3", "SWDIO"), ("4", "SWCLK"), ("5", "NRST")], 6.35)


# ------------------------------------------------------------ instances
# (ref, symbol, value, footprint, x, y, {pin_number: net})
INSTANCES = []


def inst(ref, symbol, value, footprint, x, y, nets):
    INSTANCES.append(dict(ref=ref, symbol=symbol, value=value,
                          footprint=footprint, x=x, y=y, nets=nets))


def load_cb01():
    pins = {}
    with open(CB01_NETLIST) as fh:
        for row in csv.DictReader(fh):
            pins.setdefault(row["Ref"], {})[row["Pin"]] = row["Net"]
    return pins


CB = load_cb01()

FP = {  # ref prefix and part -> footprint name (defined in the pcb generator)
    "AXIAL": "strijder:R_Axial_P10.16mm",
    "RADIAL": "strijder:C_Radial_P5.00mm",
    "DO201": "strijder:D_DO-201AD_P12.70mm",
    "DO41": "strijder:D_DO-41_P10.16mm",
    "DO35": "strijder:D_DO-35_P7.62mm",
    "SMB": "strijder:D_SMB",
    "TO220": "strijder:TO-220-3_Vertical",
    "TO92": "strijder:TO-92_Inline",
    "DIP4": "strijder:DIP-4_W7.62mm",
    "SOIC8": "strijder:SOIC-8_3.9x4.9mm_P1.27mm",
    "FUSE": "strijder:Fuseholder_Inline_TBD",
    "TP": "strijder:TestPoint_Pad_2.0mm",
    "HDR2": "strijder:PinHeader_1x02_P2.54mm",
    "HDR3": "strijder:PinHeader_1x03_P2.54mm",
    "HDR4": "strijder:PinHeader_1x04_P2.54mm",
    "HDR5": "strijder:PinHeader_1x05_P2.54mm",
}

# --- CB-01 subset (verbatim bench-heritage core; sheet zones A-E) ------
inst("J101", "CONN_2", "MAIN DC INPUT (bench)", FP["HDR2"], 40, 60, CB["J101"])
inst("J102", "CONN_2", "OPTIONAL BACKUP (bench)", FP["HDR2"], 40, 90, CB["J102"])
inst("F101", "Fuse", "1A/32VDC", FP["FUSE"], 70, 60, CB["F101"])
inst("F102", "Fuse", "1A/32VDC", FP["FUSE"], 70, 90, CB["F102"])
inst("D101", "D_AK", "STPS5L60", FP["DO201"], 100, 60, CB["D101"])
inst("D102", "D_AK", "STPS5L60", FP["DO201"], 100, 90, CB["D102"])
inst("D103", "D_AK", "SMBJ18A", FP["SMB"], 130, 75, CB["D103"])
inst("C101", "C", "100uF/50V", FP["RADIAL"], 160, 75, CB["C101"])
inst("TP101", "TP", "VSYS", FP["TP"], 185, 60, CB["TP101"])
inst("TP102", "TP", "GND", FP["TP"], 185, 90, CB["TP102"])

inst("U201", "LM7805", "LM7805CT/NOPB", FP["TO220"], 60, 140, CB["U201"])
inst("C201", "C", "330nF/50V X7R", FP["RADIAL"], 40, 165, CB["C201"])
inst("C202", "C", "100nF/16V X7R", FP["RADIAL"], 70, 165, CB["C202"])
inst("C203", "C", "10uF/16V", FP["RADIAL"], 100, 165, CB["C203"])
inst("D201", "D_AK", "1N5819", FP["DO41"], 100, 140, CB["D201"])
inst("U202", "MCP1700_TO92", "MCP1700-3302E/TO", FP["TO92"], 150, 140, CB["U202"])
inst("C204", "C", "1uF/10V X7R", FP["RADIAL"], 130, 165, CB["C204"])
inst("C205", "C", "1uF/10V X7R", FP["RADIAL"], 160, 165, CB["C205"])

inst("F301", "Fuse", "0.75A/32VDC", FP["FUSE"], 40, 215, CB["F301"])
inst("Q301", "PMOS_GDS", "IRF4905PbF", FP["TO220"], 75, 215, CB["Q301"])
inst("R301", "R", "100k", FP["AXIAL"], 75, 240, CB["R301"])
inst("D301", "D_AK", "BZX55C12", FP["DO35"], 105, 240, CB["D301"])
inst("R302", "R", "1k/0.5W", FP["AXIAL"], 40, 265, CB["R302"])
inst("Q302", "NPN_EBC", "2N3904", FP["TO92"], 75, 265, CB["Q302"])
inst("R303", "R", "1k", FP["AXIAL"], 110, 265, CB["R303"])
inst("R304", "R", "10k", FP["AXIAL"], 145, 265, CB["R304"])
inst("J301", "CONN_2", "PERIPHERAL (bench)", FP["HDR2"], 145, 215, CB["J301"])
inst("J302", "CONN_2", "3.3V ENABLE (bench)", FP["HDR2"], 175, 265, CB["J302"])

inst("R411", "R", "680/0.5W", FP["AXIAL"], 230, 60, CB["R411"])
inst("R412", "R", "680/0.5W", FP["AXIAL"], 260, 60, CB["R412"])
inst("U401", "OPTO4", "VO617A-3", FP["DIP4"], 295, 60, CB["U401"])
inst("D401", "D_AK", "1N4148", FP["DO35"], 260, 80, CB["D401"])
inst("R413", "R", "10k", FP["AXIAL"], 330, 60, CB["R413"])
inst("C401", "C", "10nF/16V", FP["RADIAL"], 330, 80, CB["C401"])
inst("R421", "R", "680/0.5W", FP["AXIAL"], 230, 110, CB["R421"])
inst("R422", "R", "680/0.5W", FP["AXIAL"], 260, 110, CB["R422"])
inst("U402", "OPTO4", "VO617A-3", FP["DIP4"], 295, 110, CB["U402"])
inst("D402", "D_AK", "1N4148", FP["DO35"], 260, 130, CB["D402"])
inst("R423", "R", "10k", FP["AXIAL"], 330, 110, CB["R423"])
inst("C402", "C", "10nF/16V", FP["RADIAL"], 330, 130, CB["C402"])
inst("J401", "CONN_3", "Sense input (bench)", FP["HDR3"], 200, 85, CB["J401"])
inst("J402", "CONN_3", "Sense logic (bench)", FP["HDR3"], 365, 85, CB["J402"])

inst("U501", "TCAN1051", "TCAN1051VDRQ1", FP["SOIC8"], 250, 175, CB["U501"])
inst("C501", "C", "100nF/16V", FP["RADIAL"], 220, 200, CB["C501"])
inst("C502", "C", "100nF/16V", FP["RADIAL"], 250, 200, CB["C502"])
inst("R501", "R", "1k", FP["AXIAL"], 290, 175, CB["R501"])
inst("J501", "CONN_3", "BUS HEADER (bench)", FP["HDR3"], 205, 175, CB["J501"])
inst("J502", "CONN_2", "MCU RECEIVE (bench)", FP["HDR2"], 330, 175, CB["J502"])

# --- Carrier power tree (zone J) --------------------------------------
inst("J801", "CONN_6", "Vehicle Power DT6 (prov.)", "strijder:DEUTSCH_DT6_Header_TBD", 230, 250, {
    "1": "VBAT_RAW", "2": "VBAT_RAW", "3": "GND", "4": "GND", "5": "IGN_VEH", "6": "CHASSIS"})
inst("U701", "FRONTEND", "LM7480-Q1 front end (prov.)", "strijder:PLACEHOLDER_QFN-24", 285, 250, {
    "1": "VBAT_RAW", "2": "IGN_VEH", "3": "GND", "4": "VVEH_PROT", "5": "FE_FLT_N"})
inst("U702", "PWRPATH", "Ideal-diode power path (prov.)", "strijder:PLACEHOLDER_QFN-24", 340, 250, {
    "1": "VVEH_PROT", "2": "VPACK", "3": "GND", "4": "VSYS_CARRIER", "5": "PP_STAT"})
inst("U703", "CHARGER", "LiFePO4 charger BQ25756-class (prov.)", "strijder:PLACEHOLDER_QFN-32", 285, 285, {
    "1": "VVEH_PROT", "2": "GND", "3": "I2C_TELEM", "4": "VPACK", "5": "CHG_STAT"})
inst("J702", "CONN_4", "UPS pack 12.8V LiFePO4 ext BMS (prov.)", "strijder:PLACEHOLDER_PWR_CONN_4", 230, 285, {
    "1": "VPACK", "2": "GND", "3": "PACK_COMM", "4": "PACK_EN"})
inst("U704", "EFUSE", "eFuse SOM branch (prov.)", "strijder:PLACEHOLDER_SOT-23-6", 400, 235, {
    "1": "VSYS_CARRIER", "2": "EN_SOM", "3": "GND", "4": "V_SOM_BRANCH", "5": "FLT_SOM"})
inst("U705", "EFUSE", "eFuse COMe branch EVS (prov.)", "strijder:PLACEHOLDER_SOT-23-6", 400, 260, {
    "1": "VSYS_CARRIER", "2": "EN_COME", "3": "GND", "4": "V_COME_12V", "5": "FLT_COME"})
inst("U706", "EFUSE", "eFuse camera/PoC branch (prov.)", "strijder:PLACEHOLDER_SOT-23-6", 400, 285, {
    "1": "VSYS_CARRIER", "2": "EN_CAM", "3": "GND", "4": "V_CAM_POC", "5": "FLT_CAM"})
inst("U707", "EFUSE", "eFuse display branch (prov.)", "strijder:PLACEHOLDER_SOT-23-6", 400, 310, {
    "1": "VSYS_CARRIER", "2": "EN_DISP", "3": "GND", "4": "V_DISP", "5": "FLT_DISP"})
inst("U708", "EFUSE", "eFuse comms/IO branch (prov.)", "strijder:PLACEHOLDER_SOT-23-6", 400, 335, {
    "1": "VSYS_CARRIER", "2": "EN_IO", "3": "GND", "4": "V_IO_BRANCH", "5": "FLT_IO"})
inst("U710", "BUCK", "Buck 5V/10A SOM rail (prov.)", "strijder:PLACEHOLDER_QFN-32", 455, 235, {
    "1": "V_SOM_BRANCH", "2": "EN_SOM", "3": "GND", "4": "+5V_SOM", "5": "PG_SOM"})
inst("U711", "BUCK", "Buck 3V3 logic rail (prov.)", "strijder:PLACEHOLDER_QFN-32", 455, 265, {
    "1": "V_IO_BRANCH", "2": "EN_IO", "3": "GND", "4": "+3V3_SYS", "5": "PG_3V3"})
inst("U712", "TELEM", "INA3221 telemetry (prov.)", "strijder:PLACEHOLDER_QFN-24", 455, 300, {
    "1": "+3V3_SYS", "2": "GND", "3": "I2C_TELEM",
    "4": "V_SOM_BRANCH", "5": "V_COME_12V", "6": "V_CAM_POC"})

# --- SOM domain (zone F) ----------------------------------------------
inst("J601", "SOM_ORIN", "Jetson Orin Nano 2 / NX SODIMM-260", "strijder:SODIMM-260_Socket_TBD", 545, 70, {
    "1": "+5V_SOM", "2": "GND", "3": "SOM_POWER_EN", "4": "SOM_RESET_N",
    "5": "SOM_RECOVERY_N", "6": "SOM_SHUTDOWN_REQ_N", "7": "SOM_SLEEP_WAKE_N",
    "8": "SOM_DBG_TX", "9": "SOM_DBG_RX", "10": "UART_SOM_TX", "11": "UART_SOM_RX",
    "12": "I2C_CAM", "13": "FAN_PWM", "14": "FAN_TACH",
    "20": "NVME1_TX", "21": "NVME1_RX", "22": "NVME1_REFCLK", "23": "NVME1_RST_N",
    "24": "NVME1_CLKREQ_N",
    "25": "NVME2_TX", "26": "NVME2_RX", "27": "NVME2_REFCLK", "28": "NVME2_RST_N",
    "29": "NVME2_CLKREQ_N",
    "30": "CSI_DES_PORT0", "31": "CSI_DES_PORT1",
    "32": "SOM_USB2", "33": "SOM_USB3", "34": "SOM_GBE_MDI", "35": "SOM_DP0"})
inst("J620", "M2_MKEY", "M.2 2280 NVMe evidence 1 (<=8TB)", "strijder:M2_2280_Socket_TBD", 630, 45, {
    "1": "+3V3_SYS", "2": "GND", "3": "NVME1_RST_N", "4": "NVME1_CLKREQ_N",
    "5": "NVME1_WAKE_N", "10": "NVME1_TX", "11": "NVME1_RX", "12": "NVME1_REFCLK",
    "13": "NVME1_DEVSLP", "14": "NVME1_LED_N"})
inst("J621", "M2_MKEY", "M.2 2280 NVMe evidence 2 (<=8TB)", "strijder:M2_2280_Socket_TBD", 630, 90, {
    "1": "+3V3_SYS", "2": "GND", "3": "NVME2_RST_N", "4": "NVME2_CLKREQ_N",
    "5": "NVME2_WAKE_N", "10": "NVME2_TX", "11": "NVME2_RX", "12": "NVME2_REFCLK",
    "13": "NVME2_DEVSLP", "14": "NVME2_LED_N"})
inst("J622", "FAN_HDR", "SOM fan", FP["HDR4"], 630, 130, {
    "1": "GND", "2": "V_SOM_BRANCH", "3": "FAN_TACH", "4": "FAN_PWM"})
inst("J623", "SWD_HDR", "SOM debug UART/service", FP["HDR5"], 630, 155, {
    "1": "+3V3_SYS", "2": "GND", "3": "SOM_DBG_TX", "4": "SOM_DBG_RX", "5": "SOM_RECOVERY_N"})

# --- EVS Windows domain (zone G) --------------------------------------
inst("J610", "COME_T6", "COM Express Compact T6 x86 (EVS only)", "strijder:COMe_AB_CD_440_TBD", 545, 220, {
    "1": "V_COME_12V", "2": "GND", "3": "COME_PWR_OK", "4": "COME_PWRBTN_N",
    "5": "COME_RESET_N", "6": "COME_SUS_S3_N", "7": "COME_SUS_S5_N", "8": "COME_WDT",
    "9": "I2C_TELEM", "10": "I2C_TELEM_DAT", "11": "COME_SPI_BIOS", "12": "COME_FAN_PWM",
    "20": "WNVME_PCIE_X4", "21": "COME_PCIE_B_X1", "22": "CAD_DP0", "23": "COME_EDP",
    "24": "CAD_USB3_0", "25": "CAD_USB3_1", "26": "CAD_USB2_0", "27": "COME_USB2_1",
    "28": "CAD_GBE_MDI", "29": "COME_SATA0", "30": "CAD_HDA", "31": "COME_THRM_N"})
inst("J612", "M2_MKEY", "M.2 2280 NVMe Windows (<=1TB, EVS)", "strijder:M2_2280_Socket_TBD", 630, 195, {
    "1": "+3V3_SYS", "2": "GND", "3": "WNVME_RST_N", "4": "WNVME_CLKREQ_N",
    "5": "WNVME_WAKE_N", "10": "WNVME_PCIE_X4", "11": "WNVME_PCIE_RX", "12": "WNVME_REFCLK",
    "13": "WNVME_DEVSLP", "14": "WNVME_LED_N"})

# --- Camera domain (zone H) -------------------------------------------
inst("U650", "GMSL_DESER4", "GMSL2 quad deser MAX96712-class (prov.)", "strijder:PLACEHOLDER_QFN-64", 480, 400, {
    "1": "+3V3_SYS", "2": "GND", "3": "CAM_COAX_A", "4": "CAM_COAX_B",
    "5": "CAM_COAX_C", "6": "CAM_COAX_D", "7": "DES_PWDN_N",
    "10": "CSI_DES_PORT0", "11": "CSI_DES_PORT1", "12": "I2C_CAM",
    "13": "DES_LOCK_N", "14": "DES_ERRB_N"})
inst("U651", "POC_QUAD", "PoC power MAX20087-class (prov.)", "strijder:PLACEHOLDER_QFN-24", 480, 445, {
    "1": "V_CAM_POC", "2": "GND", "3": "EN_CAM", "4": "I2C_CAM",
    "10": "CAM_COAX_A", "11": "CAM_COAX_B", "12": "CAM_COAX_C", "13": "CAM_COAX_D"})
for i, letter in enumerate("ABCD"):
    inst(f"J65{i}", "FAKRA", f"FAKRA Cam{i+1} (link {letter})", "strijder:FAKRA_SMT_TBD",
         560, 390 + i * 25, {"1": f"CAM_COAX_{letter}", "2": "CHASSIS"})
inst("U652", "GMSL_SER", "Aux display serializer MAX96717-class (prov.)", "strijder:PLACEHOLDER_QFN-32", 480, 490, {
    "1": "+3V3_SYS", "2": "GND", "3": "SOM_DP0", "4": "I2C_CAM", "10": "AUXDISP_GMSL"})

# --- Vehicle I/O domain (zone K, x 200-420 y 320-560) ------------------
inst("U730", "IOMCU", "STM32G474 vehicle-I/O MCU (prov.)", "strijder:PLACEHOLDER_LQFP-48", 260, 380, {
    "1": "+3V3_SYS", "2": "GND", "3": "MCU_NRST", "4": "MCU_BOOT0",
    "5": "MCU_SWDIO", "6": "MCU_SWCLK", "7": "MCU_WDI", "8": "UART_SOM_RX",
    "9": "UART_SOM_TX", "10": "I2C_TELEM",
    "20": "CAN_RX", "21": "IGN_N", "22": "SEL_N", "23": "BR_EN",
    "24": "RS485_RO", "25": "RS485_DI", "26": "RS485_DIR", "27": "ILK_EN",
    "28": "ILK_FB", "29": "LC_TX", "30": "LC_RX", "31": "LC_FLT",
    "32": "LC_EN", "33": "SENSE_BUS", "34": "AUX_AIN", "35": "EVENT_MARK"})
inst("U732", "WATCHDOG", "TPS3430 hardware watchdog (prov.)", "strijder:PLACEHOLDER_SOT-23-6", 330, 355, {
    "1": "+3V3_SYS", "2": "GND", "3": "MCU_WDI", "4": "MCU_NRST"})
inst("U735", "RS485", "THVD1450 validator RS-485 (prov.)", "strijder:PLACEHOLDER_SOIC-8", 330, 385, {
    "1": "+3V3_SYS", "2": "GND", "3": "RS485_RO", "4": "RS485_DI", "5": "RS485_DIR",
    "6": "VAL_485_A", "7": "VAL_485_B"})
inst("U733", "SENSE8", "Protected sense array, CB-01 opto channel x8 (prov.)", "strijder:PLACEHOLDER_MODULE", 330, 425, {
    "1": "+3V3_SYS", "2": "GND", "3": "SEL_IN0_RAW", "4": "SEL_IN1_RAW",
    "5": "SEL_IN2_RAW", "6": "SEL_IN3_RAW", "10": "SENSE_BUS",
    "11": "SEL_IN4_RAW", "12": "SEL_IN5_RAW", "13": "SEL_IN6_RAW", "14": "ILK_FB_RAW"})
inst("U734", "LSDRV", "Interlock protected driver (prov.)", "strijder:PLACEHOLDER_SOIC-8", 330, 465, {
    "1": "V_IO_BRANCH", "2": "GND", "3": "ILK_EN", "4": "ILK_DRV", "5": "ILK_FB_RAW"})
inst("J624", "SWD_HDR", "IOMCU SWD", FP["HDR5"], 200, 355, {
    "1": "+3V3_SYS", "2": "GND", "3": "MCU_SWDIO", "4": "MCU_SWCLK", "5": "MCU_NRST"})

# --- Vehicle connector wall (zone I) ----------------------------------
inst("J802", "CONN_6", "Validator DTM6 (prov.)", "strijder:DEUTSCH_DTM6_Header_TBD", 660, 320, {
    "1": "V_IO_BRANCH", "2": "GND", "3": "VAL_485_A", "4": "VAL_485_B",
    "5": "VAL_PRESENT", "6": "NC_RSVD"})
inst("J803", "CONN_6", "CAN/OBD/Sense DTM6 (prov.)", "strijder:DEUTSCH_DTM6_Header_TBD", 660, 350, {
    "1": "CAN_H", "2": "CAN_L", "3": "GND", "4": "CHASSIS",
    "5": "IGN_RAW", "6": "NC_RSVD"})
inst("J804", "CONN_3", "Aux sensor DTM3 (prov.)", "strijder:DEUTSCH_DTM3_Header_TBD", 660, 380, {
    "1": "V_IO_BRANCH", "2": "GND", "3": "AUX_AIN"})
inst("J805", "CONN_4", "Interlock DTM4 (prov.)", "strijder:DEUTSCH_DTM4_Header_TBD", 660, 405, {
    "1": "V_IO_BRANCH", "2": "GND", "3": "ILK_DRV", "4": "ILK_FB_RAW"})
inst("J806", "CONN_16", "Lighting controller 16-pos (prov., electronics pwr only)",
     "strijder:DEUTSCH_HDP_16_Header_TBD", 660, 450, {
    "1": "V_IO_BRANCH", "2": "GND", "3": "LC_TX", "4": "LC_RX", "5": "LC_FLT",
    "6": "LC_EN", "7": "NC_RSVD", "8": "NC_RSVD", "9": "NC_RSVD", "10": "NC_RSVD",
    "11": "NC_RSVD", "12": "NC_RSVD", "13": "NC_RSVD", "14": "NC_RSVD",
    "15": "NC_RSVD", "16": "CHASSIS"})
inst("J807", "CONN_16", "Lighting selector 16-pos (prov.)",
     "strijder:DEUTSCH_HDP_16_Header_TBD", 660, 500, {
    "1": "V_IO_BRANCH", "2": "GND", "3": "SEL_RAW", "4": "SEL_IN0_RAW",
    "5": "SEL_IN1_RAW", "6": "SEL_IN2_RAW", "7": "SEL_IN3_RAW", "8": "SEL_IN4_RAW",
    "9": "SEL_IN5_RAW", "10": "SEL_IN6_RAW", "11": "NC_RSVD", "12": "NC_RSVD",
    "13": "NC_RSVD", "14": "NC_RSVD", "15": "NC_RSVD", "16": "CHASSIS"})
inst("J808", "CONN_20", "Main dashcam head HDP20 (prov.)", "strijder:DEUTSCH_HDP20_Header_TBD", 750, 350, {
    "1": "V_DISP", "2": "V_DISP", "3": "GND", "4": "GND",
    "5": "CAM_COAX_A", "6": "CHASSIS", "7": "HEAD_UART_TX", "8": "HEAD_UART_RX",
    "9": "EVENT_MARK", "10": "HEAD_STATUS", "11": "HEAD_MIC_P", "12": "HEAD_MIC_N",
    "13": "I2C_CAM", "14": "I2C_CAM_DAT", "15": "NC_RSVD", "16": "NC_RSVD",
    "17": "NC_RSVD", "18": "NC_RSVD", "19": "NC_RSVD", "20": "NC_RSVD"})
inst("J809", "CONN_20", "CAD/Windows display 40-pos, logical subset (prov., EVS)",
     "strijder:PLACEHOLDER_CONN40", 750, 420, {
    "1": "V_DISP", "2": "V_DISP", "3": "GND", "4": "GND",
    "5": "CAD_DP0", "6": "CAD_USB3_0", "7": "CAD_USB3_1", "8": "CAD_USB2_0",
    "9": "CAD_GBE_MDI", "10": "CAD_HDA", "11": "CAD_BKLT_EN", "12": "CAD_BKLT_PWM",
    "13": "COME_PWRBTN_N", "14": "I2C_TELEM", "15": "I2C_TELEM_DAT", "16": "CHASSIS",
    "17": "NC_RSVD", "18": "NC_RSVD", "19": "NC_RSVD", "20": "NC_RSVD"})
inst("J810", "CONN_8", "Aux camera display 8-pos (prov.)", "strijder:PLACEHOLDER_CONN8", 750, 480, {
    "1": "V_DISP", "2": "GND", "3": "AUXDISP_GMSL", "4": "CHASSIS",
    "5": "AUXDISP_CTRL", "6": "NC_RSVD", "7": "NC_RSVD", "8": "NC_RSVD"})

# --- Comms domain (zone L, x 640-820 y 20-300 right of SOM) ------------
inst("J630", "M2_BKEY", "M.2 B-key LTE modem (prov.)", "strijder:M2_3042_Socket_TBD", 720, 60, {
    "1": "+3V3_SYS", "2": "GND", "3": "WWAN_DISABLE_N", "4": "WWAN_RESET_N",
    "5": "SOM_USB2", "10": "WWAN_USB3", "11": "SIM_VCC", "12": "SIM_RST",
    "13": "SIM_CLK", "14": "SIM_IO", "15": "LTE_ANT_MAIN", "16": "LTE_ANT_DIV"})
inst("J631", "SIM_SOCKET", "SIM socket (prov.)", "strijder:SIM_Socket_TBD", 790, 60, {
    "1": "SIM_VCC", "2": "SIM_RST", "3": "SIM_CLK", "4": "SIM_IO",
    "5": "GND", "6": "SIM_DET"})
inst("J632", "M2_EKEY", "M.2 E-key WiFi/BT (prov.)", "strijder:M2_2230_Socket_TBD", 720, 110, {
    "1": "+3V3_SYS", "2": "GND", "3": "WLAN_DISABLE_N", "4": "BT_DISABLE_N",
    "10": "WLAN_PCIE_TX", "11": "WLAN_PCIE_RX", "12": "WLAN_REFCLK",
    "13": "WLAN_USB2", "14": "WLAN_ANT0", "15": "WLAN_ANT1"})
inst("U640", "GNSS_MOD", "GNSS u-blox NEO-M9N-class (prov.)", "strijder:PLACEHOLDER_MODULE", 720, 160, {
    "1": "+3V3_SYS", "2": "GND", "3": "GNSS_RF", "4": "GNSS_VBCKP",
    "5": "GNSS_TX", "6": "GNSS_RX", "7": "GNSS_PPS", "8": "GNSS_RESET_N"})
inst("J641", "SMA", "SMA GNSS antenna", "strijder:SMA_Edge_TBD", 790, 160, {
    "1": "GNSS_RF", "2": "CHASSIS"})
inst("J642", "SMA", "SMA_LTE main (Gen A)", "strijder:SMA_Edge_TBD", 790, 195, {
    "1": "LTE_ANT_MAIN", "2": "CHASSIS"})
inst("J643", "SMA", "SMA LTE diversity (prov.)", "strijder:SMA_Edge_TBD", 790, 225, {
    "1": "LTE_ANT_DIV", "2": "CHASSIS"})

ZONE_TEXTS = [
    (40, 40, "CB-01 REV B BENCH CORE (verbatim from docs/engineering/circuit-base; pin-accurate)"),
    (40, 128, "CB-01 rails: bench linear supply -- production replacement = U710/U711 branch rails"),
    (40, 200, "CB-01 protected peripheral switch"),
    (200, 40, "CB-01 opto sense inputs (IGN/SEL)"),
    (205, 160, "CB-01 silent CAN (receive-only by design)"),
    (200, 235, "CARRIER POWER TREE (provisional parts; see README + POWER_AND_PROTECTION.md)"),
    (480, 30, "JETSON SOM DOMAIN - Orin Nano 2 (Pro) / Orin NX (EVS); SODIMM-260."),
    (480, 32.5, ""),
    (480, 205, "WINDOWS DOMAIN (EVS ONLY - DNP on Pro): COM Express Compact Type 6"),
    (455, 375, "CAMERA DOMAIN: GMSL2 quad link, PoC. Link A shared: main head OR FAKRA Cam1"),
    (200, 335, "VEHICLE I/O DOMAIN: deterministic MCU, watchdog, protected interfaces"),
    (645, 305, "VEHICLE CONNECTOR WALL (DEUTSCH families per CONNECTORS_AND_HARNESS.md)"),
    (700, 30, "COMMS: LTE M.2 B-key + SIM, WiFi/BT E-key, GNSS. RF cavity mapping TBD"),
    (40, 560, "All (prov.) parts are provisional selections per dossier rule 6 (no invented certainty)."),
    (40, 570, "Logical-interface blocks (SOM/COMe/M.2/deser) require cavity-level pin mapping from"),
    (40, 580, "vendor design guides before layout release. See hardware/strijder-carrier/README.md."),
]


# ------------------------------------------------------------ sch emit
def emit_symbol_def(name):
    s = SYMBOLS[name]
    ref = s["ref"]
    lines = []
    lines.append(f'    (symbol "strijder:{name}" (pin_names (offset 0.254)) (in_bom yes) (on_board yes)')
    lines.append(f'      (property "Reference" "{ref}" (id 0) (at 0 {f(s["n"] * 1.27 + 1.27)} 0) (effects (font (size 1.27 1.27))))')
    lines.append(f'      (property "Value" "{name}" (id 1) (at 0 {f(-(s["n"] * 1.27 + 1.27))} 0) (effects (font (size 1.27 1.27))))')
    lines.append('      (property "Footprint" "" (id 2) (at 0 0 0) (effects (font (size 1.27 1.27)) hide))')
    lines.append('      (property "Datasheet" "" (id 3) (at 0 0 0) (effects (font (size 1.27 1.27)) hide))')
    top = f(s["n"] * 1.27)
    bot = f(-s["n"] * 1.27)
    hw = f(s["halfw"])
    lines.append(f'      (symbol "{name}_0_1"')
    lines.append(f'        (rectangle (start -{hw} {top}) (end {hw} {bot}) (stroke (width 0.254) (type default) (color 0 0 0 0)) (fill (type background)))')
    lines.append('      )')
    lines.append(f'      (symbol "{name}_1_1"')
    offs = pin_offsets(SYMBOLS[name])
    for num, nm in s["left"] + s["right"]:
        px, py = offs[num]
        ang = 0 if px < 0 else 180
        lines.append(f'        (pin passive line (at {f(px)} {f(py)} {ang}) (length 2.54)'
                     f' (name "{nm}" (effects (font (size 1.02 1.02))))'
                     f' (number "{num}" (effects (font (size 1.02 1.02)))))')
    lines.append('      )')
    lines.append('    )')
    return "\n".join(lines)


def emit_schematic():
    used = sorted({i["symbol"] for i in INSTANCES})
    parts = []
    parts.append('(kicad_sch (version 20211123) (generator strijder_generate_project)')
    parts.append(f'  (uuid "{uid("sch-root")}")')
    parts.append('  (paper "A1")')
    parts.append('  (title_block (title "Strijder Vision Pro/EVS modular carrier - concept capture")'
                 ' (date "2026-09-09") (rev "A0") (company "Strijder")'
                 ' (comment 1 "CB-01 rev B bench core reproduced pin-for-pin; carrier blocks logical/provisional")'
                 ' (comment 2 "One PCB, two populations: Vision Pro / Vision EVS - see README population matrix"))')
    parts.append('  (lib_symbols')
    for name in used:
        parts.append(emit_symbol_def(name))
    parts.append('  )')

    inst_refs = []
    for it in INSTANCES:
        s = SYMBOLS[it["symbol"]]
        su = uid("sym", it["ref"])
        x, y = it["x"], it["y"]
        parts.append(f'  (symbol (lib_id "strijder:{it["symbol"]}") (at {f(x)} {f(y)} 0) (unit 1)')
        parts.append('    (in_bom yes) (on_board yes)')
        parts.append(f'    (uuid "{su}")')
        parts.append(f'    (property "Reference" "{it["ref"]}" (id 0) (at {f(x)} {f(y - s["n"] * 1.27 - 2.54)} 0) (effects (font (size 1.27 1.27))))')
        val = it["value"].replace('"', "'")
        parts.append(f'    (property "Value" "{val}" (id 1) (at {f(x)} {f(y + s["n"] * 1.27 + 2.54)} 0) (effects (font (size 1.02 1.02))))')
        parts.append(f'    (property "Footprint" "{it["footprint"]}" (id 2) (at {f(x)} {f(y)} 0) (effects (font (size 1.27 1.27)) hide))')
        parts.append(f'    (property "Datasheet" "" (id 3) (at {f(x)} {f(y)} 0) (effects (font (size 1.27 1.27)) hide))')
        for num, _nm in s["left"] + s["right"]:
            parts.append(f'    (pin "{num}" (uuid "{uid("pin", it["ref"], num)}"))')
        parts.append('  )')
        inst_refs.append((su, it["ref"], val, it["footprint"]))

        offs = pin_offsets(s)
        for num, _nm in s["left"] + s["right"]:
            net = it["nets"].get(num)
            if not net or net == "NC_RSVD":
                continue
            px, py = offs[num]
            wx, wy = x + px, y - py
            if px < 0:
                ang, just = 180, "right"
            else:
                ang, just = 0, "left"
            parts.append(f'  (global_label "{net}" (shape passive) (at {f(wx)} {f(wy)} {ang})'
                         f' (effects (font (size 1.02 1.02)) (justify {just}))'
                         f' (uuid "{uid("lbl", it["ref"], num)}"))')

    for tx, ty, txt in ZONE_TEXTS:
        if not txt:
            continue
        t = txt.replace('"', "'")
        parts.append(f'  (text "{t}" (at {f(tx)} {f(ty)} 0)'
                     f' (effects (font (size 2 2) bold) (justify left bottom))'
                     f' (uuid "{uid("txt", tx, ty)}"))')

    parts.append('  (sheet_instances (path "/" (page "1")))')
    parts.append('  (symbol_instances')
    for su, ref, val, fp_ in inst_refs:
        parts.append(f'    (path "/{su}" (reference "{ref}") (unit 1) (value "{val}") (footprint "{fp_}"))')
    parts.append('  )')
    parts.append(')')
    return "\n".join(parts) + "\n"


# ------------------------------------------------------------ pcb emit
FOOTPRINT_DEFS = {}


def fpdef(name, pads, outline_wh, silk=None, attr="through_hole"):
    """pads: list of (padnum, kind, shape, x, y, sx, sy, drill)."""
    FOOTPRINT_DEFS[name] = dict(pads=pads, wh=outline_wh, attr=attr)


def two_pad_tht(pitch, drill=1.0, size=1.8):
    h = pitch / 2
    return [("1", "thru_hole", "circle", -h, 0, size, size, drill),
            ("2", "thru_hole", "circle", h, 0, size, size, drill)]


def row_tht(n, pitch=2.54, drill=1.0, size=1.7, start=1):
    x0 = -(n - 1) * pitch / 2
    return [(str(start + i), "thru_hole", "rect" if i == 0 else "circle",
             x0 + i * pitch, 0, size, size, drill) for i in range(n)]


def grid_tht(n, cols, pitch=2.54, drill=1.0, size=1.7):
    rows = (n + cols - 1) // cols
    out = []
    for i in range(n):
        r, c = divmod(i, cols)
        out.append((str(i + 1), "thru_hole", "rect" if i == 0 else "circle",
                    (c - (cols - 1) / 2) * pitch, (r - (rows - 1) / 2) * pitch,
                    size, size, drill))
    return out


def smd_dual(n, pitch, span, w=0.6, h=1.5):
    half = n // 2
    out = []
    y0 = -(half - 1) * pitch / 2
    for i in range(half):
        out.append((str(i + 1), "smd", "rect", -span / 2, y0 + i * pitch, h, w, None))
    for i in range(half):
        out.append((str(n - i), "smd", "rect", span / 2, y0 + i * pitch, h, w, None))
    return out


fpdef("strijder:R_Axial_P10.16mm", two_pad_tht(10.16, 0.9, 1.6), (12.5, 3))
fpdef("strijder:C_Radial_P5.00mm", two_pad_tht(5.0, 0.9, 1.6), (8, 8))
fpdef("strijder:D_DO-201AD_P12.70mm", [("A", "thru_hole", "circle", -6.35, 0, 2.4, 2.4, 1.4),
                                       ("K", "thru_hole", "rect", 6.35, 0, 2.4, 2.4, 1.4)], (15, 5.5))
fpdef("strijder:D_DO-41_P10.16mm", [("A", "thru_hole", "circle", -5.08, 0, 1.9, 1.9, 1.1),
                                    ("K", "thru_hole", "rect", 5.08, 0, 1.9, 1.9, 1.1)], (12, 3))
fpdef("strijder:D_DO-35_P7.62mm", [("A", "thru_hole", "circle", -3.81, 0, 1.6, 1.6, 0.8),
                                   ("K", "thru_hole", "rect", 3.81, 0, 1.6, 1.6, 0.8)], (9, 2.5))
fpdef("strijder:D_SMB", [("A", "smd", "rect", -2.2, 0, 2.2, 2.2, None),
                         ("K", "smd", "rect", 2.2, 0, 2.2, 2.2, None)], (6.5, 4), attr="smd")
fpdef("strijder:TO-220-3_Vertical", row_tht(3, 2.54, 1.1, 1.9), (10.2, 4.6))
fpdef("strijder:TO-92_Inline", row_tht(3, 1.27, 0.75, 1.2), (5.2, 4.2))
fpdef("strijder:DIP-4_W7.62mm", [("1", "thru_hole", "rect", -3.81, 1.27, 1.6, 1.6, 0.8),
                                 ("2", "thru_hole", "circle", -3.81, -1.27, 1.6, 1.6, 0.8),
                                 ("3", "thru_hole", "circle", 3.81, -1.27, 1.6, 1.6, 0.8),
                                 ("4", "thru_hole", "circle", 3.81, 1.27, 1.6, 1.6, 0.8)], (10, 6.5))
fpdef("strijder:SOIC-8_3.9x4.9mm_P1.27mm", smd_dual(8, 1.27, 5.4), (4, 5), attr="smd")
fpdef("strijder:Fuseholder_Inline_TBD", two_pad_tht(22.0, 1.2, 2.2), (26, 8))
fpdef("strijder:TestPoint_Pad_2.0mm", [("1", "smd", "circle", 0, 0, 2.0, 2.0, None)], (2.5, 2.5), attr="smd")
for n_ in (2, 3, 4, 5):
    fpdef(f"strijder:PinHeader_1x0{n_}_P2.54mm", row_tht(n_), ((n_ - 1) * 2.54 + 2.6, 2.6))
fpdef("strijder:DEUTSCH_DT6_Header_TBD", grid_tht(6, 3, 5.08, 1.6, 2.6), (22, 14))
fpdef("strijder:DEUTSCH_DTM3_Header_TBD", row_tht(3, 3.81, 1.2, 2.0), (14, 9))
fpdef("strijder:DEUTSCH_DTM4_Header_TBD", grid_tht(4, 2, 3.81, 1.2, 2.0), (12, 12))
fpdef("strijder:DEUTSCH_DTM6_Header_TBD", grid_tht(6, 3, 3.81, 1.2, 2.0), (16, 12))
fpdef("strijder:DEUTSCH_HDP_16_Header_TBD", grid_tht(16, 4, 3.0, 1.1, 1.8), (18, 18))
fpdef("strijder:DEUTSCH_HDP20_Header_TBD", grid_tht(20, 5, 3.0, 1.1, 1.8), (20, 18))
fpdef("strijder:PLACEHOLDER_CONN40", grid_tht(20, 10, 2.0, 0.8, 1.4), (26, 10))
fpdef("strijder:PLACEHOLDER_CONN8", grid_tht(8, 4, 2.0, 0.8, 1.4), (12, 8))
fpdef("strijder:PLACEHOLDER_PWR_CONN_4", row_tht(4, 4.2, 1.8, 2.8), (20, 10))
fpdef("strijder:SODIMM-260_Socket_TBD", [("MP1", "thru_hole", "circle", -39, 0, 3, 3, 2),
                                         ("MP2", "thru_hole", "circle", 39, 0, 3, 3, 2)], (82, 48))
fpdef("strijder:COMe_AB_CD_440_TBD", [("MP1", "thru_hole", "circle", -45, 0, 3, 3, 2),
                                      ("MP2", "thru_hole", "circle", 45, 0, 3, 3, 2)], (96, 96))
fpdef("strijder:M2_2280_Socket_TBD", [("MP1", "thru_hole", "circle", 0, -35, 2.4, 2.4, 1.6),
                                      ("MP2", "thru_hole", "circle", 0, 40, 2.4, 2.4, 1.6)], (24, 84))
fpdef("strijder:M2_3042_Socket_TBD", [("MP1", "thru_hole", "circle", 0, -18, 2.4, 2.4, 1.6),
                                      ("MP2", "thru_hole", "circle", 0, 22, 2.4, 2.4, 1.6)], (32, 46))
fpdef("strijder:M2_2230_Socket_TBD", [("MP1", "thru_hole", "circle", 0, -12, 2.4, 2.4, 1.6),
                                      ("MP2", "thru_hole", "circle", 0, 16, 2.4, 2.4, 1.6)], (24, 34))
fpdef("strijder:SIM_Socket_TBD", grid_tht(6, 3, 2.54, 0.9, 1.5), (17, 16))
fpdef("strijder:FAKRA_SMT_TBD", [("1", "smd", "rect", 0, 0, 1.2, 1.2, None),
                                 ("2", "smd", "rect", -2.5, 2.5, 1.6, 1.6, None),
                                 ("2", "smd", "rect", 2.5, 2.5, 1.6, 1.6, None)], (10, 12), attr="smd")
fpdef("strijder:SMA_Edge_TBD", [("1", "thru_hole", "circle", 0, 0, 2.0, 2.0, 1.3),
                                ("2", "thru_hole", "circle", -2.54, 2.54, 2.0, 2.0, 1.3),
                                ("2", "thru_hole", "circle", 2.54, 2.54, 2.0, 2.0, 1.3)], (8, 8))
fpdef("strijder:PLACEHOLDER_QFN-24", smd_dual(24, 0.5, 4.6, 0.28, 0.8), (5, 5), attr="smd")
fpdef("strijder:PLACEHOLDER_QFN-32", smd_dual(32, 0.5, 5.6, 0.28, 0.8), (6, 6), attr="smd")
fpdef("strijder:PLACEHOLDER_QFN-64", smd_dual(64, 0.5, 9.6, 0.28, 0.8), (10, 10), attr="smd")
fpdef("strijder:PLACEHOLDER_SOT-23-6", smd_dual(6, 0.95, 2.9, 0.6, 1.1), (3.2, 3.2), attr="smd")
fpdef("strijder:PLACEHOLDER_SOIC-8", smd_dual(8, 1.27, 5.4), (4, 5), attr="smd")
fpdef("strijder:PLACEHOLDER_LQFP-48", smd_dual(48, 0.5, 8.8, 0.3, 1.2), (9.5, 9.5), attr="smd")
fpdef("strijder:PLACEHOLDER_MODULE", grid_tht(8, 4, 2.54, 0.9, 1.5), (18, 14))
fpdef("strijder:MountingHole_M4",
      [("", "np_thru_hole", "circle", 0, 0, 4.3, 4.3, 4.3)], (8, 8))

# board coords: outline (20,20)-(220,160) -> 200 x 140 mm
# ref, x, y, rot  (refs match schematic; nets bind via update-from-schematic)
PCB_PLACE = [
    ("J801", 32, 42, 90), ("J702", 32, 64, 90), ("J802", 32, 84, 90),
    ("J803", 32, 102, 90), ("J804", 32, 118, 90), ("J805", 32, 134, 90),
    ("J806", 50, 148, 0), ("J807", 72, 148, 0), ("J808", 96, 148, 0),
    ("J809", 122, 148, 0), ("J810", 146, 148, 0),
    ("J650", 62, 26, 0), ("J651", 76, 26, 0), ("J652", 90, 26, 0), ("J653", 104, 26, 0),
    ("J641", 190, 26, 0), ("J642", 201, 26, 0), ("J643", 212, 26, 0),
    ("J601", 100, 62, 0),
    ("J610", 170, 108, 0),
    ("J620", 138, 55, 0), ("J621", 155, 55, 0), ("J612", 205, 108, 0),
    ("J630", 190, 55, 0), ("J631", 213, 45, 0), ("J632", 190, 82, 0),
    ("U640", 208, 70, 0),
    ("U650", 80, 40, 0), ("U651", 62, 40, 0), ("U652", 118, 40, 0),
    ("U701", 48, 55, 0), ("U702", 48, 70, 0), ("U703", 48, 85, 0),
    ("U704", 60, 55, 0), ("U705", 60, 62, 0), ("U706", 60, 69, 0),
    ("U707", 60, 76, 0), ("U708", 60, 83, 0),
    ("U710", 70, 55, 0), ("U711", 70, 66, 0), ("U712", 70, 78, 0),
    ("U730", 60, 105, 0), ("U732", 74, 100, 0), ("U733", 74, 112, 0),
    ("U734", 88, 100, 0), ("U735", 88, 110, 0),
    ("J622", 130, 80, 0), ("J623", 130, 88, 0), ("J624", 60, 120, 0),
    # CB-01 bench-heritage subset, bottom-left service area
    ("J101", 46, 128, 0), ("J102", 56, 128, 0), ("F101", 70, 124, 0), ("F102", 70, 130, 0),
    ("D101", 92, 124, 0), ("D102", 92, 130, 0), ("D103", 106, 127, 0), ("C101", 114, 127, 0),
    ("TP101", 120, 122, 0), ("TP102", 120, 132, 0),
    ("U201", 130, 124, 0), ("C201", 138, 120, 0), ("C202", 143, 120, 0), ("C203", 148, 120, 0),
    ("D201", 140, 128, 0), ("U202", 152, 124, 0), ("C204", 153, 120, 0), ("C205", 158, 120, 0),
    ("F301", 96, 112, 0), ("Q301", 110, 112, 0), ("R301", 110, 117, 0), ("D301", 122, 117, 0),
    ("R302", 96, 118, 0), ("Q302", 104, 121, 0), ("R303", 112, 121, 0), ("R304", 120, 121, 0),
    ("J301", 130, 112, 0), ("J302", 130, 117, 0),
    ("R411", 138, 100, 0), ("R412", 148, 100, 0), ("U401", 158, 100, 0), ("D401", 148, 104, 0),
    ("R413", 166, 100, 0), ("C401", 171, 100, 0),
    ("R421", 138, 107, 0), ("R422", 148, 107, 0), ("U402", 158, 107, 0), ("D402", 148, 111, 0),
    ("R423", 166, 107, 0), ("C402", 171, 107, 0),
    ("J401", 130, 103, 0), ("J402", 176, 103, 0),
    ("U501", 96, 96, 0), ("C501", 90, 100, 0), ("C502", 104, 100, 0), ("R501", 104, 92, 0),
    ("J501", 86, 92, 0), ("J502", 112, 92, 0),
]

MOUNTING = [(25, 25), (215, 25), (25, 155), (215, 155), (120, 25), (120, 155)]

VALUES = {i["ref"]: (i["value"], i["footprint"]) for i in INSTANCES}


def emit_footprint(ref, x, y, rot):
    val, fpname = VALUES[ref]
    d = FOOTPRINT_DEFS[fpname]
    w, h = d["wh"]
    lines = []
    lines.append(f'  (footprint "{fpname}" (layer "F.Cu") (at {f(x)} {f(y)} {rot})')
    lines.append(f'    (attr {d["attr"]})')
    lines.append(f'    (fp_text reference "{ref}" (at 0 {f(-h / 2 - 1.2)}) (layer "F.SilkS") (effects (font (size 1 1) (thickness 0.15))))')
    v = val.replace('"', "'")
    lines.append(f'    (fp_text value "{v}" (at 0 {f(h / 2 + 1.2)}) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))')
    hw, hh = w / 2, h / 2
    for (x1, y1, x2, y2) in [(-hw, -hh, hw, -hh), (hw, -hh, hw, hh),
                             (hw, hh, -hw, hh), (-hw, hh, -hw, -hh)]:
        lines.append(f'    (fp_line (start {f(x1)} {f(y1)}) (end {f(x2)} {f(y2)}) (layer "F.Fab") (width 0.1))')
        lines.append(f'    (fp_line (start {f(x1 * 1.05)} {f(y1 * 1.05)}) (end {f(x2 * 1.05)} {f(y2 * 1.05)}) (layer "F.CrtYd") (width 0.05))')
    for (num, kind, shape, px, py, sx, sy, drill) in d["pads"]:
        drillpart = f' (drill {f(drill)})' if drill else ''
        layers = '"*.Cu" "*.Mask"' if kind != "smd" else '"F.Cu" "F.Paste" "F.Mask"'
        numq = f'"{num}"'
        lines.append(f'    (pad {numq} {kind} {shape} (at {f(px)} {f(py)} {rot}) (size {f(sx)} {f(sy)}){drillpart} (layers {layers}))')
    lines.append('  )')
    return "\n".join(lines)


def emit_pcb():
    parts = []
    parts.append('(kicad_pcb (version 20211014) (generator strijder_generate_project)')
    parts.append('  (general (thickness 2.0))')
    parts.append('  (paper "A3")')
    layer_lines = ['  (layers']
    layer_lines.append('    (0 "F.Cu" signal)')
    for i in range(1, 11):
        layer_lines.append(f'    ({i} "In{i}.Cu" signal)')
    layer_lines.append('    (31 "B.Cu" signal)')
    extra = [(32, "B.Adhes", "user", "B.Adhesive"), (33, "F.Adhes", "user", "F.Adhesive"),
             (34, "B.Paste", "user"), (35, "F.Paste", "user"),
             (36, "B.SilkS", "user", "B.Silkscreen"), (37, "F.SilkS", "user", "F.Silkscreen"),
             (38, "B.Mask", "user"), (39, "F.Mask", "user"),
             (40, "Dwgs.User", "user", "User.Drawings"), (41, "Cmts.User", "user", "User.Comments"),
             (42, "Eco1.User", "user", "User.Eco1"), (43, "Eco2.User", "user", "User.Eco2"),
             (44, "Edge.Cuts", "user"), (45, "Margin", "user"),
             (46, "B.CrtYd", "user", "B.Courtyard"), (47, "F.CrtYd", "user", "F.Courtyard"),
             (48, "B.Fab", "user"), (49, "F.Fab", "user")]
    for e in extra:
        if len(e) == 4:
            layer_lines.append(f'    ({e[0]} "{e[1]}" {e[2]} "{e[3]}")')
        else:
            layer_lines.append(f'    ({e[0]} "{e[1]}" {e[2]})')
    layer_lines.append('  )')
    parts.append("\n".join(layer_lines))
    parts.append('  (setup (pad_to_mask_clearance 0))')
    parts.append('  (net 0 "")')
    for ref, x, y, rot in PCB_PLACE:
        parts.append(emit_footprint(ref, x, y, rot))
    for i, (mx, my) in enumerate(MOUNTING):
        d = FOOTPRINT_DEFS["strijder:MountingHole_M4"]
        parts.append(f'  (footprint "strijder:MountingHole_M4" (layer "F.Cu") (at {f(mx)} {f(my)} 0)')
        parts.append('    (attr through_hole exclude_from_pos_files exclude_from_bom)')
        parts.append(f'    (fp_text reference "H{i + 1}" (at 0 -5) (layer "F.SilkS") (effects (font (size 1 1) (thickness 0.15))))')
        parts.append('    (fp_text value "M4" (at 0 5) (layer "F.Fab") (effects (font (size 1 1) (thickness 0.15))))')
        parts.append('    (pad "" np_thru_hole circle (at 0 0) (size 4.3 4.3) (drill 4.3) (layers "*.Cu" "*.Mask"))')
        parts.append('  )')
    parts.append('  (gr_rect (start 20 20) (end 220 160) (layer "Edge.Cuts") (width 0.15))')
    notes = [
        (22, 165, "Strijder Vision Pro/EVS modular carrier - concept placement rev A0. 200x140mm, 12-layer target."),
        (22, 170, "NOT ROUTED. Placement + connector wall only. Nets bind via 'Update PCB from Schematic'."),
        (22, 175, "Placeholder footprints (TBD suffix) must be replaced with manufacturer footprints before layout."),
        (22, 180, "EVS-only population: J610 COMe, J612, J809. Lighting current does NOT cross this board (dossier F-010)."),
    ]
    for nx, ny, t in notes:
        parts.append(f'  (gr_text "{t}" (at {f(nx)} {f(ny)}) (layer "Cmts.User")'
                     f' (effects (font (size 1.5 1.5) (thickness 0.3)) (justify left)))')
    parts.append(')')
    return "\n".join(parts) + "\n"


def emit_pro():
    def nc(name, clearance, track, via, viadrill, dpw=None, dpg=None):
        d = {"name": name, "clearance": clearance, "track_width": track,
             "via_diameter": via, "via_drill": viadrill,
             "microvia_diameter": 0.3, "microvia_drill": 0.1,
             "diff_pair_width": dpw or track, "diff_pair_gap": dpg or clearance,
             "diff_pair_via_gap": 0.25,
             "line_style": 0, "wire_width": 6, "bus_width": 12,
             "pcb_color": "rgba(0, 0, 0, 0.000)", "schematic_color": "rgba(0, 0, 0, 0.000)"}
        return d

    pro = {
        "meta": {"filename": "strijder-carrier.kicad_pro", "version": 1},
        "board": {"design_settings": {"defaults": {}, "rules": {
            "min_copper_edge_clearance": 0.5,
            "min_track_width": 0.09,
            "min_via_diameter": 0.45,
        }}},
        "net_settings": {
            "meta": {"version": 3},
            "classes": [
                nc("Default", 0.2, 0.25, 0.6, 0.3),
                nc("Power_Main", 0.5, 2.0, 1.2, 0.6),
                nc("Power_Branch", 0.3, 1.0, 0.8, 0.4),
                nc("Diff_90_USB_PCIe", 0.15, 0.11, 0.45, 0.2, 0.11, 0.15),
                nc("Diff_100_CSI_ETH", 0.15, 0.1, 0.45, 0.2, 0.1, 0.17),
                nc("CAN_Diff_120", 0.3, 0.3, 0.6, 0.3, 0.3, 0.3),
                nc("GMSL_Coax_50", 0.3, 0.35, 0.45, 0.2),
            ],
        },
        "schematic": {"legacy_lib_dir": "", "legacy_lib_list": []},
        "sheets": [],
        "text_variables": {},
    }
    return json.dumps(pro, indent=2) + "\n"


def main():
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "strijder-carrier.kicad_sch"), "w") as fh:
        fh.write(emit_schematic())
    with open(os.path.join(OUT, "strijder-carrier.kicad_pcb"), "w") as fh:
        fh.write(emit_pcb())
    with open(os.path.join(OUT, "strijder-carrier.kicad_pro"), "w") as fh:
        fh.write(emit_pro())
    n_sym = len(INSTANCES)
    n_fp = len(PCB_PLACE) + len(MOUNTING)
    print(f"wrote schematic ({n_sym} symbols), pcb ({n_fp} footprints), project")

    # sanity: every placed ref exists in schematic; every footprint def exists
    refs = {i["ref"] for i in INSTANCES}
    for ref, *_ in PCB_PLACE:
        assert ref in refs, f"PCB ref {ref} missing from schematic"
        assert VALUES[ref][1] in FOOTPRINT_DEFS, f"no footprint def for {VALUES[ref][1]}"
    # sanity: CB-01 nets reproduced exactly
    for ref, pins in CB.items():
        it = next(i for i in INSTANCES if i["ref"] == ref)
        for pin, net in pins.items():
            assert it["nets"].get(pin) == net, f"CB-01 mismatch {ref}.{pin}"
    print("CB-01 pin netlist reproduced exactly; placement refs consistent")


if __name__ == "__main__":
    main()
