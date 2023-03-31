from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order, Listing, Trade
class Trader:
    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        result = {}
        pos_pearls = 0
        pos_banana = 0 
        for product in state.order_depths.keys():
            if product == 'PEARLS':
                order_depth: OrderDepth = state.order_depths[product]
                orders: list[Order] = []
                acceptable_price = 10000
                if len(order_depth.sell_orders) > 0:
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]		 
                    if best_ask < 9999:
                        if abs(pos_pearls + best_ask_volume) > 20:
                            if pos_pearls>=0:
                                best_ask_volume = -1*(20+pos_pearls)
                                pos_pearls+=best_ask_volume*-1
                                
                            else:
                                best_ask_volume = -1*(20+pos_pearls)
                                pos_pearls+=best_ask_volume*-1
                                
                        else:
                            pos_pearls+=best_ask_volume*-1
                            
                        orders.append(Order(product, best_ask, -1*best_ask_volume))

                if len(order_depth.buy_orders) > 0:
                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.buy_orders[best_bid]
                    if best_bid > 10000.01:
                        if abs(pos_pearls + best_bid_volume) > 20:
                            if pos_pearls>=0:
                                best_bid_volume = 20 - pos_pearls
                                pos_pearls+=best_bid_volume*-1
                            
                            else:
                                best_bid_volume = 20+pos_pearls
                                pos_pearls+=best_bid_volume*-1
                                
                        else:
                            pos_pearls+=best_bid_volume*-1
                                
                        orders.append(Order(product, best_bid, -1*best_bid_volume))

                # Add all the above the orders to the result dict
                result[product] = orders
                
            elif product=='BANANAS':
                order_depth: OrderDepth = state.order_depths[product]
                orders: list[Order] = []
                best_ask = min(order_depth.sell_orders.keys())
                best_bid = max(order_depth.buy_orders.keys())
                
                avg_asset_price = (best_ask + best_bid)/2 
                # Making Market around this price : 
                market_making_bid = 4889
                market_making_ask = 4939
                
                if len(order_depth.sell_orders) > 0:
                    best_ask_volume = order_depth.sell_orders[best_ask]		 
                    if best_ask < market_making_bid:
                        if abs(pos_banana + best_ask_volume) > 20:
                            if pos_banana>=0:
                                best_ask_volume = -1*(19+pos_banana)
                                pos_banana+=best_ask_volume*-1
                                
                            else:
                                best_ask_volume = -1*(20+pos_banana)
                                pos_banana+=best_ask_volume*-1
                                
                        else:
                            pos_banana+=best_ask_volume*-1
                    	 
                        orders.append(Order(product, best_ask, -1*best_ask_volume))

                if len(order_depth.buy_orders) > 0:
                    best_bid_volume = order_depth.buy_orders[best_bid]
                    if best_bid > market_making_ask:
                        if abs(pos_banana + best_bid_volume) > 20:
                            if pos_banana>=0:
                                best_bid_volume = 18 - pos_banana
                                pos_banana+=best_bid_volume*-1
                            
                            else:
                                best_bid_volume = 19+pos_banana
                                pos_banana+=best_bid_volume*-1
                                
                        else:
                            pos_banana+=best_bid_volume*-1
                    		
                        orders.append(Order(product, best_bid, -1*best_bid_volume))

                # Add all the above the orders to the result dict
                result[product] = orders
                
        return result
