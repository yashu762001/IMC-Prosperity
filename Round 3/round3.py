from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order, Listing, Trade
class Trader:
    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        result = {}
        pos_pearls = 0
        pos_banana = 0 
        pos_diving = 0 
        pos_berries = 0
        for product in state.order_depths.keys():
            if product=='DIVING_GEAR':
                order_depth: OrderDepth = state.order_depths[product]
                orders: list[Order] = []
                dolphin_price = state.observations['DOLPHIN_SIGHTINGS']
                expected_diving_price = dolphin_price*32.22
                if len(order_depth.buy_orders) > 0:
                    best_bid = max(order_depth.buy_orders.keys())
                    if best_bid >= expected_diving_price:
                        available_qty = order_depth.buy_orders[best_bid]
                        if abs(-1*available_qty + pos_diving) > 50:
                            if pos_diving >= 0:
                                poss_qty = 50 + pos_diving
                                orders.append(Order(product, best_bid, -1*poss_qty))
                                pos_diving+=-1*poss_qty
                            
                            else:
                                poss_qty = 50 - abs(pos_diving)
                                orders.append(Order(product, best_bid, -1*poss_qty))
                                pos_diving+=-1*poss_qty
                        
                        else:
                            orders.append(Order(product, best_bid, -1*available_qty))
                            pos_diving+=-1*available_qty
                            
                
                if len(order_depth.sell_orders) > 0:
                    best_ask = min(order_depth.sell_orders.keys())
                    if best_ask <= expected_diving_price:
                        available_qty = order_depth.sell_orders[best_ask]
                        if abs(-1*available_qty + pos_diving) > 50:
                            if pos_diving >= 0:
                                poss_qty = 50 - pos_diving
                                orders.append(Order(product, best_ask, poss_qty))
                                pos_diving+=poss_qty
                            
                            else:
                                poss_qty = 50 - pos_diving
                                orders.append(Order(product, best_ask, poss_qty))
                                pos_diving+=poss_qty
                        
                        else:
                            orders.append(Order(product, best_ask, -1*available_qty))
                            pos_diving+=-1*available_qty
                            
                result[product] = orders
            
            
            if product == 'BERRIES':
                support = 3845.4
                resistance = 4001
                order_depth: OrderDepth = state.order_depths[product]
                orders: list[Order] = []
                if len(order_depth.buy_orders) > 0:
                    best_bid = max(order_depth.buy_orders.keys())
                    if best_bid >= resistance - 40:
                        available_qty = order_depth.buy_orders[best_bid]
                        if abs(-1*available_qty + pos_berries) > 250:
                            if pos_berries >= 0:
                                poss_qty = 250 + pos_berries
                                orders.append(Order(product, best_bid, -1*poss_qty))
                                pos_berries+=-1*poss_qty
                            
                            else:
                                poss_qty = 250 - abs(pos_berries)
                                orders.append(Order(product, best_bid, -1*poss_qty))
                                pos_berries+=-1*poss_qty
                        
                        else:
                            orders.append(Order(product, best_bid, -1*available_qty))
                            pos_berries+=-1*available_qty
                            
                if len(order_depth.sell_orders) > 0:
                    best_ask = min(order_depth.sell_orders.keys())
                    if best_ask <= support + 35:
                        available_qty = order_depth.sell_orders[best_ask]
                        if abs(-1*available_qty + pos_berries) > 250:
                            if pos_berries >= 0:
                                poss_qty = 250 - pos_berries
                                orders.append(Order(product, best_ask, poss_qty))
                                pos_berries+=poss_qty
                            
                            else:
                                poss_qty = 250 - pos_berries
                                orders.append(Order(product, best_ask, poss_qty))
                                pos_berries+=poss_qty
                        
                        else:
                            orders.append(Order(product, best_ask, -1*available_qty))
                            pos_berries+=-1*available_qty
                            
                result[product] = orders
                
            
            if product == 'PEARLS':
                order_depth: OrderDepth = state.order_depths[product]
                orders: list[Order] = []
                acceptable_price = 10000
                if len(order_depth.sell_orders) > 0:
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]		 
                    if best_ask < 9999:
                        if abs(pos_pearls + -1*best_ask_volume) > 20:
                            if pos_pearls>=0:
                                best_ask_volume = 20-pos_pearls
                                pos_pearls+=best_ask_volume
                                
                            else:
                                best_ask_volume = (20-pos_pearls)
                                pos_pearls+=best_ask_volume
                                
                        else:
                            pos_pearls+=best_ask_volume*-1
                            best_ask_volume*=-1
                            
                        orders.append(Order(product, best_ask, best_ask_volume))

                if len(order_depth.buy_orders) > 0:
                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.buy_orders[best_bid]
                    if best_bid > 10000.01:
                        if abs(pos_pearls + -1*best_bid_volume) > 20:
                            if pos_pearls>=0:
                                best_bid_volume = -1*(20 + pos_pearls)
                                pos_pearls+=best_bid_volume
                            
                            else:
                                best_bid_volume = -1*(20 + pos_pearls)
                                pos_pearls+=best_bid_volume
                                
                        else:
                            pos_pearls+=best_bid_volume*-1
                            best_bid_volume*=-1
                                
                        orders.append(Order(product, best_bid, best_bid_volume))

                # Add all the above the orders to the result dict
                result[product] = orders
                
            if product=='BANANAS':
                order_depth: OrderDepth = state.order_depths[product]
                orders: list[Order] = []
                best_ask = min(order_depth.sell_orders.keys())
                best_bid = max(order_depth.buy_orders.keys())
                
                avg_asset_price = (best_ask + best_bid)/2 
                # Making Market around this price : 
                market_making_bid = 4814
                market_making_ask = 4820
                
                if len(order_depth.sell_orders) > 0:
                    best_ask_volume = order_depth.sell_orders[best_ask]		 
                    if best_ask <= market_making_bid:
                        if abs(pos_banana + -1*best_ask_volume) > 20:
                            if pos_banana>=0:
                                best_ask_volume = 19 - pos_banana
                                pos_banana+=best_ask_volume
                                
                            else:
                                best_ask_volume = 20 - pos_banana
                                pos_banana+=best_ask_volume
                                
                        else:
                            pos_banana+=best_ask_volume*-1
                            best_ask_volume*=-1
                    	 
                        orders.append(Order(product, best_ask, best_ask_volume))

                if len(order_depth.buy_orders) > 0:
                    best_bid_volume = order_depth.buy_orders[best_bid]
                    if best_bid >= market_making_ask:
                        if abs(pos_banana + -1*best_bid_volume) > 20:
                            if pos_banana>=0:
                                best_bid_volume = (18 + pos_banana)*-1
                                pos_banana+=best_bid_volume
                            
                            else:
                                best_bid_volume = (19+pos_banana)*-1
                                pos_banana+=best_bid_volume
                                
                        else:
                            pos_banana+=best_bid_volume*-1
                            best_bid_volume*=-1
                    		
                        orders.append(Order(product, best_bid, best_bid_volume))

                # Add all the above the orders to the result dict
                result[product] = orders
                
        return result
