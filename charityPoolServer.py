import os  
import json  
import random  
import requests  
  
from flask import Flask  
from flask import request  
from flask import send_from_directory  
  
from two1.lib.wallet import Wallet  
from two1.lib.bitserv.flask import Payment  
  
app = Flask(__name__)  
wallet = Wallet()  
payment = Payment(app, wallet)  
  
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
# machine-payable endpoint that returns selected file if payment made  
@app.route('/donate')  
@payment.required(20000)  
def donate():  
  
    # extract selection from client request  
    # sel = int(request.args.get('selection'))  
  
    # # check if selection is valid  
    # if(sel < 1 or sel > len(file_list)):  
    #     return 'Invalid selection.'  
    # else:  
    #txid = wallet.send_to(client_payout_addr, 2000)  
    os.system('21 flush')  
    if wallet.confirmed_balance() > 100000:  
         txid = wallet.send_to("1PEoUKNxTZsc5rFSQvQjeTVwDE9vEDCRWm", wallet.confirmed_balance())  
    print(wallet.confirmed_balance())  
    return "Success!"  
  
if __name__ == '__main__':  
    # app.debug = True  
    app.run(host='0.0.0.0', port=9393) 