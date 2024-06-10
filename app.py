from flask import Flask, render_template, request, redirect, url_for, flash
import requests
from flask_bootstrap import Bootstrap4
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.requests import GetOrdersRequest
from alpaca.trading.enums import QueryOrderStatus
from alpaca.trading.enums import AssetClass
from dotenv import load_dotenv
import os

load_dotenv('.env.local')

ALPACA_API_KEY = os.getenv('ALPACA_API_KEY')
ALPACA_SECRET_KEY = os.getenv('ALPACA_SECRET_KEY')
ALPACA_BASE_URL = os.getenv('ALPACA_BASE_URL')

trading_client = TradingClient(ALPACA_API_KEY, ALPACA_SECRET_KEY, paper=True)

app = Flask(__name__)
app.config['ALPACA_API_KEY'] = ALPACA_API_KEY
app.config['ALPACA_SECRET_KEY'] = ALPACA_SECRET_KEY
app.config['ALPACA_BASE_URL'] = ALPACA_BASE_URL
app.secret_key = 'supersecretkey'  # For flashing messages
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

        params = {
            'asset_class': AssetClass.US_EQUITY,  # Adjust if needed
            'status': 'active',
            'tradable': True,
            'page_size': 10,
            'style': 'american',
            'limit': 10
        }

        response = requests.get(f"{app.config['ALPACA_BASE_URL']}/v2/assets", headers=headers, params=params)
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

@app.route('/orders', methods=['GET'])
def fetch_orders():
    try:
        get_orders_data = GetOrdersRequest(
        status=QueryOrderStatus.CLOSED,
        limit=100,
        nested=True  # show nested multi-leg orders
    )

        orders=trading_client.get_orders(filter=get_orders_data)
        return render_template('orders.html', orders=orders)
    except Exception as e:
        flash(f"Error fetching orders: {e}", 'danger')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
