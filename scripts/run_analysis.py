import os
import pandas as pd
import numpy as np

# Headless plotting (for CI/terminal runs)
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter


def main() -> None:
    os.makedirs("reports", exist_ok=True)

    fear_df = pd.read_csv("data/fear_greed_index.csv")
    hist_df = pd.read_csv("data/historical_data.csv")

    # Parse dates
    fear_df["date"] = pd.to_datetime(fear_df["date"]).dt.normalize()
    hist_df["datetime_ist"] = pd.to_datetime(
        hist_df["Timestamp IST"], format="%d-%m-%Y %H:%M"
    )
    hist_df["date"] = hist_df["datetime_ist"].dt.normalize()

    # Per-trade fields
    hist_df["side"] = hist_df["Side"].astype(str).str.upper().str.strip()
    hist_df["is_buy"] = hist_df["side"].eq("BUY").astype(int)
    hist_df["is_sell"] = hist_df["side"].eq("SELL").astype(int)

    hist_df["fee_usd"] = hist_df["Fee"].astype(float)
    hist_df["closed_pnl_usd"] = hist_df["Closed PnL"].astype(float)
    hist_df["net_pnl_usd"] = hist_df["closed_pnl_usd"] - hist_df["fee_usd"]

    hist_df["is_pnl_event"] = hist_df["closed_pnl_usd"].ne(0)
    hist_df["is_win"] = (hist_df["net_pnl_usd"] > 0) & hist_df["is_pnl_event"]

    hist_df["trade_size_usd"] = hist_df["Size USD"].astype(float)
    hist_df["buy_volume_usd"] = np.where(
        hist_df["is_buy"].eq(1), hist_df["trade_size_usd"], 0.0
    )
    hist_df["sell_volume_usd"] = np.where(
        hist_df["is_sell"].eq(1), hist_df["trade_size_usd"], 0.0
    )

    # Position size proxy (true leverage isn't present in this export)
    hist_df["start_pos_tokens"] = hist_df["Start Position"].astype(float)
    hist_df["execution_price"] = hist_df["Execution Price"].astype(float)
    hist_df["start_pos_notional_usd"] = (
        hist_df["start_pos_tokens"].abs() * hist_df["execution_price"]
    ).astype(float)

    # Account-day metrics
    acct_daily = (
        hist_df.groupby(["date", "Account"])
        .agg(
            fills=("trade_size_usd", "size"),
            trade_count=("Trade ID", "nunique"),
            buy_fills=("is_buy", "sum"),
            sell_fills=("is_sell", "sum"),
            total_volume_usd=("trade_size_usd", "sum"),
            avg_trade_size_usd=("trade_size_usd", "mean"),
            median_trade_size_usd=("trade_size_usd", "median"),
            p90_trade_size_usd=("trade_size_usd", lambda s: s.quantile(0.90)),
            p95_trade_size_usd=("trade_size_usd", lambda s: s.quantile(0.95)),
            total_closed_pnl_usd=("closed_pnl_usd", "sum"),
            total_fees_usd=("fee_usd", "sum"),
            total_net_pnl_usd=("net_pnl_usd", "sum"),
            pnl_event_count=("is_pnl_event", "sum"),
            win_count=("is_win", "sum"),
            buy_volume_usd=("buy_volume_usd", "sum"),
            sell_volume_usd=("sell_volume_usd", "sum"),
            max_start_pos_notional_usd=("start_pos_notional_usd", "max"),
        )
        .reset_index()
    )

    acct_daily["win_rate"] = np.where(
        acct_daily["pnl_event_count"] > 0,
        acct_daily["win_count"] / acct_daily["pnl_event_count"],
        np.nan,
    )
    acct_daily["net_flow_usd"] = acct_daily["buy_volume_usd"] - acct_daily["sell_volume_usd"]
    acct_daily["buy_volume_share"] = acct_daily["buy_volume_usd"] / (
        acct_daily["total_volume_usd"] + 1e-9
    )
    acct_daily["buy_fill_share"] = acct_daily["buy_fills"] / (acct_daily["fills"] + 1e-9)
    acct_daily["buy_sell_ratio"] = np.where(
        acct_daily["sell_volume_usd"] > 0,
        acct_daily["buy_volume_usd"] / acct_daily["sell_volume_usd"],
        np.nan,
    )

    # Regime mapping
    fear_map = {
        "Extreme Fear": "Fear",
        "Fear": "Fear",
        "Neutral": "Neutral",
        "Greed": "Greed",
        "Extreme Greed": "Greed",
    }
    fear_df["regime"] = fear_df["classification"].map(fear_map)

    # Day-level metrics
    daily_metrics = (
        acct_daily.groupby("date")
        .agg(
            active_traders=("Account", "nunique"),
            trades=("trade_count", "sum"),
            fills=("fills", "sum"),
            buy_fills=("buy_fills", "sum"),
            sell_fills=("sell_fills", "sum"),
            total_volume_usd=("total_volume_usd", "sum"),
            avg_trade_size_usd=("avg_trade_size_usd", "mean"),
            total_net_pnl_usd=("total_net_pnl_usd", "sum"),
            pnl_event_count=("pnl_event_count", "sum"),
            win_count=("win_count", "sum"),
            buy_volume_usd=("buy_volume_usd", "sum"),
            sell_volume_usd=("sell_volume_usd", "sum"),
            p95_max_start_pos_notional_usd=(
                "max_start_pos_notional_usd",
                lambda s: s.quantile(0.95),
            ),
        )
        .reset_index()
    )

    daily_metrics["pnl_per_trader"] = daily_metrics["total_net_pnl_usd"] / (
        daily_metrics["active_traders"] + 1e-9
    )
    daily_metrics["win_rate"] = np.where(
        daily_metrics["pnl_event_count"] > 0,
        daily_metrics["win_count"] / daily_metrics["pnl_event_count"],
        np.nan,
    )
    daily_metrics["net_flow_usd"] = daily_metrics["buy_volume_usd"] - daily_metrics["sell_volume_usd"]
    daily_metrics["buy_volume_share"] = daily_metrics["buy_volume_usd"] / (
        daily_metrics["total_volume_usd"] + 1e-9
    )
    daily_metrics["buy_fill_share"] = daily_metrics["buy_fills"] / (
        daily_metrics["fills"] + 1e-9
    )
    daily_metrics["buy_sell_ratio"] = np.where(
        daily_metrics["sell_volume_usd"] > 0,
        daily_metrics["buy_volume_usd"] / daily_metrics["sell_volume_usd"],
        np.nan,
    )

    aligned_daily = daily_metrics.merge(
        fear_df[["date", "value", "classification", "regime"]].drop_duplicates("date"),
        on="date",
        how="inner",
    )

    aligned_acct = acct_daily.merge(
        fear_df[["date", "value", "classification", "regime"]].drop_duplicates("date"),
        on="date",
        how="inner",
    )

    # Fear vs Greed subsets
    fg_daily = aligned_daily[aligned_daily["regime"].isin(["Fear", "Greed"])].copy()
    fg_acct = aligned_acct[aligned_acct["regime"].isin(["Fear", "Greed"])].copy()
    fg_acct = fg_acct.sort_values(["Account", "date"])

    # Drawdown proxy per account: cumulative net PnL and drawdown from peak
    fg_acct["cum_net_pnl"] = fg_acct.groupby("Account")["total_net_pnl_usd"].cumsum()
    fg_acct["cum_peak"] = fg_acct.groupby("Account")["cum_net_pnl"].cummax()
    fg_acct["drawdown_proxy"] = fg_acct["cum_net_pnl"] - fg_acct["cum_peak"]

    # Tables
    perf_by_regime = (
        fg_acct.groupby("regime")
        .agg(
            acct_days=("Account", "size"),
            traders=("Account", "nunique"),
            net_pnl_mean=("total_net_pnl_usd", "mean"),
            net_pnl_median=("total_net_pnl_usd", "median"),
            win_rate_mean=("win_rate", "mean"),
            win_rate_median=("win_rate", "median"),
            drawdown_mean=("drawdown_proxy", "mean"),
            drawdown_p05=("drawdown_proxy", lambda s: s.quantile(0.05)),
        )
        .reset_index()
    )

    daily_by_regime = (
        fg_daily.groupby("regime")
        .agg(
            days=("date", "nunique"),
            active_traders_mean=("active_traders", "mean"),
            trades_mean=("trades", "mean"),
            fills_mean=("fills", "mean"),
            total_volume_usd_mean=("total_volume_usd", "mean"),
            pnl_per_trader_mean=("pnl_per_trader", "mean"),
            pnl_per_trader_median=("pnl_per_trader", "median"),
            win_rate_mean=("win_rate", "mean"),
            buy_volume_share_mean=("buy_volume_share", "mean"),
            buy_fill_share_mean=("buy_fill_share", "mean"),
            net_flow_usd_mean=("net_flow_usd", "mean"),
            p95_max_pos_mean=("p95_max_start_pos_notional_usd", "mean"),
        )
        .reset_index()
    )

    perf_by_regime.to_csv("reports/table_perf_by_regime.csv", index=False)
    daily_by_regime.to_csv("reports/table_daily_by_regime.csv", index=False)

    # Segments (2–3)
    acct_summary = (
        fg_acct.groupby("Account")
        .agg(
            active_days=("date", "nunique"),
            total_net_pnl=("total_net_pnl_usd", "sum"),
            avg_daily_pnl=("total_net_pnl_usd", "mean"),
            pnl_std=("total_net_pnl_usd", "std"),
            avg_trades_per_day=("trade_count", "mean"),
            avg_fills_per_day=("fills", "mean"),
            median_max_pos=("max_start_pos_notional_usd", "median"),
            win_rate_mean=("win_rate", "mean"),
        )
        .reset_index()
    )
    acct_dd = (
        fg_acct.groupby("Account")["drawdown_proxy"]
        .min()
        .reset_index()
        .rename(columns={"drawdown_proxy": "max_drawdown_proxy"})
    )
    acct_summary = acct_summary.merge(acct_dd, on="Account", how="left")

    q25 = acct_summary["median_max_pos"].quantile(0.25)
    q75 = acct_summary["median_max_pos"].quantile(0.75)
    acct_summary["pos_size_segment"] = np.where(
        acct_summary["median_max_pos"] >= q75,
        "High position size",
        np.where(acct_summary["median_max_pos"] <= q25, "Low position size", "Mid"),
    )

    t25 = acct_summary["avg_trades_per_day"].quantile(0.25)
    t75 = acct_summary["avg_trades_per_day"].quantile(0.75)
    acct_summary["frequency_segment"] = np.where(
        acct_summary["avg_trades_per_day"] >= t75,
        "Frequent",
        np.where(acct_summary["avg_trades_per_day"] <= t25, "Infrequent", "Mid"),
    )

    wr_med = acct_summary["win_rate_mean"].median(skipna=True)
    std_med = acct_summary["pnl_std"].median(skipna=True)
    acct_summary["consistency_segment"] = np.where(
        (acct_summary["total_net_pnl"] > 0)
        & (acct_summary["win_rate_mean"] >= wr_med)
        & (acct_summary["pnl_std"] <= std_med),
        "Consistent winner",
        np.where(
            acct_summary["total_net_pnl"] > 0,
            "Profitable but inconsistent",
            "Unprofitable",
        ),
    )

    segA = (
        acct_summary[acct_summary["pos_size_segment"].isin(["Low position size", "High position size"])]
        .groupby("pos_size_segment")
        .agg(
            traders=("Account", "nunique"),
            total_net_pnl_mean=("total_net_pnl", "mean"),
            win_rate_mean=("win_rate_mean", "mean"),
            pnl_std_mean=("pnl_std", "mean"),
            max_dd_mean=("max_drawdown_proxy", "mean"),
            avg_trades_per_day=("avg_trades_per_day", "mean"),
            median_max_pos=("median_max_pos", "median"),
        )
        .reset_index()
    )
    segB = (
        acct_summary[acct_summary["frequency_segment"].isin(["Infrequent", "Frequent"])]
        .groupby("frequency_segment")
        .agg(
            traders=("Account", "nunique"),
            total_net_pnl_mean=("total_net_pnl", "mean"),
            win_rate_mean=("win_rate_mean", "mean"),
            pnl_std_mean=("pnl_std", "mean"),
            max_dd_mean=("max_drawdown_proxy", "mean"),
            avg_trades_per_day=("avg_trades_per_day", "mean"),
            median_max_pos=("median_max_pos", "median"),
        )
        .reset_index()
    )
    segC = (
        acct_summary.groupby("consistency_segment")
        .agg(
            traders=("Account", "nunique"),
            total_net_pnl_mean=("total_net_pnl", "mean"),
            win_rate_mean=("win_rate_mean", "mean"),
            pnl_std_mean=("pnl_std", "mean"),
            max_dd_mean=("max_drawdown_proxy", "mean"),
        )
        .reset_index()
        .sort_values("traders", ascending=False)
    )

    segA.to_csv("reports/table_segment_pos_size.csv", index=False)
    segB.to_csv("reports/table_segment_frequency.csv", index=False)
    segC.to_csv("reports/table_segment_consistency.csv", index=False)

    # Charts
    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(8, 4))
    sns.boxplot(data=fg_daily, x="regime", y="pnl_per_trader", order=["Fear", "Greed"])
    plt.axhline(0, color="black", linewidth=1)
    plt.title("PnL per trader (daily) by sentiment regime")
    plt.tight_layout()
    plt.savefig("reports/chart1_pnl_per_trader_box.png", dpi=200)
    plt.close()

    plt.figure(figsize=(8, 4))
    sns.boxplot(data=fg_daily, x="regime", y="win_rate", order=["Fear", "Greed"])
    plt.title("Win rate (daily) by sentiment regime")
    plt.tight_layout()
    plt.savefig("reports/chart1b_winrate_box.png", dpi=200)
    plt.close()

    plot_df = (
        fg_daily.groupby("regime")
        .agg(
            trades=("trades", "mean"),
            avg_trade_size=("avg_trade_size_usd", "mean"),
            buy_share=("buy_volume_share", "mean"),
            p95_pos=("p95_max_start_pos_notional_usd", "mean"),
        )
        .reindex(["Fear", "Greed"])
        .reset_index()
    )
    fig, axes = plt.subplots(1, 4, figsize=(14, 3.6))
    for ax, col, title in zip(
        axes,
        ["trades", "avg_trade_size", "buy_share", "p95_pos"],
        ["Trades/day", "Avg trade size (USD)", "Buy volume share", "P95 max pos notional (USD)"],
    ):
        sns.barplot(data=plot_df, x="regime", y=col, ax=ax, order=["Fear", "Greed"])
        ax.set_title(title)
        ax.set_xlabel("")
    plt.suptitle("Behavior differences (daily averages) Fear vs Greed", y=1.05)
    plt.tight_layout()
    plt.savefig("reports/chart2_behavior_bars.png", dpi=200, bbox_inches="tight")
    plt.close()

    seg_df = fg_acct.merge(
        acct_summary[["Account", "frequency_segment"]], on="Account", how="left"
    )
    seg_df = seg_df[seg_df["frequency_segment"].isin(["Frequent", "Infrequent"])]

    plt.figure(figsize=(9, 4))
    sns.boxplot(
        data=seg_df,
        x="frequency_segment",
        y="total_net_pnl_usd",
        hue="regime",
        order=["Infrequent", "Frequent"],
        hue_order=["Fear", "Greed"],
    )
    plt.axhline(0, color="black", linewidth=1)
    plt.title("Account-day net PnL by sentiment and trader frequency segment")
    plt.tight_layout()
    plt.savefig("reports/chart3_segment_frequency_pnl.png", dpi=200)
    plt.close()

    # ----------------------------
    # Advanced, nicer visuals
    # ----------------------------
    palette = {"Fear": "#2563EB", "Greed": "#F97316", "Neutral": "#64748B"}

    def _money(x, _pos=None):
        try:
            x = float(x)
        except Exception:
            return str(x)
        ax = abs(x)
        if ax >= 1_000_000_000:
            return f"{x/1_000_000_000:.1f}B"
        if ax >= 1_000_000:
            return f"{x/1_000_000:.1f}M"
        if ax >= 1_000:
            return f"{x/1_000:.1f}k"
        return f"{x:.0f}"

    money_fmt = FuncFormatter(_money)

    # Style tuned for "report" look
    sns.set_theme(
        context="talk",
        style="white",
        font="DejaVu Sans",
        rc={
            "axes.titleweight": "bold",
            "axes.labelcolor": "#0f172a",
            "text.color": "#0f172a",
            "axes.edgecolor": "#cbd5e1",
            "grid.color": "#e2e8f0",
            "axes.facecolor": "white",
            "figure.facecolor": "white",
        },
    )

    # Chart 4: Time-series (sentiment + performance) with regime shading
    ts = aligned_daily.sort_values("date").copy()
    ts["pnl_per_trader_14d"] = ts["pnl_per_trader"].rolling(14, min_periods=3).mean()
    ts["sentiment_14d"] = ts["value"].rolling(14, min_periods=3).mean()

    fig, ax1 = plt.subplots(figsize=(13, 5))
    ax2 = ax1.twinx()

    # Regime shading
    ts["regime_full"] = ts["regime"].fillna("Neutral")
    ts["regime_block"] = (ts["regime_full"] != ts["regime_full"].shift()).cumsum()
    blocks = ts.groupby("regime_block").agg(
        start=("date", "min"), end=("date", "max"), regime=("regime_full", "first")
    )
    for _, r in blocks.iterrows():
        ax1.axvspan(
            r["start"],
            r["end"],
            color=palette.get(r["regime"], "#94a3b8"),
            alpha=0.06,
            linewidth=0,
        )

    ax1.plot(ts["date"], ts["sentiment_14d"], color="#111827", linewidth=2.2, label="Fear/Greed (14D avg)")
    ax1.scatter(ts["date"], ts["value"], color="#111827", s=10, alpha=0.15, linewidth=0)
    ax1.set_ylabel("Fear & Greed index (0–100)")
    ax1.set_ylim(0, 100)

    ax2.plot(
        ts["date"],
        ts["pnl_per_trader_14d"],
        color="#10B981",
        linewidth=2.2,
        label="PnL per trader (14D avg)",
    )
    ax2.scatter(ts["date"], ts["pnl_per_trader"], color="#10B981", s=10, alpha=0.12, linewidth=0)
    ax2.set_ylabel("PnL per trader (USD)")
    ax2.yaxis.set_major_formatter(money_fmt)

    ax1.set_title("Sentiment vs performance over time (with Fear/Greed regime shading)")
    ax1.grid(True, axis="y")
    ax1.grid(False, axis="x")
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(handles1 + handles2, labels1 + labels2, loc="upper left", frameon=True)
    plt.tight_layout()
    plt.savefig("reports/chart4_timeseries_sentiment_vs_pnl.png", dpi=220)
    plt.close()

    # Chart 5: Violin+box of account-day net PnL by regime (clipped for readability)
    fg_acct_plot = fg_acct.copy()
    lo, hi = fg_acct_plot["total_net_pnl_usd"].quantile([0.01, 0.99])
    fg_acct_plot["net_pnl_clip"] = fg_acct_plot["total_net_pnl_usd"].clip(lo, hi)

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.violinplot(
        data=fg_acct_plot,
        x="regime",
        y="net_pnl_clip",
        order=["Fear", "Greed"],
        hue="regime",
        palette=palette,
        legend=False,
        inner=None,
        cut=0,
        linewidth=0,
        ax=ax,
    )
    sns.boxplot(
        data=fg_acct_plot,
        x="regime",
        y="net_pnl_clip",
        order=["Fear", "Greed"],
        width=0.18,
        showfliers=False,
        boxprops={"facecolor": "white", "edgecolor": "#0f172a", "alpha": 0.9},
        whiskerprops={"color": "#0f172a"},
        medianprops={"color": "#0f172a", "linewidth": 2},
        ax=ax,
    )
    ax.axhline(0, color="#0f172a", linewidth=1)
    ax.set_title("Distribution of account-day net PnL (clipped to 1–99th pct) by regime")
    ax.set_xlabel("")
    ax.set_ylabel("Net PnL (USD, clipped)")
    ax.yaxis.set_major_formatter(money_fmt)
    sns.despine(ax=ax, left=False, bottom=False)
    plt.tight_layout()
    plt.savefig("reports/chart5_violin_net_pnl_acctday.png", dpi=220)
    plt.close()

    # Chart 6: Drawdown proxy distribution (KDE, clipped) by regime
    dd = fg_acct.copy()
    dd_lo, dd_hi = dd["drawdown_proxy"].quantile([0.01, 0.99])
    dd["drawdown_clip"] = dd["drawdown_proxy"].clip(dd_lo, dd_hi)

    fig, ax = plt.subplots(figsize=(11, 5))
    for reg in ["Fear", "Greed"]:
        sub = dd[dd["regime"] == reg]
        sns.kdeplot(
            data=sub,
            x="drawdown_clip",
            fill=True,
            common_norm=False,
            alpha=0.25,
            linewidth=2.0,
            color=palette[reg],
            label=reg,
            ax=ax,
        )
    ax.set_title("Drawdown proxy distribution by regime (clipped to 1–99th pct)")
    ax.set_xlabel("Drawdown proxy (USD, <= 0; more negative = worse)")
    ax.set_ylabel("Density")
    ax.xaxis.set_major_formatter(money_fmt)
    ax.legend(frameon=True)
    sns.despine(ax=ax)
    plt.tight_layout()
    plt.savefig("reports/chart6_drawdown_kde.png", dpi=220)
    plt.close()

    # Chart 7: Sentiment buckets (deciles) vs PnL per trader with 95% CI
    bucket_df = aligned_daily.dropna(subset=["value", "pnl_per_trader"]).copy()
    # Robust to small sample sizes by dropping duplicate bins if needed
    bucket_df["sentiment_decile"] = pd.qcut(bucket_df["value"], 10, duplicates="drop")
    # Pretty labels
    bucket_df["sentiment_decile_label"] = bucket_df["sentiment_decile"].astype(str)

    fig, ax = plt.subplots(figsize=(13, 5))
    sns.pointplot(
        data=bucket_df,
        x="sentiment_decile_label",
        y="pnl_per_trader",
        errorbar=("ci", 95),
        color="#111827",
        markers="o",
        linestyles="-",
        ax=ax,
    )
    ax.axhline(0, color="#0f172a", linewidth=1, alpha=0.8)
    ax.set_title("Performance vs sentiment (Fear/Greed deciles) — mean PnL per trader with 95% CI")
    ax.set_xlabel("Fear & Greed decile (bin range)")
    ax.set_ylabel("PnL per trader (USD)")
    ax.yaxis.set_major_formatter(money_fmt)
    ax.tick_params(axis="x", rotation=25)
    sns.despine(ax=ax)
    plt.tight_layout()
    plt.savefig("reports/chart7_sentiment_deciles_pnl_ci.png", dpi=220)
    plt.close()

    # Chart 8: Correlation heatmap (Spearman) for key daily metrics + sentiment value
    corr_cols = [
        "value",
        "pnl_per_trader",
        "win_rate",
        "trades",
        "fills",
        "total_volume_usd",
        "buy_volume_share",
        "net_flow_usd",
        "p95_max_start_pos_notional_usd",
        "active_traders",
        "avg_trade_size_usd",
    ]
    corr_df = aligned_daily.dropna(subset=["value"]).copy()
    corr_df = corr_df[[c for c in corr_cols if c in corr_df.columns]].dropna(how="all")
    corr = corr_df.corr(method="spearman")

    # mask upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(
        corr,
        mask=mask,
        cmap=sns.diverging_palette(220, 20, as_cmap=True),
        vmin=-1,
        vmax=1,
        center=0,
        square=True,
        linewidths=0.6,
        cbar_kws={"shrink": 0.8, "label": "Spearman ρ"},
        ax=ax,
    )
    ax.set_title("Spearman correlation heatmap (daily metrics + sentiment)")
    plt.tight_layout()
    plt.savefig("reports/chart8_corr_heatmap.png", dpi=220)
    plt.close()

    # Chart 9: Sentiment vs PnL per trader (hexbin + trend)
    scatter_df = aligned_daily.dropna(subset=["value", "pnl_per_trader"]).copy()
    fig, ax = plt.subplots(figsize=(11, 5))
    hb = ax.hexbin(
        scatter_df["value"],
        scatter_df["pnl_per_trader"],
        gridsize=32,
        cmap="viridis",
        mincnt=1,
        linewidths=0,
        alpha=0.95,
    )
    cb = fig.colorbar(hb, ax=ax)
    cb.set_label("Days per hex")
    sns.regplot(
        data=scatter_df,
        x="value",
        y="pnl_per_trader",
        scatter=False,
        lowess=True,
        line_kws={"color": "white", "linewidth": 2.5},
        ax=ax,
    )
    ax.axhline(0, color="white", linewidth=1, alpha=0.9)
    ax.set_title("Sentiment vs PnL per trader (daily) — density + LOWESS trend")
    ax.set_xlabel("Fear & Greed index (0–100)")
    ax.set_ylabel("PnL per trader (USD)")
    ax.yaxis.set_major_formatter(money_fmt)
    plt.tight_layout()
    plt.savefig("reports/chart9_sentiment_vs_pnl_hexbin.png", dpi=220)
    plt.close()

    print("Wrote reports/*.png and reports/*.csv")


if __name__ == "__main__":
    main()

