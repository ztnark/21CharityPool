import os
import json
import random
import requests

from flask import Flask
from flask import request
from flask import send_from_directory

from two1.lib.server import rest_client
from two1.commands.config import TWO1_HOST
from two1.commands.config import Config
from two1.lib.wallet import Wallet
from two1.lib.bitserv.flask import Payment

app = Flask(__name__)
wallet = Wallet()
config = Config()
payment = Payment(app, wallet)
client = rest_client.TwentyOneRestClient(TWO1_HOST, config.machine_auth, config.username)

class Charity(object):
    name = ""
    address = ""

    # The class "constructor" - It's actually an initializer
    def __init__(self, name, address):
        self.name = name
        self.address = address

bitGive = Charity("Bit Give", "1PEoUKNxTZsc5rFSQvQjeTVwDE9vEDCRWm")
charities = [bitGive]
# endpoint to look up files to buy
@app.route('/charities', methods=['GET'])
def show_charities():
    return json.dumps(charities, default=lambda o: o.__dict__, sort_keys=True, indent=4)

def check_amount(request):
    return int(request.args.get("donation", 0))

# machine-payable endpoint that returns selected file if payment made
@app.route('/donate')
@payment.required(check_amount)
def donate():
    if(int(client.get_earnings()["total_earnings"]) > 20000):
        print("Balance over 20000, flushing to blockchain...")
        os.system('21 flush')
    if wallet.confirmed_balance() > 100000:
        print("Balance now over 100,000, sending")
        txid = wallet.send_to("1PEoUKNxTZsc5rFSQvQjeTVwDE9vEDCRWm", wallet.confirmed_balance())
    print(wallet.confirmed_balance())
    return "Success!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9393)
