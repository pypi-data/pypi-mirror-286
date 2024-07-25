from typing import Union
from .base import WhoRightSkewedGrowthTable
from .. import TableType, Sex

class WhoBmiForAgeBoys(WhoRightSkewedGrowthTable):
    def get_table_type(self) -> TableType:
        return TableType.BodyMassIndexForAge
    
    def get_file_name(self) -> str:
        return 'who_bmi_for_age_boys'
    
    def get_xslx_url(self) -> str:
        return 'https://cdn.who.int/media/docs/default-source/child-growth/child-growth-standards/indicators/body-mass-index-for-age/expanded-tables/bfa-boys-zscore-expanded-tables.xlsx'

    def get_table_sex(self) -> Union[Sex, None]:
        return Sex.Male
