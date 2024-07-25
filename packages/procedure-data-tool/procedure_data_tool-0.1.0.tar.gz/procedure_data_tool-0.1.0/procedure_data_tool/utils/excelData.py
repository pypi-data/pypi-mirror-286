from openpyxl import load_workbook
from procedure_data_tool.utils.valve import Valve
from procedure_data_tool.utils.valve2 import Valve2
from procedure_data_tool.utils.nozzle import Nozzle
from procedure_data_tool.utils.line import Line
from procedure_data_tool.utils.valve3 import Valve3
from procedure_data_tool.utils.split import Split
from procedure_data_tool.utils.pump import Pump
from procedure_data_tool.utils.tankreturn import TankReturn
from procedure_data_tool.utils.pit import Pit

def importComponents(filepath='//hanford/data/sitedata/WasteTransferEng/Waste Transfer Engineering/1 Transfers/1C - Procedure Review Tools/MasterProcedureData.xlsx'):
    try:
        wb = load_workbook(filename=filepath, data_only=True)
    except FileNotFoundError as e:
        raise e

    sheet = wb["Pit Components"]
    pits = {}

    for row in sheet.iter_rows(min_row=3, values_only=True, max_row=150, max_col=26):
        pit = row[1]
        if pit not in pits:
            pits[pit] = Pit(
                name=pit, leak_detector_id=row[2], leak_detector_pmid=row[3],
                leak_detector_tfsps=row[4], tfsps_transmitter=row[5],
                tfsps_pmid=row[6], drain_seal_location=row[7], drain_seal_name=[8],
                drain_seal_position=row[9], annulus_leak_detector=row[12],
                annulus_leak_detector_pmid=row[13], pit_nace=row[14],
                pit_nace_pmid=row[15], in_pit_heater=row[16],
                tfmcs=row[17], tsr_structure=row[18]
            )
        else:
            pits[pit].update(
                tfsps_transmitter=row[5], tfsps_pmid=row[6], 
                annulus_leak_detector=row[12], annulus_leak_detector_pmid=row[13],
                in_pit_heater=row[16],
            )

    component_types = {
        "2-Way-Valve": Valve2,
        "3-Way-Valve": Valve3,
        "Tee Fitting": Split,
        "Split Point": Split,
        "Pump": Pump,
        "Transfer Line": Line,
        "Nozzle": Nozzle,
        "": Valve,
        "Tank Return": TankReturn,
        None: Valve
    }

    inventory = {}

    cnx = wb['Transfer Route Components']
    conections_matrix=cnx["F2:H400"]

    for row in cnx.iter_rows(min_row=2, values_only= True, max_row=350, max_col=15):
        name = row[0]
        type = row[1]
        inventory[name] = component_types[type](name, pit = row[2], jumper = row[3], 
                                                dvi = row[4], field_label = row[12])

    for component, connections in zip(inventory.values(), conections_matrix):
        for connection in connections:
            if connection.value in inventory:
                if connection.value:
                    component.connect(inventory[connection.value])

    return inventory, pits


importComponents()
