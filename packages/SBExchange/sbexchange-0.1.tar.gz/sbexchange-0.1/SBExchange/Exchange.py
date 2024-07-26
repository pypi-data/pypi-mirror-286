import json
import os
import random

class Exchange:
    def __init__(self, filename='orders.json'):
        self.buy_orders = []
        self.sell_orders = []
        self.filename = filename
        self.load_orders()
    
    def save_orders(self):
        with open(self.filename, 'w') as file:
            json.dump({'buy_orders': self.buy_orders, 'sell_orders': self.sell_orders}, file)
    
    def load_orders(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                data = json.load(file)
                self.buy_orders = data.get('buy_orders', [])
                self.sell_orders = data.get('sell_orders', [])
    
    def CreateOrder(self, tokens, price, tokenName, userId, type):
        order = {"status": "CREATED", "token_amount": tokens, "token_price": price, "tokenName": tokenName, "userId": userId, "type": type, "id": random.randint(10000000000, 100000000000000)}
        if type.lower() == "sell":
            self.sell_orders.append(order)
        elif type.lower() == "buy":
            self.buy_orders.append(order)
        self.save_orders()
        return order.get("status")
        
    def PriceToSell(self, token_amount):
        price = (self.total_money) / (self.total_token + token_amount)
        return round(price * token_amount, 9)
        
    def Buy(self, token_amount, num_order, balance):
        price = self.buy_orders[int(num_order)].get("token_price")
        amount = self.buy_orders[int(num_order)].get("token_amount")
        result = round(price * token_amount, 9)
        if amount < token_amount:
            return "400"
        if round(balance, 9) < result:
            return "400"
        else:
            resultDict = {"order": self.buy_orders[int(num_order)], "price": result}
            return resultDict
        
    def Sell(self, token_amount, num_order):
        price = self.sell_orders[int(num_order)].get("token_price")
        amount = self.sell_orders[int(num_order)].get("token_amount")
        result = round(price * token_amount, 9)
        if amount < token_amount:
            return "400"
        else:
            resultDict = {"order": self.sell_orders[int(num_order)], "price": result}
            return resultDict
    
    def GetOrders(self):
        buy = sorted(self.buy_orders, key=lambda x: x['token_price'], reverse=True)
        sell = sorted(self.sell_orders, key=lambda x: x['token_price'], reverse=True)
        orders = {"sell": sell, "buy": buy}
        return orders
    
    def MultiSB(self, token_amount, type):
        orders = self.GetOrders()[type.lower()]
        total_price = 0
        sold = 0
        k = 0
        j = 0
        while token_amount > 0:
            for order in orders:
                token__amount = order["token_amount"]
                if token_amount >= token__amount:
                    total_price += token__amount * order["token_price"]
                    token_amount -= token__amount
                    sold += token__amount
                    orders.pop(0)
                    k += 1
                elif token_amount < token__amount:
                    total_price += token_amount * order["token_price"]
                    token_amount -= token_amount
                    sold += token_amount
                    k += 1
            j += 1
            if j != k:
                break
        self.save_orders()
        return {"price": total_price, "token_amount": token_amount, "sold": sold}
    def find_order_index_by_id(self, order_list, order_id):
        for index, order in enumerate(order_list):
            if order.get('id') == order_id:
                return index
        return -1
    def DeleteOrder(self, order_id = -1, order_index = -1, type = ""):
        orders = self.GetOrders()[type.lower()]
        if order_id != -1:
            index = self.find_order_index_by_id(orders, order_id)
            if type.lower() == "sell":
                self.sell_orders.pop(index)
            if type.lower() == "buy":
                self.buy_orders.pop(index)
        elif order_index != -1:
            index = order_index
            if type.lower() == "sell":
                self.sell_orders.pop(index)
            if type.lower() == "buy":
                self.buy_orders.pop(index)
        self.save_orders()
    def EditOrder(self, order_id = -1, order_index = -1, type = "", key = "", value = 0, operation = ""):
        orders = self.GetOrders()[type.lower()]
        if order_id != -1:
            index = self.find_order_index_by_id(orders, order_id)
            if type.lower() == "sell":
                if operation != "":
                    self.sell_orders[index][key] = eval(str(self.sell_orders[index][key]) + operation + str(value))
                else:
                    self.sell_orders[index][key] = value
            if type.lower() == "buy":
                if operation != "":
                    self.buy_orders[index][key] = eval(str(self.buy_orders[index][key]) + operation + str(value))
                else:
                    self.buy_orders[index][key] = value
        elif order_index != -1:
            index = order_index
            if type.lower() == "sell":
                if operation != "":
                    self.sell_orders[index][key] = eval(str(self.sell_orders[index][key]) + operation + str(value))
                else:
                    self.sell_orders[index][key] = value
            if type.lower() == "buy":
                if operation != "":
                    self.buy_orders[index][key] = eval(str(self.buy_orders[index][key]) + operation + str(value))
                else:
                    self.buy_orders[index][key] = value
        self.save_orders()