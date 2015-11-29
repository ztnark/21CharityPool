import sys
import json

#import from the 21 Developer Library
from two1.commands.config import Config
from two1.lib.wallet import Wallet
from two1.lib.bitrequests import BitTransferRequests

# set up bitrequest client for BitTransfer requests
wallet = Wallet()
username = Config().username
requests = BitTransferRequests(wallet, username)

# server address
def donate(server_url):
    # get the charity listings from the server
    response = requests.get(url=server_url+'charities')
    charity_list = json.loads(response.text)
    for charity_index in range(len(charity_list)):
        print("{0}. {1}".format(charity_index + 1, charity_list[charity_index]["name"]))
    try:
        # prompt the user to input the index number of the charity to donate to and the amount to donate
        sel = int(input("Please enter the index of the charity you'd like to donate to: "))
        # check if the input index is valid key in charity_list dict
        if sel <= len(charity_list):
            charity_name = charity_list[sel-1]["name"]
            donation_amount = int(input("How many satoshis would you like to donate to {}?: ".format(charity_name)))
        else:
            print("That is an invalid selection.")
            return
        #create a 402 request
        sel_url = server_url+'donate?sel={0}&donation={1}'.format(sel, donation_amount)
        answer = requests.get(url=sel_url, stream=True)
        if answer.status_code != 200:
            print("Could not make an offchain payment. Please check that you have sufficient balance.")
        else:
            print('Congratulations, you just donated {0} satoshis to {1}! Thanks!'.format(donation_amount, charity_name))


    except ValueError:
        print("That is an invalid input. Only numerical inputs are accepted.")

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        server_url = sys.argv[1]
    else:
        server_url = 'http://localhost:9393/'
    donate(server_url)
