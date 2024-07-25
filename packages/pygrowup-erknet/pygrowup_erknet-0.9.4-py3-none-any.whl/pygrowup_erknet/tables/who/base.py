from typing import Union

from .. import GrowthTable, Sex, AGE_BASED_TYPES

class WhoGrowthTable(GrowthTable):
    def get_col_index_sex(self) -> Union[int, None]:
        return None
    
    def get_col_index_measurement(self) -> int:
        return 0
    
    def get_col_index_l(self) -> int:
        return 1
    
    def get_col_index_m(self) -> int:
        return 2
    
    def get_col_index_s(self) -> int:
        return 3
    
    def get_index_factor(self) -> Union[float, None]:
        if self.get_table_type() in AGE_BASED_TYPES:
            return 1 / 30.4375
        else:
            return None

class WhoRightSkewedGrowthTable(WhoGrowthTable):
    def calculate_zscore(self, index_value: Union[float, int], measurement: Union[float, int], sex: Union[Sex, None] = None) -> float:
        zscore = super().calculate_zscore(index_value, measurement, sex)
        if zscore >= -3 and zscore <= 3:
            return zscore
        
        lms = self.get_lms(index_value, sex)
        if zscore > 3:
            sd3pos = self.calculate_sd(lms, 3)
            sd23pos = sd3pos - self.calculate_sd(lms, 2)
            return (3 + (measurement - sd3pos) / sd23pos)
        else: # zscore < -3
            sd3neg = self.calculate_sd(lms, -3)
            sd23neg = self.calculate_sd(lms, -2) - sd3neg
            return (-3 + (measurement - sd3neg) / sd23neg)
