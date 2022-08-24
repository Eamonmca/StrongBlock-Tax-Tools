import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

class Zerion_parser:

    def __init__(self, csv_file):
        # read csv
        self.csv_file = csv_file
        df = pd.read_csv(self.csv_file)
        
        # Some data wrangling 
        df.columns = df.columns.str.replace(' ', '_')
        df['Buy_Currency'] = df['Buy_Currency'].fillna("_")
        df['Sell_Currency'] = df['Sell_Currency'].fillna("_")
        self.Dataframe = df

        # transactions associated with incoming $Strong
        Strong_To_Wallet = df[df['Buy_Currency'].str.contains("STRONG")]
        # transactions associated with claiming $strong
        Strong_claims = Strong_To_Wallet[Strong_To_Wallet['Receiver'].str.contains("0xfbddadd80fe7bda00b901fbaf73803f2238ae655")]
        Strong_claims_spent_total_column = Strong_claims["Sell_Fiat_Amount"].astype(float) + Strong_claims["Fee_Fiat_Amount"].astype(float)
        Strong_claims["total_paid_claims"] = Strong_claims_spent_total_column
        self.Claims_df = Strong_claims

        Strong_claims_display = Strong_claims

        Strong_claims_display = Strong_claims_display.rename(columns={"Sell_Fiat_Amount": "Claim Fee", "Fee_Fiat_Amount": "ETH Network Fee Fiat", "Buy_Fiat_Amount": "Amount Claimed Fiat", "total_paid_claims": "Total Claim Fees Fiat", "Tx_Hash": "Transaction Hash", "Link": "Etherscan Link" })
        Strong_claims_display = Strong_claims_display[["Amount Claimed Fiat", "Total Claim Fees Fiat", "Claim Fee", "ETH Network Fee Fiat", "Transaction Hash", "Etherscan Link" ]]




        self.Claims_display = Strong_claims_display

        # transactions associated with outgoing $Strong 
        Strong_leaving_Wallet = df[df['Sell_Currency'].str.contains("STRONG", na=False)]

        # node creation transactions 
        Node_creation_transactions = Strong_leaving_Wallet[Strong_leaving_Wallet['Sell_Currency'].str.contains("ETH\nSTRONG", na=False)]

        self.Node_creation_transactions = Node_creation_transactions
        
        # Get total number of ETH nodes created
        Total_Eth_nodes_created = Node_creation_transactions.shape[0]
        self.Eth_nodes_total = int(Total_Eth_nodes_created)



        Node_creation_transactions_display = Node_creation_transactions
        new = Node_creation_transactions_display[['Sell_Fiat_Amount']]

        new = new["Sell_Fiat_Amount"].str.split("\n", n = 1, expand = True)
        Node_creation_transactions_display["Creation Fee ETH Fiat"] = new[0]
        Node_creation_transactions_display["Creation Fee STRONG Fiat"] = new[1]

        Node_creation_transactions_display = Node_creation_transactions_display[["Date", "Creation Fee ETH Fiat", "Creation Fee STRONG Fiat","Fee_Fiat_Amount", "Tx_Hash", "Link"]]
        Node_creation_transactions_display  = Node_creation_transactions_display.rename(columns={"Sell_Fiat_Amount": "Claim Fee", "Fee_Fiat_Amount": "ETH Network Fee Fiat", "Buy_Fiat_Amount": "Amount Claimed Fiat", "total_paid_claims": "Total Claim Fees Fiat", "Tx_Hash": "Transaction Hash", "Link": "Etherscan Link" })

        self.Node_creation_transactions_display = Node_creation_transactions_display


        Strong_Monthly_fees = df[df['Receiver'].str.contains("0xfbddadd80fe7bda00b901fbaf73803f2238ae655")]
        Strong_Monthly_fees = Strong_Monthly_fees[Strong_Monthly_fees['Accounting_Type'].str.contains("Spend")]
        Strong_Monthly_fees = Strong_Monthly_fees[Strong_Monthly_fees['Sell_Currency'] == "ETH"]
        Strong_Monthly_fees["total_fees"] = Strong_Monthly_fees["Sell_Fiat_Amount"].astype(float) + Strong_Monthly_fees["Fee_Fiat_Amount"].astype(float)

        Strong_Monthly_fees = Strong_Monthly_fees[["Date", "Sell_Fiat_Amount", "Fee_Fiat_Amount", "Tx_Hash", "Link"]]
        
        self.Monthly_fees = Strong_Monthly_fees



        





    



        

    

