import json
import pickle

# функция обновления цены у товара
def update_price(product, price_info):
    method = price_info["method"]
    if method == "add":
        product["price"] += price_info["param"]
    elif method == "sub":
        product["price"] -= price_info["param"]
    elif method == "percent+":
        product["price"] *= (1 + price_info["param"])
    elif method == "percent-":
        product["price"] *= (1 - price_info["param"])
    # округлим цены до двух знаков
    product["price"] = round(product["price"], 2)

# считаем данные о товарах, которые лежат в файл формата pkl
with open("products_30.pkl", "rb") as f:
    products = pickle.load(f)

# считаем данные об обновлении цен
with open("price_info_30.json") as f:
    price_info = json.load(f)


price_info_dict = dict()  # name -> {name, method, param}

for item in price_info:
    price_info_dict[item["name"]] = item


for product in products:
    current_price_info = price_info_dict.get(product["name"])
    if current_price_info:
        update_price(product, current_price_info)


with open("products_updated.pkl", "wb") as f:
    f.write(pickle.dumps(products))
