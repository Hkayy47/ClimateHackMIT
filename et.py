from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory database
marketplace = {
    "accounts": {},  # {"name": {"energy": <int>, "cash": <float>, "transactions": []}}
    "order_book": [],  # {"id": <int>, "type": "buy" or "sell", "quantity": <int>, "price": <float>, "person": <str>}
    "transactions": [],  # {"buyer": <str>, "seller": <str>, "quantity": <int>, "price": <float>}
}

# Utility functions
def get_next_id():
    return max([order["id"] for order in marketplace["order_book"]], default=0) + 1

def initialize_account(name):
    """Ensure the person has an account."""
    if name not in marketplace["accounts"]:
        marketplace["accounts"][name] = {
            "energy": 0,
            "cash": 1000.0,  # Starting cash balance
            "transactions": []
        }

def match_orders():
    """Match buy and sell orders dynamically."""
    transactions = []
    buys = sorted([o for o in marketplace["order_book"] if o["type"] == "buy"], key=lambda x: -x["price"])
    sells = sorted([o for o in marketplace["order_book"] if o["type"] == "sell"], key=lambda x: x["price"])

    i, j = 0, 0
    while i < len(buys) and j < len(sells):
        buy = buys[i]
        sell = sells[j]

        if buy["price"] >= sell["price"]:
            trade_quantity = min(buy["quantity"], sell["quantity"])
            trade_price = sell["price"]  # Execute at the lowest sell price

            # Update buyer and seller accounts
            initialize_account(buy["person"])
            initialize_account(sell["person"])
            marketplace["accounts"][buy["person"]]["energy"] += trade_quantity
            marketplace["accounts"][buy["person"]]["cash"] -= trade_quantity * trade_price
            marketplace["accounts"][sell["person"]]["energy"] -= trade_quantity
            marketplace["accounts"][sell["person"]]["cash"] += trade_quantity * trade_price

            # Record transaction
            transaction = {
                "buyer": buy["person"],
                "seller": sell["person"],
                "quantity": trade_quantity,
                "price": trade_price
            }
            transactions.append(transaction)
            marketplace["accounts"][buy["person"]]["transactions"].append(transaction)
            marketplace["accounts"][sell["person"]]["transactions"].append(transaction)

            # Adjust order quantities
            buy["quantity"] -= trade_quantity
            sell["quantity"] -= trade_quantity

            # Remove fully matched orders
            if buy["quantity"] == 0:
                i += 1
            if sell["quantity"] == 0:
                j += 1
        else:
            break  # No further matches possible

    # Update order book
    marketplace["order_book"] = [o for o in marketplace["order_book"] if o["quantity"] > 0]
    marketplace["transactions"].extend(transactions)
    return transactions

# API Endpoints
@app.route("/api/accounts", methods=["POST"])
def create_account():
    """Create a new account."""
    data = request.json
    name = data.get("name")
    energy = data.get("energy", 0)
    cash = data.get("cash", 1000.0)

    if not name:
        return jsonify({"error": "Name is required."}), 400

    initialize_account(name)
    marketplace["accounts"][name]["energy"] = energy
    marketplace["accounts"][name]["cash"] = cash
    return jsonify({"message": f"Account for {name} created.", "account": marketplace["accounts"][name]}), 201

@app.route("/api/orders", methods=["POST"])
def add_order():
    """Add a buy or sell order."""
    data = request.json
    person = data["person"]
    order_type = data["type"]
    quantity = data["quantity"]
    price = data["price"]

    if order_type not in ["buy", "sell"]:
        return jsonify({"error": "Order type must be 'buy' or 'sell'."}), 400
    if quantity <= 0 or price <= 0:
        return jsonify({"error": "Quantity and price must be greater than 0."}), 400

    if order_type == "sell" and marketplace["accounts"][person]["energy"] < quantity:
        return jsonify({"error": f"{person} has insufficient energy to sell."}), 400

    if order_type == "sell":
        marketplace["accounts"][person]["energy"] -= quantity

    order = {
        "id": get_next_id(),
        "type": order_type,
        "quantity": quantity,
        "price": price,
        "person": person
    }
    marketplace["order_book"].append(order)

    # Match orders dynamically
    transactions = match_orders()

    return jsonify({"message": "Order added and matched dynamically.", "order": order, "transactions": transactions}), 201

@app.route("/api/order-book", methods=["GET"])
def view_order_book():
    """View the order book."""
    return jsonify({"order_book": marketplace["order_book"]}), 200

@app.route("/api/transactions", methods=["GET"])
def view_transactions():
    """View all transactions."""
    return jsonify({"transactions": marketplace["transactions"]}), 200

@app.route("/api/accounts/<person>", methods=["GET"])
def view_account(person):
    """View account details."""
    if person not in marketplace["accounts"]:
        return jsonify({"error": f"Account for {person} not found."}), 404
    return jsonify({"account": marketplace["accounts"][person]}), 200

@app.route("/api/reset", methods=["POST"])
def reset_system():
    """Reset the marketplace."""
    marketplace["accounts"] = {}
    marketplace["order_book"] = []
    marketplace["transactions"] = []
    return jsonify({"message": "Marketplace reset successfully."}), 200

# Preload testing data
def preload_testing_data():
    accounts = [
        {"name": "Alice", "energy": 100, "cash": 1000},
        {"name": "Bob", "energy": 50, "cash": 1200},
        {"name": "Charlie", "energy": 200, "cash": 800},
        {"name": "Diana", "energy": 150, "cash": 1100}
    ]
    orders = [
        {"type": "sell", "quantity": 30, "price": 0.15, "person": "Alice"},
        {"type": "sell", "quantity": 50, "price": 0.20, "person": "Charlie"},
        {"type": "buy", "quantity": 20, "price": 0.18, "person": "Bob"},
        {"type": "buy", "quantity": 40, "price": 0.22, "person": "Diana"}
    ]
    for account in accounts:
        initialize_account(account["name"])
        marketplace["accounts"][account["name"]]["energy"] = account["energy"]
        marketplace["accounts"][account["name"]]["cash"] = account["cash"]
    for order in orders:
        marketplace["order_book"].append({
            "id": get_next_id(),
            "type": order["type"],
            "quantity": order["quantity"],
            "price": order["price"],
            "person": order["person"]
        })
    match_orders()

# Initialize testing data at startup
preload_testing_data()

if __name__ == "__main__":
    app.run(debug=True, port=8000)
