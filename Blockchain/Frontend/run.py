from flask import Flask, render_template, request
from Blockchain.client.sendBTC import SendBTC

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def wallet():
    message = ""
    if request.method == 'POST':
        FromAddress = request.form.get('fromAddress')
        ToAddress = request.form.get('toAddress')
        Amount = request.form.get('Amount', type=int)
        sendCoin = SendBTC(FromAddress, ToAddress, Amount, UTXOS)

        if not sendCoin.prepareTransaction():
            message = "Insufficient Balance"
        
    return render_template('wallet.html', message=message)

def main(utxos):
    global UTXOS
    UTXOS = utxos
    app.run()
