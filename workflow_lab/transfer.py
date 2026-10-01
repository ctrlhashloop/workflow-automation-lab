def transfer(accounts, source, dest, amount):
    accounts[source] -= amount
    accounts[dest] += amount

