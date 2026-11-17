import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd

    from trading.data import BarStore, load_bars, load_panel

    return BarStore, load_bars, load_panel, mo, np, pd, plt


@app.cell
def _(mo):
    mo.md("""
    # Exploring stored bars

    Daily bars downloaded with `uv run trading fetch`. Prices below use the
    **adjusted close**, which folds dividends and splits in, so its changes are total returns.
    """)
    return


@app.cell
def _(BarStore, mo):
    stored = BarStore().symbols("1d")
    if not stored:
        mo.stop(True, mo.md("No bars stored yet. Run `uv run trading fetch` first."))
    default = [symbol for symbol in ("SPY", "TLT", "GLD") if symbol in stored] or stored[:3]
    picker = mo.ui.multiselect(options=stored, value=default, label="Symbols")
    picker
    return (picker,)


@app.cell
def _(load_panel, mo, picker):
    mo.stop(not picker.value, mo.md("Pick at least one symbol."))
    # Start where every picked symbol has data, so they are compared over the same period.
    prices = load_panel(picker.value).dropna()
    returns = prices.pct_change().dropna()
    mo.md(
        f"Common history: **{prices.index[0]:%Y-%m-%d}** to **{prices.index[-1]:%Y-%m-%d}** "
        f"({len(prices)} sessions)"
    )
    return prices, returns


@app.cell
def _(plt, prices):
    _fig, _ax = plt.subplots(figsize=(10, 4))
    (prices / prices.iloc[0]).plot(ax=_ax, logy=True)
    _ax.set_title("Growth of $1 (log scale)")
    _ax.set_xlabel("")
    _ax.grid(alpha=0.3)
    _fig
    return


@app.cell
def _(mo, np, pd, prices, returns):
    _years = len(returns) / 252
    _drawdown = prices / prices.cummax() - 1
    _percent = "{:.2%}".format
    stats = pd.DataFrame(
        {
            "CAGR": ((prices.iloc[-1] / prices.iloc[0]) ** (1 / _years) - 1).map(_percent),
            "Volatility": (returns.std() * np.sqrt(252)).map(_percent),
            "Sharpe (rf=0)": (returns.mean() / returns.std() * np.sqrt(252)).map("{:.2f}".format),
            "Max drawdown": _drawdown.min().map(_percent),
            "Worst day": returns.min().map(_percent),
        }
    )
    mo.vstack([mo.md("## Annualized statistics"), mo.as_html(stats)])
    return


@app.cell
def _(plt, prices):
    _fig, _ax = plt.subplots(figsize=(10, 3))
    (prices / prices.cummax() - 1).plot(ax=_ax)
    _ax.set_title("Drawdown from previous peak")
    _ax.set_xlabel("")
    _ax.grid(alpha=0.3)
    _fig
    return


@app.cell
def _(load_bars, mo, picker, plt):
    _symbol = picker.value[0]
    _bars = load_bars(_symbol)
    _fig, _ax = plt.subplots(figsize=(10, 3))
    _bars[["close", "adj_close"]].plot(ax=_ax)
    _ax.set_title(f"{_symbol}: raw close vs adjusted close")
    _ax.set_xlabel("")
    _ax.grid(alpha=0.3)
    mo.vstack(
        [
            mo.md(
                f"""
                ## Raw vs adjusted

                The raw close is the price that actually traded. The adjusted close scales
                history down by every later dividend and split, so the gap between them is
                {_symbol}'s reinvested distributions. Backtest returns on `adj_close`;
                size orders and fills on the raw prices.
                """
            ),
            _fig,
        ]
    )
    return


if __name__ == "__main__":
    app.run()
