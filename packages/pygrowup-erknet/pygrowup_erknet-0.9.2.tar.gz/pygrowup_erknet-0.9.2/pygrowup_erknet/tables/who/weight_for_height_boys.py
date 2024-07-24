from typing import Union
from .base import WhoRightSkewedGrowthTable
from .. import TableType, Sex

class WhoWeightForHeightBoys(WhoRightSkewedGrowthTable):
    def get_table_type(self) -> TableType:
        return TableType.WeightForHeigt
    
    def get_file_name(self) -> str:
        return 'who_weight_for_height_boys'
    
    #def get_csv_url(self) -> str:
    #    return 'https://ftp.cdc.gov/pub/Health_Statistics/NCHS/growthcharts/WHO-Boys-Weight-for-length-Percentiles.csv'
    
    def get_xslx_url(self) -> str:
        return 'https://cdn.who.int/media/docs/default-source/child-growth/child-growth-standards/indicators/weight-for-length-height/expanded-tables/wfh-boys-zscore-expanded-tables.xlsx'

    def get_table_sex(self) -> Union[Sex, None]:
        return Sex.Male
