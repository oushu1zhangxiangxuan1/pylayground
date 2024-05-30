# 示例代码
def calculate_total_price(prices, discounts):
    total_price = 0
    for price, discount in zip(prices, discounts):
        total_price += price * (1 - discount)
    return total_price

prices = [100, 200, 300]
discounts = [0.1, 0.2, 0.3]

print(calculate_total_price(prices, discounts))
