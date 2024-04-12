import sys

from datamodel import OrderDepth, TradingState, Order
from typing import List, Tuple

timestamp_jump = 100
starfruit_product_name = 'STARFRUIT'
amethysts_product_name = 'AMETHYSTS'
active_products = [starfruit_product_name, amethysts_product_name]
starting_positions = {
    starfruit_product_name: 0,
    amethysts_product_name: 0
}
position_limits = {
    starfruit_product_name: 20,
    amethysts_product_name: 20
}
default_prices = {
    starfruit_product_name: 5_000,
    amethysts_product_name: 10_000
}


class Trader:
    def __init__(self):
        self.products_list = active_products
        self.position = dict()
        for product in self.products_list:
            self.position[product] = starting_positions[product]
        self.dev_flag = False

    def run(self, state: TradingState) -> Tuple[dict[str, list[Order]], int, str]:
        result_orders = dict()
        for product_name in self.products_list:
            result_orders[product_name] = self._run_specific_strategy(
                product_name,
                state.order_depths[product_name],
                state.timestamp
            )
        conversions = 0
        trader_data = 'gimme_seashellz'
        return result_orders, conversions, trader_data

    def _run_specific_strategy(self, product_name: str, order_depth: OrderDepth, timestamp: int) -> List[Order]:
        if product_name == starfruit_product_name:
            return self._run_starfruit_strategy(order_depth, timestamp)
        elif product_name == amethysts_product_name:
            return self._run_amethysts_strategy(order_depth, timestamp)
        else:
            raise ValueError(f'Unknown product name: {product_name}')

    def _run_starfruit_strategy(self, order_depth: OrderDepth, timestamp: int) -> List[Order]:
        pass

    def _run_amethysts_strategy(self, order_depth: OrderDepth, timestamp: int) -> List[Order]:
        pass

    @staticmethod
    def _map_order_depth_to_live_price_data(order_depth: OrderDepth) -> Tuple[int, int, int]:
        orders = []
        lowest_bot_sell_price = sys.maxsize
        highest_bot_buy_price = 0
        for price, quantity in order_depth.sell_orders.items():
            if price > 0 > quantity:
                orders.append((price, abs(quantity)))
                if price < lowest_bot_sell_price:
                    lowest_bot_sell_price = price
        for price, quantity in order_depth.buy_orders.items():
            if price > 0 and quantity > 0:
                orders.append((price, quantity))
                if price > highest_bot_buy_price:
                    highest_bot_buy_price = price
        if len(orders) == 0:
            return 0, 0, 0
        total_quantity = 0
        total_price = 0
        for price, quantity in orders:
            total_quantity += quantity
            total_price += price * quantity
        avg_price = round(total_price / total_quantity) if total_quantity > 0 else 0
        return avg_price, lowest_bot_sell_price, highest_bot_buy_price
