from workflow_lab.errors import PermanentError

def check_amount(ctx):
    if ctx['amount'] <= 0:
        raise PermanentError("Amount must be greater than zero")

def check_destination_account(ctx):
    if ctx['dest'] == ctx['source']:
        raise PermanentError("Destination account cannot be the same as source account")

def check_invalid_destination_account(ctx):
    if ctx['dest'] not in ctx['accounts']:
        raise PermanentError("Destination account does not exist")

def check_invalid_source_account(ctx):
    if ctx['source'] not in ctx['accounts']:
        raise PermanentError("Source account does not exist")

def check_insufficient_funds(ctx):
    balance = ctx['accounts'][ctx['source']]
    if ctx['amount'] > balance:
        raise PermanentError("Insufficient funds in source account")

def move_money(ctx):
    ctx['accounts'][ctx['source']] -= ctx['amount']
    ctx['accounts'][ctx['dest']] += ctx['amount']


STEPS = [
    check_amount,
    check_destination_account,
    check_invalid_destination_account,
    check_invalid_source_account,
    check_insufficient_funds,
    move_money
]

def run_steps(steps, ctx):
    for step in steps:
        step(ctx)

def transfer(accounts, source, dest, amount):
    ctx = {
        'accounts': accounts,
        'source': source,
        'dest': dest,
        'amount': amount
    }
    run_steps(STEPS, ctx)



