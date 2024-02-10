import pandas as pd
import numpy as np
import yfinance as yf
import requests
import itertools


def getMeanVar(ticker):
  ibm_data = yf.Ticker(ticker)
  hist_data_last_30_days = ibm_data.history(period="1y")
  mean = hist_data_last_30_days['Close'].mean()
  variance = hist_data_last_30_days['Close'].pct_change().std()
  return (mean, variance)


def getStdReturns(ticker):
  ibm_data = yf.Ticker(ticker)
  hist_data = ibm_data.history(period="max")
  volatility = hist_data['Close'].pct_change().std()
  return volatility


def covariance(ticker1, ticker2):
  ticker1_object = yf.Ticker(ticker1)
  ticker2_object = yf.Ticker(ticker2)
  stock1_data = ticker1_object.history(period="1y")
  stock2_data = ticker2_object.history(period="1y")
  stock1_returns = stock1_data['Close'].pct_change().dropna()
  stock2_returns = stock2_data['Close'].pct_change().dropna()
  correlation_coefficient = stock1_returns.corr(stock2_returns)
  return correlation_coefficient


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


def portfolioVariance(portfolio):
  var = sumCovariances(portfolio)
  for ticker, prop in portfolio.items():
    var += (prop)**2 * getMeanVar(ticker)[1];
  return var


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


def calculate_beta(ticker):
  asset_data = yf.Ticker(ticker).history(period="1y")['Close'].pct_change().dropna()
  market_index_data = yf.Ticker("VOO").history(period="1y")['Close'].pct_change().dropna()
  covariance = asset_data.cov(market_index_data)
  market_variance = market_index_data.var()
  beta = covariance / market_variance
  return beta


def calculate_portfolio_betas(portfolio):
  portfolio_betas = {}
  for asset_ticker, weight in portfolio.items():
    beta = calculate_beta(asset_ticker)
    portfolio_betas[asset_ticker] = beta * weight  # Adjust beta by weight
  sorted_portfolio_betas = dict(sorted(portfolio_betas.items(), key=lambda item: item[1], reverse=True))
  return sorted_portfolio_betas