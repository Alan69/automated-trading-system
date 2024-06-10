# Automated Trading System with Alpaca API

This is a Flask web application for an automated trading system using the Alpaca API. The application allows users to create market orders for stocks through a web interface.

## Features

- Create market orders for stocks.
- Uses the Alpaca API for trading.
- Bootstrap for a responsive and clean UI.

## Prerequisites

- Python 3.x
- Flask
- Bootstrap-Flask
- Alpaca-trade-api

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/flask-trading-app.git
    cd flask-trading-app
    ```

2. **Create a virtual environment:**

    ```bash
    python3 -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up your Alpaca API keys:**

    Create a `config.py` file in the root directory with the following content:

    ```python
    import os

    class Config:
        ALPACA_API_KEY = os.environ.get('ALPACA_API_KEY', 'your-alpaca-api-key')
        ALPACA_SECRET_KEY = os.environ.get('ALPACA_SECRET_KEY', 'your-alpaca-secret-key')
        ALPACA_BASE_URL = os.environ.get('ALPACA_BASE_URL', 'https://api.alpaca.markets')
        ALPACA_PAPER = True  # Use paper trading environment
    ```

5. **Run the application:**

    ```bash
    python app.py
    ```

6. **Open your browser and navigate to:**

    ```
    http://127.0.0.1:5000
    ```


## Usage

1. **Home Page:**

    - The home page provides a form to create a new trade order.

2. **Create Trade:**

    - Fill in the symbol, quantity, side (buy/sell), and time in force (GTC/day).
    - Submit the form to create a market order.

## Dependencies

- Flask
- Requests
- Bootstrap-Flask
- Alpaca-trade-api

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## Acknowledgements

- [Alpaca API](https://alpaca.markets/)
- [Flask](https://flask.palletsprojects.com/)
- [Bootstrap](https://getbootstrap.com/)
