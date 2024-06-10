from flask import Flask, render_template, request, redirect, url_for, flash
import requests
from config import Config
from flask_bootstrap import Bootstrap4
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

trading_client = TradingClient(Config.ALPACA_API_KEY, Config.ALPACA_SECRET_KEY, paper=True)

app = Flask(__name__)
app.config.from_object(Config)
Bootstrap4(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/assets', methods=['GET'])
def fetch_assets():
    try:
        headers = {
            'Apca-Api-Key-Id': app.config['ALPACA_API_KEY'],
            'Apca-Api-Secret-Key': app.config['ALPACA_SECRET_KEY'],
        }
        response = requests.get(f"{app.config['ALPACA_BASE_URL']}/v2/assets", headers=headers, params={'asset_class': 'crypto'})
        assets = response.json()
        return render_template('assets.html', assets=assets)
    except Exception as e:
        flash(f"Error fetching assets: {e}", 'danger')
        return redirect(url_for('index'))

@app.route('/trade', methods=['POST'])
def create_trade():
    symbol = request.form.get('symbol')
    qty = float(request.form.get('qty'))
    side = request.form.get('side').upper()
    time_in_force = request.form.get('time_in_force').upper()

    try:
        order_data = MarketOrderRequest(
            symbol=symbol,
            qty=qty,
            side=OrderSide[side],
            time_in_force=TimeInForce[time_in_force]
        )
        market_order = trading_client.submit_order(order_data=order_data)
        flash("Order created successfully!", 'success')
    except Exception as e:
        flash(f"Error creating order: {e}", 'danger')

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.secret_key = 'supersecretkey'  # For flashing messages
    app.run(debug=True)
