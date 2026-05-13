# OBIS Code Mapping Dictionary
# Format: OBIS_CODE: {"name": Readable Name, "unit": Unit, "scale": multiplier}

OBIS_MAP = {
    # Instantaneous Parameters
    "1.0.32.7.0.255": {"name": "Voltage R Phase", "unit": "V", "scale": 1.0, "field": "voltage_r"},
    "1.0.52.7.0.255": {"name": "Voltage Y Phase", "unit": "V", "scale": 1.0, "field": "voltage_y"},
    "1.0.72.7.0.255": {"name": "Voltage B Phase", "unit": "V", "scale": 1.0, "field": "voltage_b"},
    
    "1.0.31.7.0.255": {"name": "Current R Phase", "unit": "A", "scale": 1.0, "field": "current_r"},
    "1.0.51.7.0.255": {"name": "Current Y Phase", "unit": "A", "scale": 1.0, "field": "current_y"},
    "1.0.71.7.0.255": {"name": "Current B Phase", "unit": "A", "scale": 1.0, "field": "current_b"},
    
    "1.0.14.7.0.255": {"name": "Frequency", "unit": "Hz", "scale": 1.0, "field": "frequency"},
    
    "1.0.33.7.0.255": {"name": "Power Factor R", "unit": "", "scale": 0.001, "field": "power_factor_r"},
    "1.0.53.7.0.255": {"name": "Power Factor Y", "unit": "", "scale": 0.001, "field": "power_factor_y"},
    "1.0.73.7.0.255": {"name": "Power Factor B", "unit": "", "scale": 0.001, "field": "power_factor_b"},
    
    "1.0.1.7.0.255":  {"name": "Active Power Import", "unit": "kW", "scale": 0.001, "field": "active_power_import"},
    "1.0.2.7.0.255":  {"name": "Active Power Export", "unit": "kW", "scale": 0.001, "field": "active_power_export"},
    "1.0.3.7.0.255":  {"name": "Reactive Power", "unit": "kVAR", "scale": 0.001, "field": "reactive_power"},
    "1.0.9.7.0.255":  {"name": "Apparent Power", "unit": "kVA", "scale": 0.001, "field": "apparent_power"},
    
    # Energy Parameters
    "1.0.1.8.0.255":  {"name": "Active Energy Import", "unit": "kWh", "scale": 1.0, "field": "active_energy_import"},
    "1.0.2.8.0.255":  {"name": "Active Energy Export", "unit": "kWh", "scale": 1.0, "field": "active_energy_export"},
    "1.0.3.8.0.255":  {"name": "Reactive Energy Import", "unit": "kVARh", "scale": 1.0, "field": "reactive_energy_import"},
    "1.0.9.8.0.255":  {"name": "Apparent Energy", "unit": "kVAh", "scale": 1.0, "field": "apparent_energy"},
    
    # Billing
    "1.0.1.8.1.255":  {"name": "Active Energy Tariff 1", "unit": "kWh", "scale": 1.0, "field": "tariff_1_units"},
    "1.0.1.8.2.255":  {"name": "Active Energy Tariff 2", "unit": "kWh", "scale": 1.0, "field": "tariff_2_units"},
    "1.0.15.6.0.255": {"name": "Maximum Demand", "unit": "kW", "scale": 1.0, "field": "maximum_demand"},
}
