from typing import Union
from .base import WhoGrowthTable
from .. import TableType, Sex

class WhoLengthForAgeGirls(WhoGrowthTable):
    def get_table_type(self) -> TableType:
        return TableType.LengthForAge
    
    def get_file_name(self) -> str:
        return 'who_length_for_age_girls'
    
    #def get_csv_url(self) -> str:
    #    return 'https://ftp.cdc.gov/pub/Health_Statistics/NCHS/growthcharts/WHO-Girls-Length-for-age-Percentiles.csv'
    
    def get_xslx_url(self) -> str:
        return 'https://cdn.who.int/media/docs/default-source/child-growth/child-growth-standards/indicators/length-height-for-age/expandable-tables/lhfa-girls-zscore-expanded-tables.xlsx'
    
    def get_table_sex(self) -> Union[Sex, None]:
        return Sex.Female
