import logging
import csv
from pathlib import Path
from typing import List, Dict, Tuple, Union
import unittest

from . import Calculator, TableType, Sex, exceptions

TEST_ACCURACY = 0.3

CSV_COLUMNS_1 = 'id,region,GENDER,agemons,WEIGHT,HEIGHT,measure,oedema,HEAD,MUAC,TRI,SUB,SW,age.days,clenhei,triskin,subskin,oedema,sw,cbmi,zlen,zwei,zwfl,zbmi,zhc,zac,zts,zss,flen,fwei,fwfl,fbmi,fhc,fac,fts,fss'
CSV_COLUMNS_2 = 'id,gender,dob,screen_date,agemons,weight,height,head,zwei,zlen,zbmi,zwfl,zhc,_agemons,_cbmi,zwfa,zhfa,zbfa,sex'

TESTS = {
    #TableType.BodyMassIndexForAge : 'zbmi',
    TableType.LengthForAge : 'zlen',
    TableType.WeightForAge : 'zwei',
    TableType.WeightForLength : 'zwfl'
}

TEST_FILE1 = 'MySurvey_z_st.csv'
TEST_FILE2 = 'test_dataset.csv'

test_data_dir = Path(__file__).resolve().parent / 'testdata'
logger = logging.getLogger('pygrowup_test')
logger.setLevel(logging.DEBUG)

def parse_test_csv(filename: str, csv_columns: str, id_col: str, sex_col: str, age_col: str, weight_col: str, height_col: str, male_sex: str) -> List[Tuple[int, Sex, float, float, Union[float, None], Dict[TableType, float]]]: # index, sex, age_in_months, weight, height?, Dict[TableType, float]
    csv_file_path = test_data_dir / filename
    assert csv_file_path.exists()
    
    result = []
    with csv_file_path.open('r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        for row in reader:
            row_data = dict(zip(csv_columns.split(','), row))
            id = int(row_data[id_col])
            sex = Sex.Male if row_data[sex_col] == male_sex else Sex.Female
            age_in_months = float(row_data[age_col])
            if row_data[weight_col] != '':
                weight = float(row_data[weight_col])
                height = float(row_data[height_col]) if row_data[height_col] != '' else None
                tests = {}
                for test_type, compare_column in TESTS.items():
                    if row_data[compare_column] != '':
                        tests[test_type] = float(row_data[compare_column])
                result.append((id, sex, age_in_months, weight, height, tests))
    return result


class TestWhoZScores(unittest.TestCase):
    def compare_case(self, calculator: Calculator, id: int, sex: Sex, age_in_months: float, weight:float, height: Union[float, None], tests: Dict[TableType, float]) -> None:
        for test, ref_value in tests.items():
            test_value = 0.0
            try:
                match test:
                    case TableType.BodyMassIndexForAge:
                        test_value = calculator.bmifa((weight/((height/100)**2)), age_in_months, sex)
                    case TableType.LengthForAge:
                        test_value = calculator.lhfa(height, age_in_months, sex)
                    case TableType.WeightForAge:
                        test_value = calculator.wfa(weight, age_in_months, sex)
                    case TableType.WeightForLength:
                        test_value = calculator.wfl(weight, sex, height)
                    case _:
                        raise NotImplementedError()
                logger.debug(f'{test.value} : calculated: {test_value:.2f} ; expected: {ref_value:.2f}')
            except exceptions.DataNotFoundError:
                return
            
            with self.subTest(test=test, id=id, sex=sex, age_in_months=age_in_months, weight=weight, height=height, calculated=test_value, expected=ref_value):
                self.assertAlmostEqual(test_value, ref_value, delta=TEST_ACCURACY)
    
    def test_who_file1(self):
        who_calculator = Calculator(include_cdc=False)
        logger.debug(f'Test file: {TEST_FILE1}')
        for id, sex, age_in_months, weight, height, tests in parse_test_csv(TEST_FILE1, CSV_COLUMNS_1, 'id', 'GENDER', 'agemons', 'WEIGHT', 'HEIGHT', male_sex='1'):
            logger.debug(f'id: {id}, sex: {sex.value}, age_in_months: {age_in_months:.2f}, weight: {weight:.2f}, height: {height}')
            self.compare_case(who_calculator, id, sex, age_in_months, weight, height, tests)
    
    def test_who_file2(self):
        return
        who_calculator = Calculator(include_cdc=False)
        logger.debug(f'Test file: {TEST_FILE2}')
        for id, sex, age_in_months, weight, height, tests in parse_test_csv(TEST_FILE2, CSV_COLUMNS_2, 'id', 'gender', 'agemons', 'weight', 'height', male_sex='Male'):
            logger.debug(f'id: {id}, sex: {sex.value}, age_in_months: {age_in_months:.2f}, weight: {weight:.2f}, height: {height}')
            self.compare_case(who_calculator, id, sex, age_in_months, weight, height, tests)

if __name__ == '__main__':
    unittest.main()
