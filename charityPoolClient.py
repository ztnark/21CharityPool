import sys
import json
import os
#import from the 21 Developer Library
from two1.commands.config import Config
from two1.lib.wallet import Wallet
from two1.lib.bitrequests import BitTransferRequests

# set up bitrequest client for BitTransfer requests
wallet = Wallet()
username = Config().username
requests = BitTransferRequests(wallet, username)

# server address
def donate(server_url = 'http://localhost:9393/'):

    # get the file listing from the server
    response = requests.get(url=server_url+'charities')
    file_list = json.loads(response.text)
    for file in range(len(file_list)):
        print("{}".format(file_list[file]["name"]))
    try:
        # prompt the user to input the index number of the file to be purchase
        sel = input("Please enter the index of the charity you'd like to donate to:")
        # check if the input index is valid key in file_list dict
        if int(sel) <= len(file_list):
            print('You selected {} in our database'.format(file_list[int(sel) - 1]["name"]))
        else:
            print("That is an invalid selection.")
        #create a 402 request with the server payout address
        sel_url = server_url+'donate?payout_address={0}&donation=100'
        answer = requests.get(url=sel_url.format(wallet.get_payout_address()), stream=True)
        if answer.status_code != 200:
                print("Could not make an offchain payment. Please check that you have sufficient balance.")
        else:
            print('Congratulations, you just donated to charity!')


    except ValueError:
        print("That is an invalid input. Only numerical inputs are accepted.")

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        server_url = sys.argv[1]
    else:
        server_url = 'http://localhost:9393/'
    donate(server_url)