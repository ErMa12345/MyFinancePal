import pandas as pd
import numpy as np
import yfinance as yf
import requests
import itertools
from sklearn.linear_model import LinearRegression
import tickerToSector


# Get the tuple (mean, variance) of a stock over the past year
def getMeanVar(ticker):
  ibm_data = yf.Ticker(ticker)
  hist_data = ibm_data.history(period="1y")
  mean = hist_data['Close'].mean()
  variance = hist_data['Close'].pct_change().std()
  return (mean, variance)


# Get standard deviation of stock returns for a certain ticker over its entire time period
def getStdReturns(ticker):
  ibm_data = yf.Ticker(ticker)
  hist_data = ibm_data.history(period="max")
  volatility = hist_data['Close'].pct_change().std()
  return volatility


# Get the covariance between two stocks by analyzing correlation between their stock trends over the past year
def covariance(ticker1, ticker2):
  ticker1_object = yf.Ticker(ticker1)
  ticker2_object = yf.Ticker(ticker2)
  stock1_data = ticker1_object.history(period="1y")
  stock2_data = ticker2_object.history(period="1y")
  stock1_returns = stock1_data['Close'].pct_change().dropna()
  stock2_returns = stock2_data['Close'].pct_change().dropna()
  correlation_coefficient = stock1_returns.corr(stock2_returns)
  return correlation_coefficient


# Sum all of the covariances for each pair within a given portfolio
def sumCovariances(portfolio):
  weighted_correlations = []
  ticker_objects = {ticker: yf.Ticker(ticker) for ticker in portfolio.keys()}

  for pair in itertools.combinations(portfolio.keys(), 2):
    stock1_weight = portfolio[pair[0]]
    stock2_weight = portfolio[pair[1]]
    stock1_data = pair[0]
    stock2_data = pair[1]

    cov = covariance(stock1_data, stock2_data)
    weighted_correlation = stock1_weight * stock2_weight * cov
    weighted_correlations.append(weighted_correlation)

  return np.sum(weighted_correlations)


# Get the portfolio variance by calling the sumCovariances function and adding
def portfolioVariance(portfolio):
  var = sumCovariances(portfolio)
  for ticker, weight in portfolio.items():
    var += (weight)**2 * getMeanVar(ticker)[1]
  return var


# Calculate the covariances between every pair and return the pairs from highest to lowest covariances
def find_high_covariance_pairs(portfolio, threshold):
  high_covariance_pairs = []
  for pair in itertools.combinations(portfolio.keys(), 2):
    stock1_weight = portfolio[pair[0]]
    stock2_weight = portfolio[pair[1]]
    corr = covariance(pair[0], pair[1])
    if corr is not None and abs(corr) >= threshold:
      high_covariance_pairs.append((pair[0], pair[1], corr))
  high_covariance_pairs.sort(key=lambda x: abs(x[2]), reverse=True)
  return high_covariance_pairs


# Get the beta value (amount of systematic risk relative to the S&P500) of a single stock
def calculate_beta(ticker):
  asset_data = yf.Ticker(ticker).history(period="1y")['Close'].pct_change().dropna()
  market_index_data = yf.Ticker("VOO").history(period="1y")['Close'].pct_change().dropna()
  covariance = asset_data.cov(market_index_data)
  market_variance = market_index_data.var()
  beta = covariance / market_variance
  return beta


# Get the weighted betas using portfolio weights of each stock
def weighted_betas(portfolio):
  portfolio_betas = {}
  for asset_ticker, weight in portfolio.items():
    beta = calculate_beta(asset_ticker)
    portfolio_betas[asset_ticker] = beta * weight
  sorted_portfolio_betas = dict(sorted(portfolio_betas.items(), key=lambda item: item[1], reverse=True))
  return sorted_portfolio_betas


# Get the beta of the entire portfolio (how risky is the portfolio relative to the P500)
def calculate_portfolio_beta(portfolio):
  total_portfolio_beta = 0
  total_portfolio_weight = 0
  for asset_ticker, weight in portfolio.items():
    beta = calculate_beta(asset_ticker)
    total_portfolio_beta += beta * weight
    total_portfolio_weight += weight
  portfolio_beta = total_portfolio_beta / total_portfolio_weight
  return portfolio_beta


# Return r squared of a stock compared to an index (percentage of a stock's movements that can be explained by movements in a benchmark index)
def calculate_r_squared(asset_ticker, market_index_ticker):
  asset_data = yf.Ticker(asset_ticker).history(period="1y")['Close'].pct_change().dropna().values.reshape(-1, 1)
  market_data = yf.Ticker(market_index_ticker).history(period="1y")['Close'].pct_change().dropna().values.reshape(-1,
                                                                                                                  1)
  model = LinearRegression()
  model.fit(market_data, asset_data)
  r_squared = model.score(market_data, asset_data)
  return r_squared


# Return r squared of a portfolio compared to an index (percentage of the portfolio's movements that can be explained by movements in a benchmark index)
def calculate_portfolio_r_squared(portfolio, market_index_ticker, period="1y"):
  market_data = yf.Ticker(market_index_ticker).history(period=period)['Close'].pct_change().dropna().values.reshape(
    -1, 1)
  portfolio_returns = []
  portfolio_weights = []
  for asset_ticker, weight in portfolio.items():
    asset_data = yf.Ticker(asset_ticker).history(period=period)['Close'].pct_change().dropna().values.reshape(-1, 1)
    portfolio_returns.append(asset_data)
    portfolio_weights.append(weight)
  portfolio_returns = np.hstack(portfolio_returns)
  weighted_portfolio_returns = np.dot(portfolio_returns, portfolio_weights)
  model = LinearRegression()
  model.fit(market_data, weighted_portfolio_returns)
  r_squared = model.score(market_data, weighted_portfolio_returns)
  return r_squared


# Convert dictionary of tickers to number of shares to a dictionary of tickers to portfolio weights
def generate_portfolio(shares_portfolio):
  stock_prices = {}
  for ticker, shares in shares_portfolio.items():
    data = yf.Ticker(ticker).history(period="1d")
    if not data.empty:
      stock_prices[ticker] = data.iloc[-1]['Close']
  total_value = sum(
    shares * price for ticker, shares in shares_portfolio.items() for price in [stock_prices.get(ticker, 0)])
  portfolio = {ticker: (shares * price) / total_value for ticker, shares in shares_portfolio.items() for price in
               [stock_prices.get(ticker, 0)]}
  return portfolio


def beta_variances(portfolio):
  ret = {}
  for ticker, weight in portfolio.items():
    ret[ticker] = (weight, calculate_beta(ticker), getMeanVar(ticker)[1])
  return ret


def get_analysis_data(portfolio):
  var = portfolioVariance(portfolio)
  beta = calculate_portfolio_beta(portfolio)
  r2 = calculate_portfolio_r_squared(portfolio)
  return (var, beta, r2)


def suggestIndexFromTicker(ticker, portfolio):
  indexes_map = {'Basic Materials': "VMIAX", 'Industrials': "XLI", 'Consumer Goods': "XLP", 'Healthcare': "IXJ", 'Financial Services': "XLF", 'Technology and Communication': "IXN", 'Real estate and utilities': "XLRE"}
  index = 'IBM'
  r = calculate_r_squared(ticker, index)
  var1 = portfolioVariance(portfolio)
  newPortfolio = portfolio.copy()
  rem = newPortfolio.pop(ticker)
  newPortfolio[index] = rem
  var2 = portfolioVariance(newPortfolio)
  beta1 = calculate_beta(ticker)
  beta2 = calculate_beta(index)
  return (r, var1, var2, beta1, beta2)


def suggestIndex(portfolio):
  best = 1
  r = 1
  var1 = 1
  var2 = 1
  beta1 = 1
  beta2 = 1
  for ticker, weight in portfolio.items():
    r0, var10, var20, beta10, beta20 = suggestIndexFromTicker(ticker, portfolio)
    print(ticker)
    print(r, var1, var2, beta1, beta2)
    if (var20 - var10) < best:
      best = var20 - var10
      r, var1, var2, beta1, beta2 = r0, var10, var20, beta10, beta20
  return (r, var1, var2, beta1, beta2)