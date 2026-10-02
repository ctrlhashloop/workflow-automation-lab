from workflow_lab.errors import PermanentError


def transfer(accounts, source, dest, amount):
    if amount <= 0:
        raise PermanentError("Amount must be greater than zero")
    if source == dest:
        raise PermanentError("Destination account cannot be the same as source account")
    if dest not in accounts:
        raise PermanentError("Destination account does not exist")
    if source not in accounts:
        raise PermanentError("Source account does not exist")
    if amount >= accounts[source]:
        raise PermanentError("Insufficient funds in source account")

    accounts[source] -= amount
    accounts[dest] += amount



