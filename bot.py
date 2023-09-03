import time
import hmac
import hashlib
import requests
from flask import Flask, request, Response
from pyngrok import ngrok

app = Flask(__name__)
URL = "https://api.telegram.org/bot{}/sendMessage".format('TOKEN')
CHAT_ID = 'MICHATID_TELEGRAM'
RISK_REWARD_RATIO = 1.51
API_KEY = ""
API_SECRET = ""
APIURL = "https://open-api.bingx.com"

@app.route('/trading', methods=['POST'])
def trading():
    data = request.json
    action = data.get('strategy.order.action', '')
    contracts = data.get('strategy.order.contracts', '')
    ticker = data.get('ticker', '')
    position_size = data.get('strategy.position_size', '')
    alert_price = float(data.get('alert_price', 0))

    # Calculating stop loss and take profit
    if action.lower() == 'buy':
        stop_loss = alert_price * (1 - RISK_REWARD_RATIO)
        take_profit = alert_price * (1 + RISK_REWARD_RATIO)
    elif action.lower() == 'sell':
        stop_loss = alert_price * (1 + RISK_REWARD_RATIO)
        take_profit = alert_price * (1 - RISK_REWARD_RATIO)
    else:
        stop_loss = take_profit = None

    # Crear orden en BingX
    timestamp = int(time.time() * 1000)
    params = f"symbol={ticker}&side={action.upper()}&type=LIMIT&quantity={contracts}&price={alert_price}&timestamp={timestamp}"
    signature = hmac.new(API_SECRET.encode(), params.encode(), hashlib.sha256).hexdigest()

    headers = {"X-BX-APIKEY": API_KEY}
    r = requests.post(f"{APIURL}/openApi/spot/v1/order", headers=headers, data=params + f"&signature={signature}")

    message = (
        f"🤖 @TradingRentable_bot\n\n"
        f"🌐 BingX Exchange 🚀\n"
        f"💎---- EVENTO REALIZADO ----💎\n\n" 
        f"🔹 Orden: {action} \n"
        f"🔹 Contratos: {contracts}\n"
        f"🔹 Ticker: {ticker}\n"
        f"🔹 Nueva posición estratégica: {position_size}\n"
        f"🔹 Precio de alerta: {alert_price}\n"
        f"🔹 Stop Loss: {stop_loss}\n"
        f"🔹 Take Profit: {take_profit}\n"
        f"🔹 Respuesta de BingX: {r.json()}\n\n"
    )

    requests.post(URL, data={'chat_id': CHAT_ID, 'text': message})

    return Response(status=200)

if __name__ == '__main__':
    public_url = ngrok.connect(5000)
    print("Public URL:", public_url)
    app.run(port=5000)
