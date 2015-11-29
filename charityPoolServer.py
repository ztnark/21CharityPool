import os
import json

from flask import Flask
from flask import request

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

# endpoint to look up avaialable charities to donate to
@app.route('/charities', methods=['GET'])
def show_charities():
    return json.dumps(charities, default=lambda o: o.__dict__, sort_keys=True, indent=4)

# check how much donated
def check_amount(request):
    return int(request.args.get("donation", 0))

# machine-payable endpoint that donates given amount to specified charity
@app.route('/donate')
@payment.required(check_amount)
def donate():
    amount = int(request.args.get("donation", 0))

    # if current off-chain balance is over 20,000, flush to blockchain
    off_chain_balance = int(client.get_earnings()["total_earnings"])
    if(off_chain_balance > 20000):
        print("Off-chain balance now over 20,000 at {0}, flushing to blockchain...".format(off_chain_balance))
        os.system('21 flush')
    if wallet.confirmed_balance() > 100000:
        print("On-chain balance now over 100,000 at {0}, sending to charity...".format(wallet.confirmed_balance()))
        txid = wallet.send_to(charities[0].address, wallet.confirmed_balance())
    print("Donated {0} to charity! On-chain balance now: {1}".format(amount, wallet.confirmed_balance()))
    return "Success!"

if __name__ == '__main__':
    #app.debug = True
    app.run(host='0.0.0.0', port=9393)
