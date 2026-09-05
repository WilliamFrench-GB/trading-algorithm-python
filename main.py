# The 12 candles are a toy dataset.
# Historical data would be needed to draw real conclusions. 
candles = [
    {"open": 125, "high": 175, "low": 110, "close": 150},
    {"open": 135, "high": 185, "low": 120, "close": 160},
    {"open": 115, "high": 165, "low": 110, "close": 140},
    {"open": 145, "high": 195, "low": 130, "close": 170},
    {"open": 155, "high": 205, "low": 140, "close": 180},
    {"open": 144, "high": 178, "low": 143, "close": 155},
    {"open": 190, "high": 190, "low": 180, "close": 185},
    {"open": 210, "high": 260, "low": 190, "close": 200},
    {"open": 130, "high": 170, "low": 130, "close": 170},
    {"open": 150, "high": 160, "low": 130, "close": 133},
    {"open": 165, "high": 177, "low": 153, "close": 161},
    {"open": 144, "high": 199, "low": 133, "close": 186}
]

# Calculate average close price.
def calculateAverageClose(candles): 
    total = 0 

    for i in range(len(candles)):
        total += candles[i]["close"]

    return total / len(candles)

print("Average close:", calculateAverageClose(candles))

# Compares only the LAST candle's close to the overall average — a single
# snapshot, not a bar-by-bar trend. A candle can be individually bearish

def detectTrend(candles):
    average = calculateAverageClose(candles)
    latestCandle =candles[len(candles)-1]

    if latestCandle["close"] > average:
        return "Bullish"
    else:
        return "Bearish"

print("Overall trend:", detectTrend(candles))

def generateSignals(candles, period):
    signals = []

    for i in range(period, len(candles)):
        window = candles[i - period : i]
        average = calculateAverageClose(window)
        currentPrice = candles[i]["close"]

        if currentPrice > average:
            signals.append({
                "bar": i,
                "signal": "BUY", 
                "currentPrice": currentPrice, 
                "average": average
                })
        elif currentPrice < average:
            signals.append({
                "bar": i, 
                "signal": "SELL", 
                "currentPrice": currentPrice, 
                "average": average
                })
        else:
            signals.append({
                "bar": i,
                "signal": "HOLD",
                "currentPrice": currentPrice,
                "average": average
            })

    return signals

signals10 = generateSignals(candles, 10)
signals5 = generateSignals(candles, 5)
signals3 = generateSignals(candles, 3)

print ("signals (period 10):", signals10)
print ("signals (period 5):", signals5)
print ("signals (period 3):", signals3)

# Counts how many signals were BUY, SELL or HOLD.

def countSignals(signals):

    buyCount = len([s for s in signals if s["signal"] == "BUY"])
    sellCount = len([s for s in signals if s["signal"] == "SELL"])
    holdCount = len([s for s in signals if s["signal"] == "HOLD"])

    return {"BUY": buyCount, "SELL": sellCount, "HOLD": holdCount}

print(countSignals(signals10))
print(countSignals(signals5))
print(countSignals(signals3))

# Excludes HOLD signals. Not a measure of profitability — see calculateWinRate for that.
def calculateBuyRatio(signals):
    counts = countSignals(signals)
    totalSignals = counts["BUY"] + counts["SELL"]

    if totalSignals == 0:
        return 0

    return counts["BUY"] / totalSignals * 100

print(calculateBuyRatio(signals10))
print(calculateBuyRatio(signals5))
print(calculateBuyRatio(signals3))

# Determines whether a single trade, entered at a given price, hits its
# win target, its stop-loss, or neither — resulting in WIN, LOSS, or UNRESOLVED.
def checkOutcome(candles, entryBar, entryPrice, winPercent, lossPercent):
    targetPrice = entryPrice * (1 + winPercent / 100)
    stopPrice = entryPrice * ( 1 - lossPercent / 100)

    for i in range(entryBar + 1, len(candles)):
        if candles[i]["high"] >= targetPrice:
            return "WIN"
        
        if candles[i]["low"]<= stopPrice:
            return "LOSS"

    return "UNRESOLVED"

print(checkOutcome(candles, 8, 170, 5, 2))

# A function returning a "plausible" result on bad input is more dangerous
# than a crash. Crashes get noticed. Silent wrong answers get shipped.
def backtest(candles, signals, winPercent, lossPercent):
    outcomes = [checkOutcome(candles, s["bar"], s["currentPrice"],winPercent, lossPercent)
                 for s in signals if s["signal"] == "BUY"]

    return outcomes

print(backtest(candles, signals5, 5, 2))

# Excludes UNRESOLVED trades from the denominator — an unresolved trade
# is neither a win nor a loss, so it shouldn't count against the rate.
def calculateWinRate(outcomes):
    winCount = len([o for o in outcomes if o == "WIN"])
    unresolvedCount = len([ o for o in outcomes if o == "UNRESOLVED"])
    totalDecided = len(outcomes) - unresolvedCount

    if totalDecided == 0:
        return 0

    return winCount / totalDecided * 100

print(calculateWinRate(backtest(candles, signals5, 5, 2)))


# NOTE: This summary currently shows raw win/loss/unresolved counts using
# .count(). It doesn't yet call calculateBuyRatio — planned as part of a
# more complete comparison view later.

outcomes10 = backtest(candles, signals10, 5, 2)
outcomes5 = backtest(candles, signals5, 5, 2)
outcomes3 = backtest(candles, signals3, 5, 2)

print({"Period 10": {
    "signals": len(signals10),
    "Wins": outcomes10.count("WIN"),
    "Losses": outcomes10.count("LOSS"),
    "Unresolved": outcomes10.count("UNRESOLVED"),
    }
})
print({"Period 5": {
    "signals": len(signals5),
    "Wins": outcomes5.count("WIN"),
    "Losses": outcomes5.count("LOSS"),
    "Unresolved": outcomes5.count("UNRESOLVED"),
    }
})
print({"Period 3": {
    "signals": len(signals3),
    "Wins": outcomes3.count("WIN"),
    "Losses": outcomes3.count("LOSS"),
    "Unresolved": outcomes3.count("UNRESOLVED"),
    }
})