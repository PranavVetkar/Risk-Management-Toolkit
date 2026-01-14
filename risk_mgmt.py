import pandas as pd
import numpy as np

class RiskManager:
    def __init__(self, stop_loss_pct=0.02):
        self.stop_loss_pct = stop_loss_pct
        self.balance = 1000 
        self.position = 0
        self.entry_price = 0
        self.in_position = False

    def run_simulation(self, file_path):
        df = pd.read_csv(file_path)
        print(f"--- Starting Risk Simulation on {file_path} ---")

        for i, row in df.iterrows():
            price = row['close']
            
            if row['signal'] == 'BULLISH' and not self.in_position:
                self.in_position = True
                self.entry_price = price
                self.position = self.balance / price
                self.balance = 0
                print(f"[{row['timestamp']}] BUY at ${price:,.2f}")

            elif self.in_position:
                price_change = (price - self.entry_price) / self.entry_price
                
                if price_change <= -self.stop_loss_pct:
                    self.balance = self.position * price
                    self.in_position = False
                    print(f"[{row['timestamp']}] !!! STOP LOSS at ${price:,.2f} (Loss: {price_change*100:.2f}%)")
                    print()
                    self.position = 0
                
                elif row['signal'] == 'BEARISH':
                    self.balance = self.position * price
                    self.in_position = False
                    print(f"[{row['timestamp']}] STRATEGY EXIT at ${price:,.2f} | Balance: ${self.balance:,.2f}")
                    print()
                    self.position = 0

        final_value = self.balance if self.balance > 0 else self.position * df.iloc[-1]['close']
        print(f"FINAL PORTFOLIO VALUE: ${final_value:,.2f}")

if __name__ == "__main__":
        manager = RiskManager(stop_loss_pct = 0.01)
        manager.run_simulation('btc_history.csv')