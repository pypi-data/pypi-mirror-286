from typing import Union
from .base import WhoGrowthTable
from .. import TableType, Sex

class WhoHcForAgeBoys(WhoGrowthTable):
    def get_table_type(self) -> TableType:
        return TableType.HeadCircumferenceForAge
    
    def get_file_name(self) -> str:
        return 'who_head_circumference_for_age_boys'
    
    #def get_csv_url(self) -> str:
    #    return 'https://ftp.cdc.gov/pub/Health_Statistics/NCHS/growthcharts/WHO-Boys-Head-Circumference-for-age-Percentiles.csv'
    
    def get_xslx_url(self) -> str:
        return 'https://cdn.who.int/media/docs/default-source/child-growth/child-growth-standards/indicators/head-circumference-for-age/expanded-tables/hcfa-boys-zscore-expanded-tables.xlsx'
    
    def get_table_sex(self) -> Union[Sex, None]:
        return Sex.Male
