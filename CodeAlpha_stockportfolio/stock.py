import tkinter as tk
from tkinter import scrolledtext
import csv
from datetime import datetime
import os
import sys

if os.name != "nt" and os.environ.get("DISPLAY", "") == "":
    print("No graphical display found. Run this on a desktop system.")
    sys.exit()

try:
    import ttkbootstrap as ttb
    from ttkbootstrap.constants import *
    from ttkbootstrap.dialogs import Messagebox
except ImportError:
    print(
        "This redesigned UI needs the 'ttkbootstrap' package.\n\n"
        "Install it with:\n  pip install ttkbootstrap\n\n"
        "then run this script again."
    )
    sys.exit()

try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

# ─────────────────────────────────────────────
# Data
# ─────────────────────────────────────────────

STOCK_PRICES = {
    "AAPL": 180.50, "TSLA": 250.75, "GOOGL": 140.25, "MSFT": 378.90,
    "AMZN": 175.30, "NVDA": 460.15, "META": 350.60, "NFLX": 485.20,
    "ORCL": 125.40, "AMD": 115.80,
}

PURCHASE_PRICES = {
    "AAPL": 152.30, "TSLA": 210.40, "GOOGL": 118.75, "MSFT": 310.50,
    "AMZN": 142.60, "NVDA": 280.90, "META": 290.15, "NFLX": 410.30,
    "ORCL": 108.20, "AMD": 89.45,
}

portfolio = {}

# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def money(value):
    return f"₹{value:,.2f}"

def shade(hex_color, amount):
    """Lighten (amount > 0) or darken (amount < 0) a hex color."""
    hex_color = hex_color.lstrip("#")
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    r = max(0, min(255, int(r + 255 * amount)))
    g = max(0, min(255, int(g + 255 * amount)))
    b = max(0, min(255, int(b + 255 * amount)))
    return f"#{r:02x}{g:02x}{b:02x}"

def show_error(title, msg):
    Messagebox.show_error(msg, title)

def show_info(title, msg):
    Messagebox.show_info(msg, title)

def show_warning(title, msg):
    Messagebox.show_warning(msg, title)

def ask_yes_no(title, msg):
    return Messagebox.yesno(msg, title) == "Yes"

# ─────────────────────────────────────────────
# Symbol selection / price preview
# ─────────────────────────────────────────────

def on_symbol_changed(*_):
    symbol = stock_var.get().upper().strip()
    current = STOCK_PRICES.get(symbol)
    purchase = PURCHASE_PRICES.get(symbol)

    if current:
        buy_price_val.config(text=money(purchase), bootstyle="success")
        market_price_val.config(text=money(current), bootstyle="info")
    else:
        buy_price_val.config(text="—", bootstyle="secondary")
        market_price_val.config(text="—", bootstyle="secondary")

# ─────────────────────────────────────────────
# Details panel
# ─────────────────────────────────────────────

def update_details(stock=None):
    details_text.config(state="normal")
    details_text.delete("1.0", tk.END)

    if not portfolio:
        details_text.insert(tk.END, "Portfolio is empty.\nAdd a stock above to see its details here.")
    elif stock is None:
        details_text.insert(tk.END, "Select a stock from the table to view full details.")
    else:
        data = portfolio.get(stock)
        if not data:
            details_text.insert(tk.END, "No details available.")
        else:
            arrow = "▲" if data["profit_loss"] >= 0 else "▼"
            details_text.insert(tk.END, f"  Stock Symbol          {stock}\n")
            details_text.insert(tk.END, f"  Quantity              {data['quantity']:.2f}\n")
            details_text.insert(tk.END, f"  Avg Purchase Price    {money(data['purchase_price'])}\n")
            details_text.insert(tk.END, f"  Current Market Price  {money(data['current_price'])}\n")
            details_text.insert(tk.END, f"  Total Invested        {money(data['total_invested'])}\n")
            details_text.insert(tk.END, f"  Current Value         {money(data['current_value'])}\n")
            details_text.insert(tk.END, f"  Profit / Loss         {arrow} {money(abs(data['profit_loss']))}\n")
            details_text.insert(tk.END, f"  Profit / Loss %       {data['profit_loss_pct']:+.2f}%\n")
            details_text.insert(tk.END, f"  Updated On            {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    details_text.config(state="disabled")

# ─────────────────────────────────────────────
# Table
# ─────────────────────────────────────────────

def refresh_table():
    for row in tree.get_children():
        tree.delete(row)

    total_invested = 0
    total_current = 0

    for stock, data in portfolio.items():
        current_price = STOCK_PRICES[stock]
        current_value = data["quantity"] * current_price
        profit_loss = current_value - data["total_invested"]
        profit_loss_pct = (profit_loss / data["total_invested"]) * 100 if data["total_invested"] > 0 else 0

        data["current_price"] = current_price
        data["current_value"] = current_value
        data["profit_loss"] = profit_loss
        data["profit_loss_pct"] = profit_loss_pct

        total_invested += data["total_invested"]
        total_current += current_value

    for i, (stock, data) in enumerate(
        sorted(portfolio.items(), key=lambda item: item[1]["current_value"], reverse=True)
    ):
        allocation = (data["current_value"] / total_current) * 100 if total_current > 0 else 0
        pl_val = data["profit_loss"]
        row_tag = "evenrow" if i % 2 == 0 else "oddrow"
        pl_tag = "gain" if pl_val >= 0 else "loss"
        tree.insert("", "end", values=(
            stock,
            f"{data['quantity']:.2f}",
            money(data["purchase_price"]),
            money(data["current_price"]),
            money(data["total_invested"]),
            money(data["current_value"]),
            f"{'+' if pl_val >= 0 else ''}{money(pl_val)}",
            f"{data['profit_loss_pct']:+.2f}%",
            f"{allocation:.2f}%",
        ), tags=(row_tag, pl_tag))

    invested_val.config(text=money(total_invested))
    current_val.config(text=money(total_current))

    net_pl = total_current - total_invested
    pl_card.config(bg=colors.success if net_pl >= 0 else colors.danger)
    pl_val_label.config(
        text=f"{'+' if net_pl >= 0 else ''}{money(net_pl)}",
        bootstyle="inverse-success" if net_pl >= 0 else "inverse-danger",
    )

    if portfolio:
        first_stock = next(iter(sorted(portfolio.keys())))
        update_details(first_stock)
    else:
        update_details()

    update_statistics()

# ─────────────────────────────────────────────
# Validation
# ─────────────────────────────────────────────

def get_positive_float(value_text, field_name):
    try:
        value = float(value_text)
        if value <= 0:
            raise ValueError
        return value
    except ValueError:
        raise ValueError(f"Please enter a valid positive number for {field_name}.")

# ─────────────────────────────────────────────
# Portfolio actions
# ─────────────────────────────────────────────

def add_stock():
    stock = stock_var.get().upper().strip()
    qty_text = quantity_var.get().strip()

    if not stock:
        show_error("Error", "Stock symbol cannot be empty.")
        return

    if stock not in STOCK_PRICES:
        show_error("Error", f"{stock} is not available in the stock list.")
        return

    try:
        quantity = get_positive_float(qty_text, "quantity")
    except ValueError as e:
        show_error("Input Error", str(e))
        return

    purchase_price = PURCHASE_PRICES[stock]

    if stock in portfolio:
        old_qty = portfolio[stock]["quantity"]
        old_invested = portfolio[stock]["total_invested"]
        new_invested = quantity * purchase_price
        total_qty = old_qty + quantity
        portfolio[stock]["quantity"] = total_qty
        portfolio[stock]["total_invested"] = old_invested + new_invested
        portfolio[stock]["purchase_price"] = portfolio[stock]["total_invested"] / total_qty
    else:
        portfolio[stock] = {
            "quantity": quantity,
            "purchase_price": purchase_price,
            "total_invested": quantity * purchase_price,
        }

    stock_var.set("")
    quantity_var.set("")
    buy_price_val.config(text="—", bootstyle="secondary")
    market_price_val.config(text="—", bootstyle="secondary")

    refresh_table()
    show_info("Success", f"{stock} added!\n\nBought at:     {money(purchase_price)}\nMarket Price:  {money(STOCK_PRICES[stock])}\nQty:           {quantity:.2f}")

def remove_stock():
    stock = stock_var.get().upper().strip()
    if not stock:
        show_error("Error", "Enter or select a stock symbol to remove.")
        return

    if stock in portfolio:
        del portfolio[stock]
        refresh_table()
        show_info("Removed", f"{stock} removed successfully.")
    else:
        show_error("Error", "Stock not found in portfolio.")

def clear_portfolio():
    if not portfolio:
        show_warning("Warning", "Portfolio is already empty.")
        return

    if ask_yes_no("Confirm", "Do you want to clear the entire portfolio?"):
        portfolio.clear()
        refresh_table()
        show_info("Cleared", "Portfolio cleared successfully.")

def save_portfolio():
    if not portfolio:
        show_warning("Warning", "Portfolio is empty. Nothing to save.")
        return

    try:
        with open("portfolio.csv", "w", newline="") as file:
            fieldnames = [
                "stock", "quantity", "purchase_price", "current_price",
                "total_invested", "current_value", "profit_loss", "profit_loss_pct",
            ]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for stock, data in portfolio.items():
                writer.writerow({
                    "stock": stock,
                    "quantity": data["quantity"],
                    "purchase_price": data["purchase_price"],
                    "current_price": data["current_price"],
                    "total_invested": data["total_invested"],
                    "current_value": data["current_value"],
                    "profit_loss": data["profit_loss"],
                    "profit_loss_pct": data["profit_loss_pct"],
                })
        show_info("Saved", "Portfolio saved to portfolio.csv successfully.")
    except Exception as e:
        show_error("Save Error", f"Could not save file.\n{e}")

def load_portfolio():
    try:
        with open("portfolio.csv", "r", newline="") as file:
            reader = csv.DictReader(file)
            loaded = {}
            for row in reader:
                stock = row.get("stock", "").strip().upper()
                if stock not in STOCK_PRICES:
                    continue
                loaded[stock] = {
                    "quantity": float(row["quantity"]),
                    "purchase_price": float(row["purchase_price"]),
                    "total_invested": float(row["total_invested"]),
                    "current_price": float(row["current_price"]),
                    "current_value": float(row["current_value"]),
                    "profit_loss": float(row["profit_loss"]),
                    "profit_loss_pct": float(row["profit_loss_pct"]),
                }

        portfolio.clear()
        portfolio.update(loaded)
        refresh_table()
        show_info("Loaded", "Portfolio loaded successfully.")
    except FileNotFoundError:
        show_error("Error", "portfolio.csv not found.")
    except Exception as e:
        show_error("Load Error", f"Could not load file.\n{e}")

def show_available_stocks():
    win = ttb.Toplevel(title="Available Stocks")
    win.geometry("520x460")

    ttb.Label(win, text="Available Stocks", font=("Segoe UI", 15, "bold")).pack(pady=(14, 2))
    ttb.Label(win, text="Buy price vs. current market price", bootstyle="secondary").pack(pady=(0, 10))

    cols = ("Symbol", "Buy Price", "Market Price", "Change %")
    price_tree = ttb.Treeview(win, columns=cols, show="headings", height=10, bootstyle="info")
    for c in cols:
        price_tree.heading(c, text=c)
        price_tree.column(c, anchor="center", width=110)
    price_tree.tag_configure("gain", foreground=colors.success)
    price_tree.tag_configure("loss", foreground=colors.danger)

    for stock in sorted(STOCK_PRICES):
        buy = PURCHASE_PRICES[stock]
        mkt = STOCK_PRICES[stock]
        change = (mkt - buy) / buy * 100
        price_tree.insert("", "end", values=(
            stock, money(buy), money(mkt), f"{change:+.2f}%"
        ), tags=("gain" if change >= 0 else "loss",))

    price_tree.pack(fill="both", expand=True, padx=16, pady=8)
    ttb.Button(win, text="Close", command=win.destroy, bootstyle="secondary", width=12).pack(pady=12)

def on_tree_select(event):
    selected = tree.focus()
    if not selected:
        return
    values = tree.item(selected, "values")
    if not values:
        return
    stock = values[0]
    stock_var.set(stock)
    update_details(stock)

# ─────────────────────────────────────────────
# Statistics dashboard
# ─────────────────────────────────────────────

def get_stats():
    if not portfolio:
        return None

    total_invested = sum(d["total_invested"] for d in portfolio.values())
    total_current = sum(d.get("current_value", d["quantity"] * STOCK_PRICES[s]) for s, d in portfolio.items())
    portfolio_return_pct = ((total_current - total_invested) / total_invested * 100) if total_invested > 0 else 0

    best_stock = max(portfolio.items(), key=lambda x: x[1].get("profit_loss_pct", 0))
    worst_stock = min(portfolio.items(), key=lambda x: x[1].get("profit_loss_pct", 0))

    return {
        "total_stocks": len(portfolio),
        "best_performer": best_stock[0],
        "best_pct": best_stock[1].get("profit_loss_pct", 0),
        "worst_performer": worst_stock[0],
        "worst_pct": worst_stock[1].get("profit_loss_pct", 0),
        "portfolio_return_pct": portfolio_return_pct,
        "total_invested": total_invested,
        "total_current": total_current,
    }

def update_statistics():
    stats = get_stats()
    if not stats:
        stat_stocks_val.config(text="0")
        stat_best_val.config(text="—")
        stat_worst_val.config(text="—")
        stat_return_val.config(text="0.00%")
        return_card.config(bg=colors.primary)
        stat_return_val.config(bootstyle="inverse-primary")
        return

    stat_stocks_val.config(text=str(stats["total_stocks"]))
    stat_best_val.config(text=f"{stats['best_performer']}  {stats['best_pct']:+.2f}%")
    stat_worst_val.config(text=f"{stats['worst_performer']}  {stats['worst_pct']:+.2f}%")

    ret = stats["portfolio_return_pct"]
    stat_return_val.config(text=f"{ret:+.2f}%")
    if ret >= 0:
        return_card.config(bg=colors.success)
        stat_return_val.config(bootstyle="inverse-success")
        return_icon.config(bg=colors.success, bootstyle="inverse-success")
    else:
        return_card.config(bg=colors.danger)
        stat_return_val.config(bootstyle="inverse-danger")
        return_icon.config(bg=colors.danger, bootstyle="inverse-danger")

# ─────────────────────────────────────────────
# TXT export report
# ─────────────────────────────────────────────

def export_txt_report():
    if not portfolio:
        show_warning("Warning", "Portfolio is empty. Nothing to export.")
        return

    stats = get_stats()
    filename = f"portfolio_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write("=" * 60 + "\n")
            f.write("         STOCK PORTFOLIO REPORT\n")
            f.write(f"         Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")

            f.write("PORTFOLIO STATISTICS\n")
            f.write("-" * 40 + "\n")
            f.write(f"  Total Stocks       : {stats['total_stocks']}\n")
            f.write(f"  Best Performer     : {stats['best_performer']}  ({stats['best_pct']:+.2f}%)\n")
            f.write(f"  Worst Performer    : {stats['worst_performer']}  ({stats['worst_pct']:+.2f}%)\n")
            f.write(f"  Portfolio Return % : {stats['portfolio_return_pct']:+.2f}%\n")
            f.write(f"  Total Invested     : {money(stats['total_invested'])}\n")
            f.write(f"  Current Value      : {money(stats['total_current'])}\n")
            f.write(f"  Overall P/L        : {money(stats['total_current'] - stats['total_invested'])}\n")
            f.write("\n")

            f.write("INDIVIDUAL STOCK DETAILS\n")
            f.write("-" * 60 + "\n")
            header = f"{'Stock':<8} {'Qty':>8} {'Buy Price':>12} {'Mkt Price':>12} {'Invested':>14} {'Value':>14} {'P/L':>12} {'P/L%':>8} {'Alloc%':>8}\n"
            f.write(header)
            f.write("-" * 96 + "\n")

            total_current = stats["total_current"]
            for stock, data in sorted(portfolio.items(), key=lambda x: x[1].get("current_value", 0), reverse=True):
                allocation = (data.get("current_value", 0) / total_current * 100) if total_current > 0 else 0
                row = (
                    f"{stock:<8} "
                    f"{data['quantity']:>8.2f} "
                    f"{data['purchase_price']:>12.2f} "
                    f"{data.get('current_price', STOCK_PRICES[stock]):>12.2f} "
                    f"{data['total_invested']:>14.2f} "
                    f"{data.get('current_value', 0):>14.2f} "
                    f"{data.get('profit_loss', 0):>12.2f} "
                    f"{data.get('profit_loss_pct', 0):>7.2f}% "
                    f"{allocation:>7.2f}%\n"
                )
                f.write(row)

            f.write("-" * 96 + "\n\n")
            f.write("=" * 60 + "\n")
            f.write("             END OF REPORT\n")
            f.write("=" * 60 + "\n")

        show_info("Exported", f"Report saved as:\n{filename}")
    except Exception as e:
        show_error("Export Error", f"Could not export report.\n{e}")

# ─────────────────────────────────────────────
# Pie chart
# ─────────────────────────────────────────────

def show_pie_chart():
    if not portfolio:
        show_warning("Warning", "Portfolio is empty. Add stocks first.")
        return

    if not MATPLOTLIB_AVAILABLE:
        show_error(
            "Missing Library",
            "matplotlib is not installed.\n\nPlease run:\n  pip install matplotlib\n\nthen restart.",
        )
        return

    total_current = sum(d.get("current_value", d["quantity"] * STOCK_PRICES[s]) for s, d in portfolio.items())
    if total_current == 0:
        show_warning("Warning", "No value to chart.")
        return

    labels, sizes = [], []
    for stock, data in sorted(portfolio.items(), key=lambda x: x[1].get("current_value", 0), reverse=True):
        val = data.get("current_value", data["quantity"] * STOCK_PRICES[stock])
        labels.append(stock)
        sizes.append(val)

    chart_window = ttb.Toplevel(title="Portfolio Allocation")
    chart_window.geometry("700x580")

    ttb.Label(chart_window, text="Portfolio Allocation", font=("Segoe UI", 16, "bold")).pack(pady=(12, 0))
    ttb.Label(chart_window, text=f"Total Value: {money(total_current)}", bootstyle="secondary").pack(pady=(0, 6))

    palette = [colors.primary, colors.success, colors.info, colors.warning,
               colors.danger, colors.secondary, "#9b59b6", "#16a085", "#e67e22", "#2ecc71"]
    wedge_colors = [palette[i % len(palette)] for i in range(len(labels))]

    fig, ax = plt.subplots(figsize=(6.5, 5), facecolor=colors.bg)
    ax.set_facecolor(colors.bg)
    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, autopct="%1.1f%%", startangle=140,
        colors=wedge_colors, pctdistance=0.82,
        wedgeprops=dict(width=0.6, edgecolor=colors.bg, linewidth=2),
        textprops=dict(color=colors.fg),
    )
    for at in autotexts:
        at.set_fontsize(9)
        at.set_color(colors.bg)
        at.set_fontweight("bold")
    for t in texts:
        t.set_fontsize(10)
        t.set_color(colors.fg)

    canvas = FigureCanvasTkAgg(fig, master=chart_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=5)

    ttb.Button(chart_window, text="Close", command=chart_window.destroy, bootstyle="danger", width=12).pack(pady=10)

# ─────────────────────────────────────────────
# GUI Layout
# ─────────────────────────────────────────────

root = ttb.Window(title="Stock Portfolio Tracker", themename="darkly", size=(1300, 920))
style = root.style
colors = style.colors

MAIN_PAD = 22

# ── Header ────────────────────────────────────
header = ttb.Frame(root, padding=(MAIN_PAD, 18, MAIN_PAD, 6))
header.pack(fill="x")

ttb.Label(header, text="📈 Stock Portfolio Tracker", font=("Segoe UI", 22, "bold")).pack(side="left")
ttb.Label(header, text="Track your investments, profits and allocation in real time",
          bootstyle="secondary").pack(side="left", padx=(14, 0), pady=(8, 0))

ttb.Separator(root).pack(fill="x", padx=MAIN_PAD)

# ── Add to portfolio card ─────────────────────
add_card = ttb.Labelframe(root, text="  Add to Portfolio  ", padding=16, bootstyle="primary")
add_card.pack(fill="x", padx=MAIN_PAD, pady=14)

ttb.Label(add_card, text="Stock Symbol").grid(row=0, column=0, padx=(0, 8), pady=4, sticky="w")
stock_var = tk.StringVar()
stock_combo = ttb.Combobox(add_card, textvariable=stock_var, width=14,
                            values=sorted(STOCK_PRICES.keys()), bootstyle="primary")
stock_combo.grid(row=1, column=0, padx=(0, 20), sticky="w")
stock_var.trace_add("write", on_symbol_changed)
stock_combo.bind("<<ComboboxSelected>>", on_symbol_changed)

ttb.Label(add_card, text="Quantity").grid(row=0, column=1, padx=(0, 8), pady=4, sticky="w")
quantity_var = tk.StringVar()
quantity_entry = ttb.Entry(add_card, textvariable=quantity_var, width=14, bootstyle="primary")
quantity_entry.grid(row=1, column=1, padx=(0, 20), sticky="w")

ttb.Label(add_card, text="Buy Price").grid(row=0, column=2, padx=(0, 8), pady=4, sticky="w")
buy_price_val = ttb.Label(add_card, text="—", font=("Segoe UI", 11, "bold"), bootstyle="secondary")
buy_price_val.grid(row=1, column=2, padx=(0, 20), sticky="w")

ttb.Label(add_card, text="Market Price").grid(row=0, column=3, padx=(0, 8), pady=4, sticky="w")
market_price_val = ttb.Label(add_card, text="—", font=("Segoe UI", 11, "bold"), bootstyle="secondary")
market_price_val.grid(row=1, column=3, padx=(0, 24), sticky="w")

btn_row = ttb.Frame(add_card)
btn_row.grid(row=1, column=4, sticky="e")
add_card.grid_columnconfigure(5, weight=1)

ttb.Button(btn_row, text="➕ Add", command=add_stock, bootstyle="success", width=10).pack(side="left", padx=4)
ttb.Button(btn_row, text="➖ Remove", command=remove_stock, bootstyle="warning", width=10).pack(side="left", padx=4)

# ── Secondary toolbar ──────────────────────────
toolbar = ttb.Frame(root, padding=(MAIN_PAD, 0, MAIN_PAD, 6))
toolbar.pack(fill="x")

ttb.Button(toolbar, text="🗑 Clear Portfolio", command=clear_portfolio, bootstyle="danger-outline").pack(side="left", padx=4)
ttb.Button(toolbar, text="💾 Save", command=save_portfolio, bootstyle="info-outline").pack(side="left", padx=4)
ttb.Button(toolbar, text="📂 Load", command=load_portfolio, bootstyle="info-outline").pack(side="left", padx=4)
ttb.Button(toolbar, text="📋 Show Prices", command=show_available_stocks, bootstyle="secondary-outline").pack(side="left", padx=4)
ttb.Button(toolbar, text="📄 Export Report", command=export_txt_report, bootstyle="primary-outline").pack(side="left", padx=4)
ttb.Button(toolbar, text="🥧 Pie Chart", command=show_pie_chart, bootstyle="primary-outline").pack(side="left", padx=4)

# ── Statistics dashboard ───────────────────────
stats_section = ttb.Frame(root, padding=(MAIN_PAD, 6, MAIN_PAD, 6))
stats_section.pack(fill="x")

for i in range(4):
    stats_section.grid_columnconfigure(i, weight=1, uniform="card")

def make_stat_card(parent, col, icon, label, bg):
    card = tk.Frame(parent, bg=bg, bd=0)
    card.grid(row=0, column=col, padx=8, sticky="nsew")
    inner = tk.Frame(card, bg=bg)
    inner.pack(fill="both", expand=True, padx=16, pady=14)
    icon_lbl = ttb.Label(inner, text=icon, font=("Segoe UI", 18), bootstyle=f"inverse-{bg_name}" if False else None)
    icon_lbl.pack(anchor="w")
    value_lbl = ttb.Label(inner, text="0", font=("Segoe UI", 17, "bold"))
    value_lbl.pack(anchor="w", pady=(2, 0))
    text_lbl = ttb.Label(inner, text=label, font=("Segoe UI", 9))
    text_lbl.pack(anchor="w")
    return card, icon_lbl, value_lbl, text_lbl

stocks_card, stocks_icon, stat_stocks_val, _ = make_stat_card(stats_section, 0, "📦", "Total Stocks", colors.secondary)
stocks_icon.config(bootstyle="inverse-secondary")
stat_stocks_val.config(bootstyle="inverse-secondary")
stats_section.children[stocks_card.winfo_name()]  # keep ref alive (no-op)
for w in stocks_card.winfo_children()[0].winfo_children():
    if isinstance(w, ttb.Label) and w not in (stocks_icon, stat_stocks_val):
        w.config(bootstyle="inverse-secondary")

best_card, best_icon, stat_best_val, best_text = make_stat_card(stats_section, 1, "🏆", "Best Performer", colors.success)
best_icon.config(bootstyle="inverse-success")
stat_best_val.config(bootstyle="inverse-success")
best_text.config(bootstyle="inverse-success")

worst_card, worst_icon, stat_worst_val, worst_text = make_stat_card(stats_section, 2, "📉", "Worst Performer", colors.danger)
worst_icon.config(bootstyle="inverse-danger")
stat_worst_val.config(bootstyle="inverse-danger")
worst_text.config(bootstyle="inverse-danger")

return_card, return_icon, stat_return_val, return_text = make_stat_card(stats_section, 3, "📊", "Portfolio Return", colors.primary)
return_icon.config(bootstyle="inverse-primary")
stat_return_val.config(bootstyle="inverse-primary")
return_text.config(bootstyle="inverse-primary")

# ── Portfolio table ─────────────────────────────
table_card = ttb.Labelframe(root, text="  Holdings  ", padding=10, bootstyle="secondary")
table_card.pack(fill="both", expand=True, padx=MAIN_PAD, pady=10)

table_frame = ttb.Frame(table_card)
table_frame.pack(fill="both", expand=True)

columns = ("Stock", "Qty", "Avg Buy", "Current", "Invested", "Value", "P/L", "P/L %", "Alloc %")
tree = ttb.Treeview(table_frame, columns=columns, show="headings", height=11, bootstyle="primary")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=110, anchor="center")

tree.tag_configure("evenrow", background=colors.bg)
tree.tag_configure("oddrow", background=shade(colors.bg, 0.04))
tree.tag_configure("gain", foreground=colors.success)
tree.tag_configure("loss", foreground=colors.danger)

scrollbar = ttb.Scrollbar(table_frame, orient="vertical", command=tree.yview, bootstyle="round")
tree.configure(yscrollcommand=scrollbar.set)
tree.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

tree.bind("<<TreeviewSelect>>", on_tree_select)

# ── Summary footer ──────────────────────────────
summary_frame = ttb.Frame(root, padding=(MAIN_PAD, 0, MAIN_PAD, 14))
summary_frame.pack(fill="x")

def make_pill(parent, label, bg):
    card = tk.Frame(parent, bg=bg)
    card.pack(side="left", padx=8, fill="x", expand=True)
    inner = tk.Frame(card, bg=bg)
    inner.pack(padx=18, pady=10)
    ttb.Label(inner, text=label, font=("Segoe UI", 9), bootstyle="inverse-secondary" if bg == colors.secondary else None).pack(anchor="w")
    val = ttb.Label(inner, text=money(0), font=("Segoe UI", 14, "bold"))
    val.pack(anchor="w")
    return card, val

invested_card, invested_val = make_pill(summary_frame, "Total Invested", colors.dark)
current_card, current_val = make_pill(summary_frame, "Current Value", colors.dark)
pl_card, pl_val_label = make_pill(summary_frame, "Profit / Loss", colors.success)

for lbl in invested_card.winfo_children()[0].winfo_children():
    lbl.config(bootstyle="inverse-dark")
for lbl in current_card.winfo_children()[0].winfo_children():
    lbl.config(bootstyle="inverse-dark")
for lbl in pl_card.winfo_children()[0].winfo_children():
    lbl.config(bootstyle="inverse-success")

# ── Stock details panel ─────────────────────────
details_card = ttb.Labelframe(root, text="  Stock Details  ", padding=10, bootstyle="secondary")
details_card.pack(fill="both", expand=False, padx=MAIN_PAD, pady=(0, 18))

details_text = scrolledtext.ScrolledText(
    details_card, height=9, font=("Consolas", 11),
    bg=colors.bg, fg=colors.fg, insertbackground=colors.fg,
    relief="flat", borderwidth=0,
)
details_text.pack(fill="both", expand=True, padx=4, pady=4)
details_text.config(state="disabled")

update_details()
refresh_table()
root.mainloop()
