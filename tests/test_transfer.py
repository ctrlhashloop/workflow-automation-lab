import unittest
from workflow_lab.transfer import transfer, submit_transfer, STEPS
from workflow_lab.errors import PermanentError

class TestTransfer(unittest.TestCase):
    def test_valid_request_completes_and_moves_money(self):
        accounts = {"A": 100000, "B": 5000}

        result = submit_transfer(accounts, "A", "B", 1000)

        self.assertEqual(result["status"], "COMPLETED")
        self.assertEqual(accounts["A"], 99000)
        self.assertEqual(accounts["B"], 6000)

    def test_invalid_request_is_rejected_with_reason_and_nothing_moves(self):
        accounts = {"A": 100000, "B": 5000}

        result = submit_transfer(accounts, "A", "B", -1000)

        self.assertEqual(result["status"], "REJECTED")
        self.assertEqual(result["reason"], "Amount must be greater than zero")
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

    def test_audit_lists_every_step_in_order_when_completed(self):
        accounts = {"A": 100000, "B": 5000}

        result = submit_transfer(accounts, "A", "B", 1000)

        names = [entry["step"] for entry in result["audit"]]
        outcomes = {entry["outcome"] for entry in result["audit"]}
        self.assertEqual(names, [step.__name__ for step in STEPS])
        self.assertEqual(outcomes, {"SUCCESS"})

    def test_audit_stops_at_the_step_that_refused(self):
        accounts = {"A": 100000, "B": 5000}

        result = submit_transfer(accounts, "A", "B", 500000)

        all_names = [step.__name__ for step in STEPS]
        expected = all_names[: all_names.index("check_insufficient_funds") + 1]
        names = [entry["step"] for entry in result["audit"]]
        self.assertEqual(names, expected)
        self.assertEqual(result["audit"][-1]["outcome"], "REJECTED")
        self.assertNotIn("move_money", names)

if __name__ == '__main__':
    unittest.main()