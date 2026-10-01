import unittest
from workflow_lab.transfer import transfer

class TestTransfer(unittest.TestCase):
    def test_transfer_moves_money_and_keeps_total(self):
        accounts = {"A": 100000, "B": 5000}
        total_before = accounts["A"] + accounts["B"]
        # 1. call your transfer function: move 1000 from A to B
        # 2. check A went down by 1000
        # 3. check B went up by 1000
        # 4. check the total of both is still the same as before
        transfer(accounts, "A", "B", 1000)
        self.assertEqual(accounts["A"], 99000)
        self.assertEqual(accounts["B"], 6000)
        self.assertEqual(accounts["A"] + accounts["B"], total_before)

if __name__ == '__main__':
    unittest.main()