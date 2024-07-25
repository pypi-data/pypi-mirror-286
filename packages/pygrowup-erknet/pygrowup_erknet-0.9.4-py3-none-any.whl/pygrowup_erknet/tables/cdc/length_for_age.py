from .base import CdcGrowthTable
from .. import TableType

class CdcLengthForAge(CdcGrowthTable):
    def get_table_type(self) -> TableType:
        return TableType.LengthForAge

    def get_file_name(self) -> str:
        return 'cdc_length_for_age_0_36'
    
    def get_csv_url(self) -> str:
        return 'https://www.cdc.gov/growthcharts/data/zscore/lenageinf.csv' 
