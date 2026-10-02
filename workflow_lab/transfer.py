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

def build_ctx(accounts, source, dest, amount):
    return {
        'accounts': accounts,
        'source': source,
        'dest': dest,
        'amount': amount,
        'audit' : []
    }

def run_steps(steps, ctx):
    for step in steps:
        try:
            step(ctx)
        except PermanentError as exc:
            ctx['audit'].append(
                {'step' : step.__name__, 'outcome' : 'REJECTED', 'message' : str(exc)}
            )
            raise
        ctx['audit'].append(
            {'step' : step.__name__, 'outcome' : 'SUCCESS', 'message' : ''}
        )


def transfer(accounts, source, dest, amount):
    ctx = build_ctx(accounts, source, dest, amount)
    run_steps(STEPS, ctx)


def submit_transfer(accounts, source, dest, amount):
    ctx = build_ctx(accounts, source, dest, amount)
    try:
        run_steps(STEPS, ctx)
    except PermanentError as exc:
        return {'status' : 'REJECTED', 'reason' : str(exc), 'audit' : ctx['audit']}
    return {'status': 'COMPLETED', 'reason': '', 'audit': ctx['audit']}

