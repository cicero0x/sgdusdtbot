import requests, json
import schedule
import time

telegram_chatID = "*******"

telegram_api = "https://api.telegram.org/bot*********/sendMessage?" ## followed by chat_id = *** (sendMessage, getUpdates)&text="" 


def send_tele_msg(msg):
    base_url = telegram_api + "chat_id=" + telegram_chatID +'&text=' +msg
    requests.get(base_url)


oanda_access_token = "*********************"
gemini_url = "https://api.gemini.com/v1"
binance_url = "https://api.binance.com/api/v3"
oanda_url = "https://api-fxpractice.oanda.com/v3/accounts/101-003-20060714-001"

def get_ask_price(instrument):
    query = {"instruments": instrument}
    headers = {"Authorization": "Bearer 408a2c551435b00ea0992e93b035929b-befef980a74578c21a39f3178ce68187"}
    responseOanda = requests.get(oanda_url+"/pricing", headers = headers, params = query)
    json_response = responseOanda.json()
    ask_price = json_response["prices"][0]["asks"][0]["price"]
    return ask_price


#GET PRICES FROM EXCHANGES
# responseGemini = requests.get(gemini_url + "/pubticker/btcsgd")
# btcsgd_data = responseGemini.json() #btcsgd data from gemini

# responseBinance = requests.get(binance_url + "/ticker/price?symbol=BTCUSDT")
# btcusdt_data = responseBinance.json()

# btcsgd_lastprice = float(btcsgd_data['last'])
# btcusdt_lastprice = float(btcusdt_data['price']) 



def showrates(coinOne, coinTwo):

    print('\n\n'+ "getting rates..." + '\n')
    coinOnesgd = float(requests.get(gemini_url+ "/pubticker/"+coinOne+"SGD").json()['ask'])
    coinOneusdt = float(requests.get(binance_url+"/ticker/price?symbol="+coinOne+"USDT").json()['price'])
    coinTwosgd = float(requests.get(gemini_url+ "/pubticker/"+coinTwo+"SGD").json()['ask'])
    coinTwousdt = float(requests.get(binance_url+"/ticker/price?symbol="+coinTwo+"USDT").json()['price'])

    usdspot = float(get_ask_price("USD_SGD"))
    usdtsgdOne = coinOnesgd/coinOneusdt
    usdtsgdTwo = coinTwosgd/coinTwousdt
    breakevenPrice_coinOne = coinOneusdt*usdspot
    breakevenPrice_coinTwo = coinTwousdt*usdspot

    bps_one = ((usdtsgdOne/usdspot-1)* 10000)
    bps_two = ((usdtsgdTwo/usdspot-1)* 10000)

    if usdtsgdOne < usdtsgdTwo:
        betterPair = coinOne
    else:
        betterPair = coinTwo

    results = f"========== Better Rates for {betterPair} =========="+"\n"
    coinOneResults = ("\nUSDSGD SPOT: " + str(usdspot)+"\n\n" +
        "Rate for " + coinOne + ": " + str(round(usdtsgdOne,4))+ " (" + str(round(bps_one,2))+ " bps)\n"+
        "SGD ASK PRICE: " +str(coinOnesgd)+"\n"+
        "USDT ASK PRICE: " +str(coinOneusdt)+"\n"+
        "Limit Order for " +coinOne+ "SGD: "+ str(round(breakevenPrice_coinOne, 2))+"\n")
    
    coinTwoResults = ("\nRate for " + coinTwo + ": " + str(round(usdtsgdTwo,4)) + " (" + str(round(bps_two,2))+ " bps)\n"+
        "SGD ASK PRICE: " +str(coinTwosgd)+"\n"+ 
        "USDT ASK PRICE: " +str(coinTwousdt)+"\n"+
        "Limit Order for " +coinTwo+ "SGD: "+ str(round(breakevenPrice_coinTwo,2)))


    if usdspot > min(usdtsgdOne, usdtsgdTwo):
        print("ARBITRAGE OPPORTUNITY SPOTTED FOR " + betterPair)
        send_tele_msg("ARBITRAGE OPPORTUNITY SPOTTED FOR " + betterPair)
        send_tele_msg(results + coinOneResults + coinTwoResults)
        print(results + coinOneResults + coinTwoResults)

    elif min(bps_one, bps_two) < 10:
        print("Narrow Spread for " + betterPair)
        send_tele_msg("Narrow Spread for " + betterPair)
        send_tele_msg(results + coinOneResults + coinTwoResults)
        print(results + coinOneResults + coinTwoResults)


    else:
        print(results + coinOneResults + coinTwoResults)

    

schedule.every(10).seconds.do(showrates, coinOne="BTC", coinTwo="ETH")

while True:
    schedule.run_pending()
    time.sleep(1)




