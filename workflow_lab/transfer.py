from workflow_lab.errors import PermanentError


def transfer(accounts, source, dest, amount):
    if amount <= 0:
        raise PermanentError("Amount must be greater than zero")
    accounts[source] -= amount
    accounts[dest] += amount

