"""
Bellman-Ford Algorithm for Cryptocurrency Arbitrage Detection
Uses Binance.us API to fetch real-time exchange rates
"""

import requests
import math
from typing import Dict, List, Tuple, Optional
import time


class BellmanFordArbitrage:
    def __init__(self):
        self.base_url = "https://api.binance.us"
        self.graph = {}
        self.currencies = set()
        
    def fetch_exchange_rates(self) -> Dict[str, float]:
        """
        Fetch current exchange rates from Binance.us
        
        **PLACE YOUR API KEY HERE IF NEEDED**
        For public endpoints (ticker prices), no API key is required.
        If you need authenticated endpoints, add:
        headers = {
            'X-MBX-APIKEY': 'YOUR_API_KEY_HERE'
        }
        """
        try:
            # Fetch all ticker prices
            endpoint = f"{self.base_url}/api/v3/ticker/price"
            response = requests.get(endpoint, timeout=10)
            response.raise_for_status()
            
            tickers = response.json()
            rates = {}
            
            # Parse ticker data
            for ticker in tickers:
                symbol = ticker['symbol']
                price = float(ticker['price'])
                if price > 0:  # Only include valid prices
                    rates[symbol] = price
                    
            print(f"Fetched {len(rates)} trading pairs from Binance.us")
            return rates
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from Binance.us: {e}")
            return {}
    
    def build_graph(self, rates: Dict[str, float]):
        """
        Build a graph from exchange rates
        Convert to negative log for Bellman-Ford algorithm
        """
        self.graph = {}
        self.currencies = set()
        
        for symbol, price in rates.items():
            # Parse symbol (e.g., BTCUSDT -> BTC/USDT)
            # Binance.us typically uses format: BASEQUOTE
            base, quote = self._parse_symbol(symbol)
            
            if base and quote:
                self.currencies.add(base)
                self.currencies.add(quote)
                
                # Add edges in both directions
                # Forward: base -> quote
                if base not in self.graph:
                    self.graph[base] = {}
                # Use negative log to convert multiplication to addition
                self.graph[base][quote] = -math.log(price)
                
                # Reverse: quote -> base
                if quote not in self.graph:
                    self.graph[quote] = {}
                self.graph[quote][base] = -math.log(1 / price)
    
    def _parse_symbol(self, symbol: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Parse trading pair symbol into base and quote currencies
        Common patterns: BTCUSDT, ETHBTC, etc.
        """
        # Common quote currencies on Binance.us
        quote_currencies = ['USDT', 'USD', 'USDC', 'BTC', 'ETH', 'BNB', 'BUSD']
        
        for quote in quote_currencies:
            if symbol.endswith(quote):
                base = symbol[:-len(quote)]
                if base:  # Ensure base is not empty
                    return base, quote
        
        return None, None
    
    def bellman_ford(self, source: str) -> Tuple[Dict[str, float], Dict[str, Optional[str]], bool]:
        """
        Bellman-Ford algorithm to detect negative cycles (arbitrage opportunities)
        
        Returns:
            distances: Dict of shortest distances
            predecessors: Dict of predecessors for path reconstruction
            has_negative_cycle: Boolean indicating if arbitrage exists
        """
        # Initialize distances and predecessors
        distances = {currency: float('inf') for currency in self.currencies}
        predecessors = {currency: None for currency in self.currencies}
        distances[source] = 0
        
        # Relax edges |V| - 1 times
        for _ in range(len(self.currencies) - 1):
            for u in self.graph:
                for v in self.graph[u]:
                    weight = self.graph[u][v]
                    if distances[u] + weight < distances[v]:
                        distances[v] = distances[u] + weight
                        predecessors[v] = u
        
        # Check for negative cycles
        has_negative_cycle = False
        cycle_node = None
        
        for u in self.graph:
            for v in self.graph[u]:
                weight = self.graph[u][v]
                if distances[u] + weight < distances[v]:
                    has_negative_cycle = True
                    cycle_node = v
                    predecessors[v] = u
                    break
            if has_negative_cycle:
                break
        
        return distances, predecessors, has_negative_cycle
    
    def find_arbitrage_cycle(self, predecessors: Dict[str, Optional[str]], 
                            start_node: str) -> List[str]:
        """
        Reconstruct the arbitrage cycle from predecessors
        """
        cycle = []
        visited = set()
        current = start_node
        
        # Find a node in the cycle
        for _ in range(len(self.currencies)):
            if current in visited:
                break
            visited.add(current)
            current = predecessors[current]
        
        # Build the cycle
        cycle_start = current
        cycle.append(current)
        current = predecessors[current]
        
        while current != cycle_start:
            cycle.append(current)
            current = predecessors[current]
        
        cycle.append(cycle_start)
        cycle.reverse()
        
        return cycle
    
    def calculate_profit(self, cycle: List[str], rates: Dict[str, float]) -> float:
        """
        Calculate the profit percentage for an arbitrage cycle
        """
        amount = 1.0
        
        for i in range(len(cycle) - 1):
            from_curr = cycle[i]
            to_curr = cycle[i + 1]
            
            # Find the exchange rate
            symbol1 = from_curr + to_curr
            symbol2 = to_curr + from_curr
            
            if symbol1 in rates:
                amount *= rates[symbol1]
            elif symbol2 in rates:
                amount /= rates[symbol2]
        
        profit_percentage = (amount - 1.0) * 100
        return profit_percentage
    
    def detect_arbitrage(self):
        """
        Main function to detect arbitrage opportunities
        """
        print("=" * 60)
        print("Bellman-Ford Arbitrage Detection")
        print("=" * 60)
        
        # Fetch exchange rates
        print("\n1. Fetching exchange rates from Binance.us...")
        rates = self.fetch_exchange_rates()
        
        if not rates:
            print("Failed to fetch exchange rates. Exiting.")
            return
        
        # Build graph
        print("\n2. Building currency graph...")
        self.build_graph(rates)
        print(f"Graph built with {len(self.currencies)} currencies")
        
        # Run Bellman-Ford from multiple sources
        print("\n3. Running Bellman-Ford algorithm...")
        arbitrage_found = False
        
        # Try a few major currencies as starting points
        test_currencies = ['BTC', 'ETH', 'USDT', 'USD', 'BNB']
        available_test = [c for c in test_currencies if c in self.currencies]
        
        if not available_test:
            available_test = list(self.currencies)[:5]
        
        for source in available_test:
            distances, predecessors, has_negative_cycle = self.bellman_ford(source)
            
            if has_negative_cycle:
                print(f"\n🎯 ARBITRAGE OPPORTUNITY DETECTED (starting from {source})!")
                arbitrage_found = True
                
                # Find and display the cycle
                cycle = self.find_arbitrage_cycle(predecessors, source)
                print(f"\nArbitrage Cycle: {' -> '.join(cycle)}")
                
                # Calculate profit
                profit = self.calculate_profit(cycle, rates)
                print(f"Estimated Profit: {profit:.4f}%")
                
                # Show exchange rates in the cycle
                print("\nExchange rates in cycle:")
                for i in range(len(cycle) - 1):
                    from_curr = cycle[i]
                    to_curr = cycle[i + 1]
                    symbol1 = from_curr + to_curr
                    symbol2 = to_curr + from_curr
                    
                    if symbol1 in rates:
                        print(f"  {from_curr} -> {to_curr}: {rates[symbol1]:.8f}")
                    elif symbol2 in rates:
                        print(f"  {from_curr} -> {to_curr}: {1/rates[symbol2]:.8f}")
                
                break
        
        if not arbitrage_found:
            print("\n✓ No arbitrage opportunities detected at this time.")
            print("Note: In efficient markets, arbitrage opportunities are rare and short-lived.")


def main():
    """
    Main execution function
    """
    detector = BellmanFordArbitrage()
    
    # Run detection
    detector.detect_arbitrage()
    
    print("\n" + "=" * 60)
    print("Analysis complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()