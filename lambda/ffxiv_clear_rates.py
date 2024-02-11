import sys
from ffxiv_clear_rates.main import run


def lambda_handler(event, context):
    sys.argv = ['main.py', 'clear_rates', '-c', '/opt/python/.fcconfig', '-p']
    run()
    return {
        'statusCode': 200,
        'body': 'Success'
    }