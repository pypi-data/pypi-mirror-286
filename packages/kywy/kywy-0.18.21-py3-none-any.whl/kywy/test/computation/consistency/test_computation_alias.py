from ...kawa_base_e2e_test import KawaBaseTest
import pandas as pd
import uuid
import tempfile
from ....client.kawa_client import KawaClient as K
from ....client.data_consistency import DataConsistencyChecker


class TestComputationWithSorting(KawaBaseTest):
    cities_and_countries = pd.DataFrame([
        {'id': 'a', 'country': 'FR', 'city': 'Paris', 'measure': 1},
        {'id': 'b', 'country': 'FR', 'city': 'Lyon', 'measure': 2},
        {'id': 'c', 'country': 'FR', 'city': 'Lille', 'measure': 3},
        {'id': 'd', 'country': 'UK', 'city': 'London', 'measure': 4},
        {'id': 'e', 'country': 'UK', 'city': 'Cardiff', 'measure': 5},
        {'id': 'g', 'country': 'UK', 'city': 'Edinburgh', 'measure': 6},
        {'id': 'h', 'country': 'UK', 'city': 'Belfast', 'measure': 7},
        {'id': 'i', 'country': 'BE', 'city': 'Brussels', 'measure': 8},
        {'id': 'j', 'country': 'BE', 'city': 'Bruges', 'measure': 9},
        {'id': 'k', 'country': 'BE', 'city': 'Namur', 'measure': 10},
    ])

    @classmethod
    def setUpClass(cls):
        unique_id = 'resource_{}'.format(uuid.uuid4())
        print(tempfile.gettempdir())
        KawaBaseTest.setUpClass()
        cls.sheet_name = unique_id

    def test_that_aliases_are_taken_in_account(self):
        dc = DataConsistencyChecker()
        dc.init_data(self.cities_and_countries)
        dc.check_data_quality()
        dc.display_detailed_results()