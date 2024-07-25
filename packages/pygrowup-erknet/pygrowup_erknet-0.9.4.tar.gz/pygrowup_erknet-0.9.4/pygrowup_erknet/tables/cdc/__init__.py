from .bmi_for_age import CdcBmiForAge
from .head_circumference_for_age import CdcHcForAge
from .height_for_age import CdcHeightForAge
from .length_for_age import CdcLengthForAge
from .weight_for_age import CdcWeightForAge
from .weight_for_age_infant import CdcWeightForAgeInfant
from .weight_for_height import CdcWeightForHeight
from .weight_for_length import CdcWeightForLength

CDC_TABLES = [
    CdcBmiForAge,
    CdcHcForAge,
    CdcLengthForAge,
    CdcHeightForAge,
    CdcWeightForAgeInfant,
    CdcWeightForAge,
    CdcWeightForLength,
    CdcWeightForHeight,
]
