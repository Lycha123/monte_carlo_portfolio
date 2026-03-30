import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns

#Wykresy
sns.set_theme(style="whitegrid")

class ActuarialPortfolioSim:
    def __init__(self, tickers, weights, initial_capital=170):
        self.tickers = tickers
        self.weights = np.array(weights)
        self.initial_capital = initial_capital
        self.returns = None

    def fetch_data(self, period="2y"):
        print(f"Pobieranie danych dla portfela: {self.tickers}...")
        data = yf.download(self.tickers, period=period, auto_adjust=True)
        close_prices = data['Close']
        self.returns = np.log(close_prices / close_prices.shift(1)).dropna()
        return self.returns

    def run_simulation(self, n_sims=10000, days=252):
        print(f"Uruchamianie {n_sims} symulacji na okres {days} dni roboczych...")
        mean_returns = self.returns.mean()
        cov_matrix = self.returns.cov()
        
        sim_returns = np.random.multivariate_normal(
            mean_returns, cov_matrix, (days, n_sims)
        )
        
        portfolio_sim_returns = np.dot(sim_returns, self.weights)
        portfolio_values = self.initial_capital * np.exp(np.cumsum(portfolio_sim_returns, axis=0))
        
        return portfolio_values

   
    def calculate_metrics(self, portfolio_values, confidence_level=0.95):
        final_values = portfolio_values[-1, :]
        losses = self.initial_capital - final_values
        
        var = np.percentile(losses, confidence_level * 100)
        cvar = losses[losses >= var].mean()
        
        #Maximum Drawdown - MDD
        peaks = np.maximum.accumulate(portfolio_values, axis=0)
        drawdowns = (portfolio_values - peaks) / peaks
        max_drawdowns = drawdowns.min(axis=0) 
        avg_mdd = max_drawdowns.mean() * 100  
        
        #Roczny zwrot 
        sim_returns_annual = (final_values / self.initial_capital) - 1
        expected_return = sim_returns_annual.mean()
        
        return var, cvar, avg_mdd, expected_return

    def plot_results(self, portfolio_values, var, cvar):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        #Wykres 1
        ax1.plot(portfolio_values[:, :100], lw=0.5, alpha=0.6)
        ax1.axhline(self.initial_capital, color='black', ls='--', label='Start')
        ax1.set_title("Scenariusze portfela (100 ścieżek)")
        ax1.set_xlabel("Dni")
        ax1.set_ylabel("Wartość (PLN)")
        
        #Wykres 2
        final_values = portfolio_values[-1, :]
        sns.histplot(final_values, bins=50, ax=ax2, kde=True, color='skyblue')
        
        var_line = self.initial_capital - var
        ax2.axvline(var_line, color='red', ls='--', label=f'VaR 95%: {var:,.2f} PLN')
        ax2.axvline(self.initial_capital - cvar, color='darkred', ls=':', label=f'CVaR 95%: {cvar:,.2f} PLN')
        
        ax2.set_title("Rozkład wartości po roku")
        ax2.set_xlabel("Wartość końcowa (PLN)")
        ax2.legend()
        
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    assets = ['NVDA', 'AAPL','DRS','NOC', 'LMT']
    weights = [0.2, 0.3, 0.1, 0.2, 0.2]
    
    sim = ActuarialPortfolioSim(assets, weights, initial_capital=10000)
    sim.fetch_data()
    
    
    results = sim.run_simulation(n_sims=10000, days=252)
    
  
    v, cv, mdd, exp_ret = sim.calculate_metrics(results)
    
    
    print(" WYNIKI SYMULACJI PORTFELA")
    print(f"Oczekiwany zysk z portfela: {exp_ret*100:,.2f}%\n")
    print(f"VaR 95%:     {v:,.2f} PLN")
    print(f"CVaR 95%: {cv:,.2f} PLN")
    print(f"Sredni Max Drawdown (MDD):   {mdd:,.2f}%")
  
    
    sim.plot_results(results, v, cv)