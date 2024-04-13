import requests
import webbrowser

# CHANGE THE VARIABLE BELOW TO YOUR FLASK URL
FLASK_URL = "http://localhost:8888/"


def http(method, path, data=None):
    print(f"Making {method} request to {FLASK_URL + path}...")
    if method not in ["GET", "POST", "PUT", "DELETE"]:
        raise RuntimeWarning("Invalid method")

    if method == "GET":
        response = requests.get(FLASK_URL + path)
    elif method == "POST":
        response = requests.post(FLASK_URL + path, json=data)
    elif method == "PUT":
        response = requests.put(FLASK_URL + path, json=data)
    elif method == "DELETE":
        response = requests.delete(FLASK_URL + path)

    print("Received status code:", response.status_code)
    return response


def get(path):
    return http("GET", path)


def post(path, data=None):
    return http("POST", path, data)


def put(path, data=None):
    return http("PUT", path, data)


def delete(path):
    return http("DELETE", path)


def demo():
    print("Adding a new product: 'salty nuts' (6.99)")
    post("api/products/", {"name": "salty nuts", "price": 6.99})
    input("Check for salty nuts in the web page. Press Enter when ready.")
    webbrowser.open(FLASK_URL + "products")
    input("Updating the product price of product 1 to 7.99. Press Enter when ready.")
    put("api/products/1", {"price": 7.99})
    input("Check for the price change in the web page. Press Enter when ready.")
    webbrowser.open(FLASK_URL + "products")
    input("Deleting third... press Enter when ready.")
    delete("api/products/3")
    input("Check for product in the web page. Press Enter when ready.")
    webbrowser.open(FLASK_URL + "products")
    input("Press Enter to continue.")
    input("Adding a customer: 'Rylan Raj, phone: 778-980-5743... Press Enter when ready.")
    post("api/customers", {"name": "Rylan Raj", "phone": "778-980-5743"})
    input("Check for Rylan in the web page. Press Enter when ready.")
    webbrowser.open(FLASK_URL + "customers")
    input("Updating the balance of customer 1 to $1000. Press Enter when ready.")
    put("api/customers/1", {"balance": 1000})
    input("Check for the balance change in the web page. Press Enter when ready.")
    webbrowser.open(FLASK_URL + "api/customers/1")
    input("Deleting first customer press Enter when ready.")
    delete("api/customers/1")
    input("Check for customer in the web page. Press Enter when ready.")
    webbrowser.open(FLASK_URL + "customers")
    input("Press Enter to continue.")
    input("Changing the amount of product 2 (bananas) to 10. Press Enter when ready.")
    put("api/products/2", {"available": 10})
    input("Check for the change in the web page. Press Enter when ready.")
    webbrowser.open(FLASK_URL + "products")
    input("Press Enter to continue.")
    input("Change customer 2 balance to 100. Press Enter when ready.")
    put("api/customers/2", {"balance": 100})
    input("Check for the change in the web page. Press Enter when ready.")
    webbrowser.open(FLASK_URL + "api/customers/2")
    input("Press Enter to continue.")
    input("Creating an order for customer 2 with product 2 of quantity 5 Press Enter when ready.")
    post("api/orders", {"customer_id": 2,
                        "items": [
                            {"name": "bananas", "quantity": 5}
                        ]
                        })


if __name__ == "__main__":
    demo()
