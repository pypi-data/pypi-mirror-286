from .head_circumference_for_age_boys import WhoHcForAgeBoys
from .head_circumference_for_age_girls import WhoHcForAgeGirls
from .length_for_age_boys import WhoLengthForAgeBoys
from .length_for_age_girls import WhoLengthForAgeGirls
from .weight_for_age_boys import WhoWeightForAgeBoys
from .weight_for_age_girls import WhoWeightForAgeGirls
from .weight_for_length_boys import WhoWeightForLengthBoys
from .weight_for_length_girls import WhoWeightForLengthGirls
from .weight_for_height_boys import WhoWeightForHeightBoys
from .weight_for_height_girls import WhoWeightForHeightGirls

WHO_TABLES = [
    WhoHcForAgeBoys,
    WhoHcForAgeGirls,
    WhoLengthForAgeBoys,
    WhoLengthForAgeGirls,
    WhoWeightForAgeBoys,
    WhoWeightForAgeGirls,
    WhoWeightForHeightBoys,
    WhoWeightForHeightGirls,
    WhoWeightForLengthBoys,
    WhoWeightForLengthGirls,
]
