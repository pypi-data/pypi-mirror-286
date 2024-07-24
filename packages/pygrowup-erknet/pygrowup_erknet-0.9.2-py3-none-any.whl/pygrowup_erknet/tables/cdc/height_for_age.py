from .base import CdcGrowthTable
from .. import TableType

class CdcHeightForAge(CdcGrowthTable):
    def get_table_type(self) -> TableType:
        return TableType.HeightForAge

    def get_file_name(self) -> str:
        return 'cdc_height_for_age_24_240'
    
    def get_csv_url(self) -> str:
        return 'https://www.cdc.gov/growthcharts/data/zscore/statage.csv' 
