import unittest
from workflow_lab.transfer import transfer
from workflow_lab.errors import PermanentError

class TestTransfer(unittest.TestCase):
    def test_transfer_moves_money_and_keeps_total(self):
        accounts = {"A": 100000, "B": 5000}
        total_before = accounts["A"] + accounts["B"]

        # 1. call your transfer function: move 1000 from A to B
        transfer(accounts, "A", "B", 1000)

        # 2. check A went down by 1000
        # print(f'Balance in Account A = {accounts["A"]}')
        self.assertEqual(accounts["A"], 99000)

        # 3. check B went up by 1000
        # print(f'Balance in Account B = {accounts["B"]}')
        self.assertEqual(accounts["B"], 6000)

        # 4. check the total of both is still the same as before
        self.assertEqual(accounts["A"] + accounts["B"], total_before)

    def test_negative_amount_is_refused_and_nothing_moves(self):
        accounts = {"A": 100000, "B": 5000}

        with self.assertRaises(PermanentError):
            transfer(accounts, "A", "B", -1000)

        print(f'A = {accounts["A"]}, B = {accounts["B"]}')
        self.assertEqual(accounts["A"], 100000)
        self.assertEqual(accounts["B"], 5000)

    def test_zero_amount_is_refused_and_nothing_moves(self):
        accounts = {"A": 100000, "B": 5000}

        with self.assertRaises(PermanentError):
            transfer(accounts, "A", "B", 0)
        print(f'A = {accounts["A"]}, B = {accounts["B"]}')
        self.assertEqual(accounts["A"], 100000)
        self.assertEqual(accounts["B"], 5000)

    def test_same_source_and_destination_accounts_is_refused_and_nothing_moves(self):
        accounts = {"A": 100000, "B": 5000}

        with self.assertRaises(PermanentError):
            transfer(accounts, "A", "A", 1000)

        print(f'A = {accounts["A"]}, B = {accounts["B"]}')
        self.assertEqual(accounts["A"], 100000)
        self.assertEqual(accounts["B"], 5000)

    def test_unknown_destination_account_is_refused_and_nothing_moves(self):
        accounts = {"A": 100000, "B": 5000}

        with self.assertRaises(PermanentError):
            transfer(accounts, "A", "Z", 1000)

        self.assertEqual(accounts["A"], 100000)
        self.assertEqual(accounts["B"], 5000)

    def test_unknown_source_account_is_refused_and_nothing_moves(self):
        accounts = {"A": 100000, "B": 5000}

        with self.assertRaises(PermanentError):
            transfer(accounts, "C", "B", 1000)

        print(f'A = {accounts["A"]}, B = {accounts["B"]}')
        self.assertEqual(accounts["A"], 100000)
        self.assertEqual(accounts["B"], 5000)

    def test_insufficient_funds_is_refused_and_nothing_moves(self):
        accounts = {"A": 100000, "B": 5000}

        with self.assertRaises(PermanentError):
            transfer(accounts, "A", "B", 500000)

        print(f'A = {accounts["A"]}, B = {accounts["B"]}')
        self.assertEqual(accounts["A"], 100000)
        self.assertEqual(accounts["B"], 5000)

if __name__ == '__main__':
    unittest.main()