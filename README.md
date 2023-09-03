# BingX-Flask
Compras automaticas TradingView

Para utilizar esta aplicación, debes configurar las constantes como API_KEY, API_SECRET, CHAT_ID , TOKEN

En Tradingview deberas realizar una alerta
En mensaje deberas enviar el marcador correcto

Puede usar marcadores de posición para crear el mensaje de notificación de su alerta. Serán reemplazados por su valor correspondiente cuando se active la alerta. Un marcador de posición se define mediante el uso de una de las siguientes palabras clave rodeadas por llaves dobles, por ejemplo, {{strategy.position_size}}:

strategy.position_size — devuelve el valor de la misma palabra clave en Pine, es decir, el tamaño de la posición actual.
strategy.order.action — devuelve la cadena "comprar" o "vender" para la orden ejecutada.
strategy.order.contracts — devuelve el número de contratos de la orden ejecutada.
strategy.order.price — devuelve el precio al que se ejecutó la orden.
strategy.order.id — devuelve el ID de la orden ejecutada (la cadena utilizada como el primer parámetro en una de las llamadas de función que genera órdenes: strategy.entry, strategy.exit o strategy.order).
strategy.order.comment — devuelve el comentario de la orden ejecutada (la cadena utilizada en el parámetro de comentario en una de las llamadas de función que genera órdenes: strategy.entry, strategy..exit o strategy.order). Si no se especifica ningún comentario, se utilizará el valor de strategy.order.id.
strategy.order.alert_message — devuelve el valor del parámetro alert_message que se puede usar en el código Pine de la estrategia cuando se llama a una de las funciones que se usan para realizar pedidos: strategy.entry, strategy.exit o strategy.order. Esta característica solo es compatible con Pine v4.
strategy.market_position — devuelve la posición actual de la estrategia en forma de cadena: "largo", "plano" o "corto".
strategy.market_position_size — devuelve el tamaño de la posición actual.
strategy.prev_market_position — devuelve la posición anterior de la estrategia en forma de cadena: "largo", "plano" o "corto".
strategy.prev_market_position_size — devuelve el tamaño de la posición anterior.

Ahora deberas onfigurar URL WEBHOOK 
http://TU_IP/trading



En el código actual, los niveles de stop loss y take profit se calculan en función de la acción de trading (compra o venta) y el precio de alerta. La variable RISK_REWARD_RATIO controla la relación entre el riesgo y la recompensa.

Por ejemplo, en la siguiente sección del código:

python
Copy code
if action.lower() == 'buy':
    stop_loss = alert_price * (1 - RISK_REWARD_RATIO)
    take_profit = alert_price * (1 + RISK_REWARD_RATIO)
elif action.lower() == 'sell':
    stop_loss = alert_price * (1 + RISK_REWARD_RATIO)
    take_profit = alert_price * (1 - RISK_REWARD_RATIO)
else:
    stop_loss = take_profit = None
Puedes ajustar el valor de RISK_REWARD_RATIO para controlar cuánto mayor debe ser la recompensa en comparación con el riesgo. Por ejemplo, si deseas ser más conservador, puedes disminuir el valor de RISK_REWARD_RATIO (por ejemplo, 1.2) para reducir la distancia entre el stop loss y el take profit.


Tambien podemos ajustar el mensaje de salida en Telegram
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
