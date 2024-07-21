from typing import Dict, List, TypedDict

class GenvexNabtoDatapointKey:
    TEMP_SUPPLY = "temp_supply"
    TEMP_OUTSIDE = "temp_outside"
    TEMP_EXHAUST = "temp_exhaust"
    TEMP_EXTRACT = "temp_extract"
    TEMP_CONDENSER = "temp_condenser"
    TEMP_EVAPORATOR = "temp_evaporator"
    TEMP_ROOM = "temp_room"
    HUMIDITY = "humidity"
    DUTYCYCLE_SUPPLY = "fan_speed_supply"
    DUTYCYCLE_EXTRACT = "fan_speed_extract"
    RPM_SUPPLY = "fan_rpm_supply"
    RPM_EXTRACT = "fan_rpm_extract"
    M3H_SUPPLY = "fan_m3h_supply"
    M3H_EXTRACT = "fan_m3h_extract"
    BYPASS_ACTIVE = "bypass_active"
    HOTWATER_TOP = "hotwater_top"
    HOTWATER_BOTTOM = "hotwater_bottom"
    SUMMER_MODE = "summer_mode"
    SACRIFICIAL_ANODE = "sacrificial_anode"
    CO2_LEVEL = "co2_level"
    FILTER_DAYS_LEFT = "filter_days_left"

class GenvexNabtoSetpointKey:
    FAN_SPEED = "fan_speed"
    TEMP_SETPOINT = "temp_setpoint"
    BYPASS_OPENOFFSET = "bypass_openoffset" # EE1
    REHEATING = "reheating" # A1
    HUMIDITY_CONTROL = "humidity_control" # A2
    BOOST_ENABLE = "boost_enable"
    BOOST_TIME = "boost_time" # A3
    FILTER_DAYS = "filter_days"
    FILTER_MONTHS = "filter_months"
    FILTER_HOURS = "filter_hours"
    FILTER_RESET = "filter_reset"
    SUPPLY_AIR_LEVEL1 = "supply_air_level1"
    SUPPLY_AIR_LEVEL2 = "supply_air_level2"
    SUPPLY_AIR_LEVEL3 = "supply_air_level3"
    SUPPLY_AIR_LEVEL4 = "supply_air_level4"
    EXTRACT_AIR_LEVEL1 = "extract_air_level1"
    EXTRACT_AIR_LEVEL2 = "extract_air_level2"
    EXTRACT_AIR_LEVEL3 = "extract_air_level3"
    EXTRACT_AIR_LEVEL4 = "extract_air_level4"
    HOTWATER_TEMP = "hotwater_temp"
    HOTWATER_BOOSTTEMP = "hotwater_boosttemp"


class GenvexNabtoDatapoint(TypedDict):
    obj: int
    address: int
    divider: int
    offset: int

class GenvexNabtoSetpoint(TypedDict):
    read_obj: int
    read_address: int
    write_obj: int
    write_address: int
    divider: int
    offset: int
    min: int
    max: int
    step: float



class GenvexNabtoBaseModel:
    _datapoints: Dict[GenvexNabtoDatapointKey, GenvexNabtoDatapoint] = {}
    _setpoints: Dict[GenvexNabtoSetpointKey, GenvexNabtoSetpoint] = {}

    def __init__(self):
        return
    
    def getModelName(self):
        return "Basemodel"
    
    def getManufacturer(self):
        return ""

    def modelProvidesDatapoint(self, datapoint: GenvexNabtoDatapointKey) -> bool: 
        return datapoint in self._datapoints
    
    def getDefaultDatapointRequest(self) -> List[GenvexNabtoDatapointKey]:
        return {}
    
    def modelProvidesSetpoint(self, datapoint: GenvexNabtoSetpointKey) -> bool: 
        return datapoint in self._setpoints
    
    def getDefaultSetpointRequest(self) -> List[GenvexNabtoSetpointKey]:
        return {}