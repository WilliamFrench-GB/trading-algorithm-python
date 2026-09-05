## Status

JavaScript version fully ported to Python. Every function
(calculateAverageClose, detectTrend, generateSignals, countSignals,
calculateBuyRatio, checkOutcome, backtest, calculateWinRate) verified
against the original JS output to confirm the port is correct.

Known limitations (carried over from the JS version):
- 12-candle dataset demonstrates mechanics, not statistically meaningful
- checkOutcome assumes WIN is checked before LOSS within a candle
- Final summary currently shows raw win/loss/unresolved counts,
  not yet using calculateBuyRatio — planned improvement

Next: heading into LeetCode practice for algorithmic fundamentals,
then back to extend this with real historical data and pandas/numpy.
