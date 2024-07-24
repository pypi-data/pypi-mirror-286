from . import exceptions
from .tables import GrowthTable, TableType, Sex, AGE_BASED_TYPES, LENGTH_BASED_TYPES, TYPES_ALIASES
from .tables.cdc import CDC_TABLES
from .tables.who import WHO_TABLES

import logging
from typing import List, Union, Type

HEIGHT_TO_LENGTH_FACTOR = 0.7 #cm

class Calculator(object):
    _resolvers: List[GrowthTable]
    logger: logging.Logger
    adjust_height_data: float

    def __init__(self,
                 adjust_height_data: bool = False,
                 include_cdc: bool = False,
                 override_tables: Union[List[Type[GrowthTable]], None] = None) -> None:
        
        self.adjust_height_data = adjust_height_data
        tables: List[Type[GrowthTable]] = override_tables if override_tables is not None else ([ *WHO_TABLES, *CDC_TABLES ] if include_cdc else [ *WHO_TABLES ])
        self._resolvers = [ t() for t in tables ]
    
    # convenience methods
    def lhfa(self, measurement: Union[float, int, None], age_in_months: Union[float, int], sex: Union[str, Sex], is_recumbent_height: bool = False) -> float:
        """ Calculate length/height-for-age """
        return self.zscore_for_measurement(TableType.LengthForAge,
                                           measurement=measurement,
                                           sex=sex,
                                           index_value=age_in_months,
                                           is_recumbent_height=is_recumbent_height)

    def wfl(self, measurement: Union[float, int, None], sex: Union[str, Sex], length: Union[float, int], is_recumbent_height: bool = False) -> float:
        """ Calculate weight-for-length """
        return self.zscore_for_measurement(TableType.WeightForLength,
                                           measurement=measurement,
                                           sex=sex,
                                           index_value=length,
                                           is_recumbent_height=is_recumbent_height)

    def wfh(self, measurement: Union[float, int, None], sex: Union[str, Sex], height: Union[float, int], is_recumbent_height: bool = False) -> float:
        """ Calculate weight-for-height """
        return self.zscore_for_measurement(TableType.WeightForHeigt,
                                           measurement=measurement,
                                           sex=sex,
                                           index_value=height,
                                           is_recumbent_height=is_recumbent_height)

    def wfa(self, measurement: Union[float, int, None], age_in_months: Union[float, int], sex: Union[str, Sex]) -> float:
        """ Calculate weight-for-age """
        return self.zscore_for_measurement(TableType.WeightForAge,
                                           measurement=measurement,
                                           sex=sex,
                                           index_value=age_in_months)

    def bmifa(self, measurement: Union[float, int, None], age_in_months: Union[float, int], sex: Union[str, Sex]) -> float:
        """ Calculate body-mass-index-for-age """
        return self.zscore_for_measurement(TableType.BodyMassIndexForAge,
                                           measurement=measurement,
                                           sex=sex,
                                           index_value=age_in_months)

    def hcfa(self, measurement: Union[float, int, None], age_in_months: Union[float, int], sex: Union[str, Sex]) -> float:
        """ Calculate head-circumference-for-age """
        return self.zscore_for_measurement(TableType.HeadCircumferenceForAge,
                                           measurement=measurement,
                                           sex=sex,
                                           index_value=age_in_months)
    
    def find_table(self, indicator: TableType, sex: Sex, index_value: Union[float, int], aliases_included: bool = False) -> Union[GrowthTable, None]:
        for table in self._resolvers:
            if ((table.get_table_type() == indicator)
                and (table.get_table_sex() is None or table.get_table_sex() == sex)
                and (index_value >= table.get_min_range())
                and (index_value <= table.get_max_range())):
                return table
        
        if (not aliases_included) and (indicator in TYPES_ALIASES):
            # this approach is used to search for the required table before shifting to an alias
            # mostly relevant for length/height tables
            return self.find_table(TYPES_ALIASES[indicator], sex, index_value, aliases_included=True)
        return None
    
    def zscore_for_measurement(self,
                               indicator: Union[TableType, str],
                               measurement : Union[float, int, str, None],
                               sex: Union[str, Sex],
                               index_value: Union[float, int, str],
                               is_recumbent_height: bool = False) -> Union[float, None]:
        if measurement is None:
            return None
        
        sex_converted: Union[Sex, None] = None
        if isinstance(sex, Sex):
            sex_converted = sex
        elif isinstance(sex, str):
            sex_str = sex.upper().strip()
            if sex_str == 'M' or sex_str == 'MALE':
                sex_converted = Sex.Male
            elif sex_str == 'F' or sex_str == 'FEMALE':
                sex_converted = Sex.Female
        
        if sex_converted is None:
            raise exceptions.InvalidSexError(sex)
        
        indicator_converted = None
        if isinstance(indicator, TableType):
            indicator_converted = indicator
        elif isinstance(indicator, str):
            indicator_input = indicator.lower().strip()
            indicator_converted = next((tt for tt in TableType if tt.value == indicator_input), None)
        if indicator_converted is None:
            raise exceptions.InvalidTableNameError(indicator)
        
        index_value_converted = 0.0
        invalid_index_value = False
        if isinstance(index_value, str):
            try:
                index_value_converted = float(index_value)
            except ValueError:
                invalid_index_value = True
        elif index_value is not None:
            index_value_converted = index_value
        else:
            invalid_index_value = True
        
        if invalid_index_value:
            if indicator_converted in LENGTH_BASED_TYPES:
                raise exceptions.InvalidLengthError(index_value)
            elif indicator_converted in AGE_BASED_TYPES:
                raise exceptions.InvalidAgeError(index_value)
            else:
                raise exceptions.InvalidIndexError(index_value)
        table = self.find_table(indicator_converted, sex_converted, index_value_converted)
        if table is None:
            raise exceptions.DataNotFoundError(indicator, sex, index_value)
        
        measurement_converted = None
        try:
            measurement_converted = float(measurement)
        except:
            raise exceptions.InvalidMeasurement(measurement)
        
        if self.adjust_height_data:
            if (table.get_table_type() == TableType.HeightForAge) and is_recumbent_height:
                measurement_converted -= HEIGHT_TO_LENGTH_FACTOR
            elif (table.get_table_type() == TableType.LengthForAge) and (not is_recumbent_height):
                measurement_converted += HEIGHT_TO_LENGTH_FACTOR
            elif (table.get_table_type() == TableType.WeightForHeigt) and is_recumbent_height:
                index_value_converted -= HEIGHT_TO_LENGTH_FACTOR
            elif (table.get_table_type() == TableType.WeightForLength) and (not is_recumbent_height):
                index_value_converted += HEIGHT_TO_LENGTH_FACTOR

        return table.calculate_zscore(index_value_converted, measurement_converted, sex_converted)
