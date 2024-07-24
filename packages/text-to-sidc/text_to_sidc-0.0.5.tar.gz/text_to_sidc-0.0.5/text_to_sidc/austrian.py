from enum import Enum, auto
import regex
from os.path import dirname

def load_designator_data():
    # read csv file as txt
    # return list of tuples with pattern and sidc
    path = f"{dirname(__file__)}/patterns_data.csv"
    open_file = open(path, "r")
    lines = open_file.readlines()
    open_file.close()

    # create list of tuples and remove new line character
    data = []
    for line in lines:
        pattern, sidc = line.strip().split(",")
        data.append((pattern, sidc))

    return data

    # return pd.read_csv(f"{dirname(__file__)}/patterns_data.csv")

class Status(Enum):
    """
    Provides status of the unit.
    """
    PRESENT = "0"
    PLANNED_ANTICIPATED_SUSPECT = "1"
    FULLY_CAPABLE = "2"
    DAMAGED = "3" 
    DESTROYED = "4"
    FULL_TO_CAPACITY = "5"

class Mobility(Enum):
    """
    Provides mobility of the unit. 
    """
    UNSPECIFIED = auto()
    WHEELED_LIMITED_CROSS_COUNTRY = auto()
    WHEELED_CROSS_COUNTRY = auto()
    TRACKED = auto()
    WHEELED_AND_TRACKED_COMBINATION = auto()
    TOWED = auto()

def set_mobility(sidc, mobility):
    """
    Set's mobility for disignated unit
    """
    if mobility == Mobility.WHEELED_LIMITED_CROSS_COUNTRY:
        sidc = set_char_at_position(sidc, '3', 8)
        sidc = set_char_at_position(sidc, '1', 9)
    elif mobility == Mobility.WHEELED_CROSS_COUNTRY:
        sidc = set_char_at_position(sidc, '3', 8)
        sidc = set_char_at_position(sidc, '2', 9)
    elif mobility == Mobility.TRACKED:
        sidc = set_char_at_position(sidc, '3', 8)
        sidc = set_char_at_position(sidc, '3', 9)
    elif mobility == Mobility.TOWED:
        sidc = set_char_at_position(sidc, '3', 8)
        sidc = set_char_at_position(sidc, '5', 9)
    else:  # Mobility.UNSPECIFIED or any other case
        sidc = set_char_at_position(sidc, '0', 8)
        sidc = set_char_at_position(sidc, '0', 9)
    return sidc

def set_char_at_position(sidc, character, position):
    "Replaces characters by gives ones"
    replacement = list(sidc)
    replacement[position] = character
    return ''.join(replacement)


class UnitDesignator:
    """
    Accepts a name of the unit and returns a SIDC code.
    """

    _data = load_designator_data()

    def __init__(self):
        # Use self._data as needed
        pass

    @staticmethod
    def calculate_icon(name: str) -> str:
        return UnitDesignator.calculate_icon_with_flag(name, True)

    @staticmethod
    def calculate_icon_with_flag(name: str, calculate_icon: bool) -> str:
        if calculate_icon and name:
            sidc = UnitDesignator.get_unit(name.upper())
            return "30012500001313000000" if sidc is None else sidc
        return "30012500001313000000"

    @staticmethod
    def get_unit(name: str) -> str:
        mobility = Mobility.UNSPECIFIED
        if "БУКСИРОВАНИЙ" in name:
            mobility = Mobility.TOWED
            name = name.replace("БУКСИРОВАНИЙ", "")

        sidc = UnitDesignator.designate_icon(name)

        if any(keyword in name for keyword in ["МАКЕТ", "МУЛЯЖ", "МАКЕТЫ", "МУЛЯЖИ", "МАКЕТА", "МУЛЯЖА"]):
            if sidc is not None:
                return set_char_at_position(sidc, "1", 7)

        if any(keyword in name for keyword in ["УРАЖЕНО", "УРАЖЕНА", "ПОШКОДЖЕНА", "ПОШКОДЖЕНО", "ПОШКОДЖЕНІ", 
                                            "ПОРАЖЕНО", "ПОРАЖЕНА", "ПОВРЕЖДЕНА", "ПОВРЕЖДЕНО", "ПОВРЕЖДЕННЫЕ"]):
            if sidc is not None:
                return set_char_at_position(sidc, Status.DAMAGED.value, 6)

        if any(keyword in name for keyword in ["ЗНИЩЕНОГО", "ЗНИЩЕНА", "ЗРУЙНОВАНО", "ЗНИЩЕНО",
                                            "УНИЧТОЖЕННОГО", "УНИЧТОЖЕНА", "РАЗРУШЕНО", "УНИЧТОЖЕНО"]):
            if sidc is not None:
                return set_char_at_position(sidc, Status.DESTROYED.value, 6)

        if "ВІДНОВЛЕНО" in name:
            if sidc is not None:
                return set_char_at_position(sidc, Status.FULL_TO_CAPACITY.value, 6)

        if any(keyword in name for keyword in ["ЙМОВІРНО", "МОЖЛИВО", "ЙМОВІРНА",
                                              "ВЕРОЯТНО", "ВОЗМОЖНО", "ВЕРОЯТНАЯ"]):
            if sidc is not None:
                return set_char_at_position(sidc, Status.PLANNED_ANTICIPATED_SUSPECT.value, 6)

        if  mobility != Mobility.UNSPECIFIED:
            sidc_with_mobility = set_mobility(sidc, mobility)
            return sidc_with_mobility

        return sidc

    @staticmethod
    def additional_pattern(pattern):
            return (r'(^|[^\p{L}])' + "(" + pattern + ")" + r'($|[^\p{L}])')
    


    @staticmethod
    def designate_icon(name: str) -> str:        

        for pattern_row in UnitDesignator._data:
            full_pattern = UnitDesignator.additional_pattern(pattern_row[1])
            
            match = regex.search(full_pattern, name.upper())            
            if match:
                return pattern_row[0]
        return None 