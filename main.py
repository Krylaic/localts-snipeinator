# localts snipe-inator

import requests
import time

api_key = input('paste your api key: ')

base = "https://localts.store/v1/"
headers = {'X-API-Key': api_key}
lol = ''

r = requests.get(base + "me", headers=headers)
data = r.json()

print("you are logged in as: " + data.get("username") + "\n")

print("=========================================")
print("      YOU CAN GET A 5% DISCOUNT ON       ")
print("   YOUR LOCALTS ORDER, BUT IT PROBABLY   ")
print("            VIOLATES THE TOS             ")
print("=========================================")
print("\nit is done by spoofing your requests as coming from rise client, which applies a discount to your order")
print("i am not responsible if you get in trouble for doing this\n")

localtsgodbypass = input("save money? (y/n): ")

if localtsgodbypass == "y":
	headers = {'X-API-Key': api_key, 'User-Agent': 'Rise-Client/6.7.10'}
	lol = '&campaign=rise'
	# dont worry i already know this is a terrible and stupid way of doing this

r = requests.get(base + "products", headers=headers)
data = r.json()

for product in data.get("products", []):
	if product.get("name") == "Hypixel Unbanned":
		while product.get("stock", 0) <= 0:
			if r.status_code != 200:
				print("rate limited, waiting a little longer")
				time.sleep(10)
			else:
				time.sleep(1)
				
			print("out of stock, trying again " + str(r.status_code))

			r = requests.get(base + "products", headers=headers)

			if r.status_code == 200:
				data = r.json()
				for p in data.get("products", []):
					if p.get("name") == "Hypixel Unbanned":
						product = p
						break

		print("in stock")
		print("purchasing the account now...")
		prod_id = product.get("id")

		r = requests.post(base + "products/" + prod_id + "/purchase?amount=1" + lol, headers=headers)
		data = r.json()

		order_id = data.get("orderId")

		if not order_id:
			print("purchase failed : ", data)
			exit()

		print("purchased, order id: " + str(order_id))

		r = requests.get(base + "orders/get-order?id=" + str(order_id) + lol, headers=headers)
		data = r.json()

		while data.get("order-status") != "COMPLETE":
			if data.get("order-status") == "REFUNDED":
				print("issue with order :(")
				exit()

			print("waiting for order to complete...")
			time.sleep(2)

			r = requests.get(base + "orders/get-order?id=" + str(order_id) + lol, headers=headers)
			data = r.json()

		print("order completed!! content:\n\n")
		for item in data.get("items", []):
			print(item.get("content"))
		break