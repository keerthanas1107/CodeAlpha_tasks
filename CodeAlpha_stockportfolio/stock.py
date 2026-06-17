import tkinter as tk
from tkinter import ttk, messagebox
import csv
from datetime import datetime
import os
import sys

if os.name != "nt" and os.environ.get("DISPLAY", "") == "":
    print("No graphical display found. Run this on a desktop system.")
    sys.exit()

try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

# Current live market prices
STOCK_PRICES = {
    "AAPL": 180.50,
    "TSLA": 250.75,
    "GOOGL": 140.25,
    "MSFT": 378.90,
    "AMZN": 175.30,
    "NVDA": 460.15,
    "META": 350.60,
    "NFLX": 485.20,
    "ORCL": 125.40,
    "AMD":  115.80
}

# Simulated historical purchase prices (what you originally bought at)
PURCHASE_PRICES = {
    "AAPL": 152.30,
    "TSLA": 210.40,
    "GOOGL": 118.75,
    "MSFT": 310.50,
    "AMZN": 142.60,
    "NVDA": 280.90,
    "META": 290.15,
    "NFLX": 410.30,
    "ORCL": 108.20,
    "AMD":  89.45
}

portfolio = {}

def money(value):
    return f"₹{value:,.2f}"

def show_error(title, msg):
    messagebox.showerror(title, msg)

def show_info(title, msg):
    messagebox.showinfo(title, msg)

def show_warning(title, msg):
    messagebox.showwarning(title, msg)

def on_symbol_changed(*_):
    symbol  = stock_entry.get().upper().strip()
    current  = STOCK_PRICES.get(symbol)
    purchase = PURCHASE_PRICES.get(symbol)
    purchase_price_var.set(f"{purchase:.2f}" if purchase else "")
    price_display_label.config(
        text=f"Buy Price: {money(purchase)}  |  Market: {money(current)}" if current else "Market Price: —",
        fg="#27ae60" if current else "#888888"
    )

def update_details(stock=None):
    details_text.config(state="normal")
    details_text.delete("1.0", tk.END)

    if not portfolio:
        details_text.insert(tk.END, "Portfolio is empty.\nAdd a stock to see details here.")
    elif stock is None:
        details_text.insert(tk.END, "Select a stock from the table to view full details.")
    else:
        data = portfolio.get(stock)
        if not data:
            details_text.insert(tk.END, "No details available.")
        else:
            details_text.insert(tk.END, f"Stock Symbol:          {stock}\n")
            details_text.insert(tk.END, f"Quantity:              {data['quantity']:.2f}\n")
            details_text.insert(tk.END, f"Avg Purchase Price:    {money(data['purchase_price'])}\n")
            details_text.insert(tk.END, f"Current Market Price:  {money(data['current_price'])}\n")
            details_text.insert(tk.END, f"Total Invested:        {money(data['total_invested'])}\n")
            details_text.insert(tk.END, f"Current Value:         {money(data['current_value'])}\n")
            details_text.insert(tk.END, f"Profit/Loss:           {money(data['profit_loss'])}\n")
            details_text.insert(tk.END, f"Profit/Loss %:         {data['profit_loss_pct']:.2f}%\n")
            details_text.insert(tk.END, f"Updated On:            {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    details_text.config(state="disabled")

def refresh_table():
    for row in tree.get_children():
        tree.delete(row)

    total_invested = 0
    total_current  = 0

    for stock, data in portfolio.items():
        current_price   = STOCK_PRICES[stock]
        current_value   = data["quantity"] * current_price
        profit_loss     = current_value - data["total_invested"]
        profit_loss_pct = (profit_loss / data["total_invested"]) * 100 if data["total_invested"] > 0 else 0

        data["current_price"]   = current_price
        data["current_value"]   = current_value
        data["profit_loss"]     = profit_loss
        data["profit_loss_pct"] = profit_loss_pct

        total_invested += data["total_invested"]
        total_current  += current_value

    for stock, data in sorted(portfolio.items(), key=lambda item: item[1]["current_value"], reverse=True):
        allocation = (data["current_value"] / total_current) * 100 if total_current > 0 else 0
        pl_val = data["profit_loss"]
        tree.insert("", "end", values=(
            stock,
            f"{data['quantity']:.2f}",
            money(data["purchase_price"]),
            money(data["current_price"]),
            money(data["total_invested"]),
            money(data["current_value"]),
            money(pl_val),
            f"{data['profit_loss_pct']:.2f}%",
            f"{allocation:.2f}%"
        ))

    invested_label.config(text=f"Total Invested: {money(total_invested)}")
    current_label.config(text=f"Current Value:  {money(total_current)}")

    net_pl = total_current - total_invested
    profit_label.config(
        text=f"Profit/Loss: {money(net_pl)}",
        fg="#27ae60" if net_pl >= 0 else "#e74c3c"
    )

    if portfolio:
        first_stock = next(iter(sorted(portfolio.keys())))
        update_details(first_stock)
    else:
        update_details()

    update_statistics()

def get_positive_float(value_text, field_name):
    try:
        value = float(value_text)
        if value <= 0:
            raise ValueError
        return value
    except ValueError:
        raise ValueError(f"Please enter a valid positive number for {field_name}.")

def add_stock():
    stock    = stock_entry.get().upper().strip()
    qty_text = quantity_entry.get().strip()

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

    # Purchase price comes from historical PURCHASE_PRICES
    purchase_price = PURCHASE_PRICES[stock]

    if stock in portfolio:
        old_qty      = portfolio[stock]["quantity"]
        old_invested = portfolio[stock]["total_invested"]
        new_invested = quantity * purchase_price
        total_qty    = old_qty + quantity
        portfolio[stock]["quantity"]       = total_qty
        portfolio[stock]["total_invested"] = old_invested + new_invested
        portfolio[stock]["purchase_price"] = portfolio[stock]["total_invested"] / total_qty
    else:
        portfolio[stock] = {
            "quantity":       quantity,
            "purchase_price": purchase_price,
            "total_invested": quantity * purchase_price
        }

    stock_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)
    purchase_price_var.set("")
    price_display_label.config(text="Market Price: —", fg="#888888")

    refresh_table()
    show_info("Success", f"{stock} added!\n\nBought at:     {money(purchase_price)}\nMarket Price:  {money(STOCK_PRICES[stock])}\nQty:           {quantity:.2f}")

def remove_stock():
    stock = stock_entry.get().upper().strip()
    if not stock:
        show_error("Error", "Enter a stock symbol to remove.")
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

    if messagebox.askyesno("Confirm", "Do you want to clear the entire portfolio?"):
        portfolio.clear()
        refresh_table()
        update_details()
        update_statistics()
        show_info("Cleared", "Portfolio cleared successfully.")

def save_portfolio():
    if not portfolio:
        show_warning("Warning", "Portfolio is empty. Nothing to save.")
        return

    try:
        with open("portfolio.csv", "w", newline="") as file:
            fieldnames = [
                "stock", "quantity", "purchase_price", "current_price",
                "total_invested", "current_value", "profit_loss", "profit_loss_pct"
            ]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for stock, data in portfolio.items():
                writer.writerow({
                    "stock":           stock,
                    "quantity":        data["quantity"],
                    "purchase_price":  data["purchase_price"],
                    "current_price":   data["current_price"],
                    "total_invested":  data["total_invested"],
                    "current_value":   data["current_value"],
                    "profit_loss":     data["profit_loss"],
                    "profit_loss_pct": data["profit_loss_pct"]
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
                    "quantity":        float(row["quantity"]),
                    "purchase_price":  float(row["purchase_price"]),
                    "total_invested":  float(row["total_invested"]),
                    "current_price":   float(row["current_price"]),
                    "current_value":   float(row["current_value"]),
                    "profit_loss":     float(row["profit_loss"]),
                    "profit_loss_pct": float(row["profit_loss_pct"])
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
    info = "Available Stocks\n"
    info += "─" * 38 + "\n"
    info += f"{'Symbol':<8}  {'Buy Price':>12}  {'Market Price':>12}\n"
    info += "─" * 38 + "\n"
    for stock in STOCK_PRICES:
        info += f"{stock:<8}  {money(PURCHASE_PRICES[stock]):>12}  {money(STOCK_PRICES[stock]):>12}\n"
    messagebox.showinfo("Stock Prices", info)

def on_tree_select(event):
    selected = tree.focus()
    if not selected:
        return
    values = tree.item(selected, "values")
    if not values:
        return
    stock = values[0]
    update_details(stock)

# ─────────────────────────────────────────────
# FEATURE 1: Statistics Dashboard
# ─────────────────────────────────────────────

def get_stats():
    if not portfolio:
        return None

    total_invested = sum(d["total_invested"] for d in portfolio.values())
    total_current  = sum(d.get("current_value", d["quantity"] * STOCK_PRICES[s]) for s, d in portfolio.items())
    portfolio_return_pct = ((total_current - total_invested) / total_invested * 100) if total_invested > 0 else 0

    best_stock  = max(portfolio.items(), key=lambda x: x[1].get("profit_loss_pct", 0))
    worst_stock = min(portfolio.items(), key=lambda x: x[1].get("profit_loss_pct", 0))

    return {
        "total_stocks":         len(portfolio),
        "best_performer":       best_stock[0],
        "best_pct":             best_stock[1].get("profit_loss_pct", 0),
        "worst_performer":      worst_stock[0],
        "worst_pct":            worst_stock[1].get("profit_loss_pct", 0),
        "portfolio_return_pct": portfolio_return_pct,
        "total_invested":       total_invested,
        "total_current":        total_current,
    }

def update_statistics():
    stats = get_stats()
    if not stats:
        stat_stocks_val.config(text="0")
        stat_best_val.config(text="—")
        stat_worst_val.config(text="—")
        stat_return_val.config(text="0.00%")
        return

    stat_stocks_val.config(text=str(stats["total_stocks"]))
    stat_best_val.config(
        text=f"{stats['best_performer']}  ({stats['best_pct']:+.2f}%)",
        fg="#27ae60"
    )
    stat_worst_val.config(
        text=f"{stats['worst_performer']}  ({stats['worst_pct']:+.2f}%)",
        fg="#e74c3c"
    )
    ret = stats["portfolio_return_pct"]
    stat_return_val.config(
        text=f"{ret:+.2f}%",
        fg="#27ae60" if ret >= 0 else "#e74c3c"
    )

# ─────────────────────────────────────────────
# FEATURE 2: TXT Export Report
# ─────────────────────────────────────────────

def export_txt_report():
    if not portfolio:
        show_warning("Warning", "Portfolio is empty. Nothing to export.")
        return

    stats    = get_stats()
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
# FEATURE 3: Pie Chart
# ─────────────────────────────────────────────

def show_pie_chart():
    if not portfolio:
        show_warning("Warning", "Portfolio is empty. Add stocks first.")
        return

    if not MATPLOTLIB_AVAILABLE:
        show_error(
            "Missing Library",
            "matplotlib is not installed.\n\nPlease run:\n  pip install matplotlib\n\nthen restart."
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

    chart_window = tk.Toplevel(root)
    chart_window.title("Portfolio Allocation – Pie Chart")
    chart_window.geometry("700x560")
    chart_window.config(bg="#f4f4f4")

    tk.Label(chart_window, text="Portfolio Allocation",
             font=("Arial", 16, "bold"), bg="#f4f4f4").pack(pady=(10, 0))

    fig, ax = plt.subplots(figsize=(6.5, 5), facecolor="#f4f4f4")
    colors = plt.cm.Set3.colors[:len(labels)]  # type: ignore
    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, autopct="%1.1f%%", startangle=140,
        colors=colors, pctdistance=0.82,
        wedgeprops=dict(width=0.6, edgecolor="white", linewidth=1.5)
    )
    for at in autotexts:
        at.set_fontsize(9)
    for t in texts:
        t.set_fontsize(10)

    ax.set_title(f"Total Value: {money(total_current)}", fontsize=11, pad=12, color="#333333")

    canvas = FigureCanvasTkAgg(fig, master=chart_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=5)

    tk.Button(chart_window, text="Close", command=chart_window.destroy,
              bg="#e74c3c", fg="white", width=10).pack(pady=8)

# ─────────────────────────────────────────────
# GUI Layout
# ─────────────────────────────────────────────

root = tk.Tk()
root.title("Stock Portfolio Tracker")
root.geometry("1200x900")
root.config(bg="#f4f4f4")

tk.Label(root, text="Stock Portfolio Tracker",
         font=("Arial", 20, "bold"), bg="#f4f4f4").pack(pady=10)

# ── Input Row ────────────────────────────────
top_frame = tk.Frame(root, bg="#f4f4f4")
top_frame.pack(pady=5)

tk.Label(top_frame, text="Stock Symbol:", bg="#f4f4f4").grid(row=0, column=0, padx=5, pady=5)
stock_entry = tk.Entry(top_frame, width=15)
stock_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(top_frame, text="Quantity:", bg="#f4f4f4").grid(row=0, column=2, padx=5, pady=5)
quantity_entry = tk.Entry(top_frame, width=15)
quantity_entry.grid(row=0, column=3, padx=5, pady=5)

tk.Label(top_frame, text="Purchase Price (Auto):", bg="#f4f4f4").grid(row=0, column=4, padx=5, pady=5)
purchase_price_var = tk.StringVar()
purchase_price_display = tk.Entry(
    top_frame, textvariable=purchase_price_var,
    width=15, state="readonly",
    readonlybackground="#e8f5e9", fg="#27ae60",
    font=("Arial", 10, "bold")
)
purchase_price_display.grid(row=0, column=5, padx=5, pady=5)

price_display_label = tk.Label(top_frame, text="Market Price: —",
                                font=("Arial", 9), bg="#f4f4f4", fg="#888888")
price_display_label.grid(row=1, column=4, columnspan=2, pady=(0, 4))

stock_entry_var = tk.StringVar()
stock_entry.config(textvariable=stock_entry_var)
stock_entry_var.trace_add("write", on_symbol_changed)

# ── Action Buttons ───────────────────────────
button_frame = tk.Frame(root, bg="#f4f4f4")
button_frame.pack(pady=10)

tk.Button(button_frame, text="Add Stock",    command=add_stock,             width=12, bg="#4CAF50", fg="white").grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Remove Stock", command=remove_stock,          width=12, bg="#f39c12", fg="white").grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Clear",        command=clear_portfolio,       width=12, bg="#e74c3c", fg="white").grid(row=0, column=2, padx=5)
tk.Button(button_frame, text="Save",         command=save_portfolio,        width=12, bg="#3498db", fg="white").grid(row=0, column=3, padx=5)
tk.Button(button_frame, text="Load",         command=load_portfolio,        width=12, bg="#9b59b6", fg="white").grid(row=0, column=4, padx=5)
tk.Button(button_frame, text="Show Prices",  command=show_available_stocks, width=12, bg="#34495e", fg="white").grid(row=0, column=5, padx=5)

# ── Feature Buttons ───────────────────────────
feature_frame = tk.Frame(root, bg="#f4f4f4")
feature_frame.pack(pady=4)

tk.Button(feature_frame, text="Export TXT Report", command=export_txt_report, width=18, bg="#16a085", fg="white").grid(row=0, column=0, padx=8)
tk.Button(feature_frame, text="Pie Chart",          command=show_pie_chart,   width=18, bg="#8e44ad", fg="white").grid(row=0, column=1, padx=8)

# ── Statistics Dashboard ─────────────────────
stats_outer = tk.LabelFrame(root, text="  Statistics Dashboard  ",
                              font=("Arial", 11, "bold"),
                              bg="#f4f4f4", fg="#2c3e50", bd=2, relief="groove")
stats_outer.pack(pady=6, padx=20, fill="x")

stats_inner = tk.Frame(stats_outer, bg="#f4f4f4")
stats_inner.pack(pady=6)

STAT_FONT_LBL = ("Arial", 10, "bold")
STAT_FONT_VAL = ("Arial", 11)

tk.Label(stats_inner, text="Total Stocks:",       font=STAT_FONT_LBL, bg="#f4f4f4", fg="#555").grid(row=0, column=0, padx=18, sticky="e")
stat_stocks_val = tk.Label(stats_inner, text="0", font=("Arial", 11, "bold"), bg="#f4f4f4", fg="#2c3e50")
stat_stocks_val.grid(row=0, column=1, padx=6, sticky="w")

tk.Label(stats_inner, text="Best Performer:",     font=STAT_FONT_LBL, bg="#f4f4f4", fg="#555").grid(row=0, column=2, padx=18, sticky="e")
stat_best_val = tk.Label(stats_inner, text="—",   font=STAT_FONT_VAL, bg="#f4f4f4", fg="#27ae60")
stat_best_val.grid(row=0, column=3, padx=6, sticky="w")

tk.Label(stats_inner, text="Worst Performer:",    font=STAT_FONT_LBL, bg="#f4f4f4", fg="#555").grid(row=0, column=4, padx=18, sticky="e")
stat_worst_val = tk.Label(stats_inner, text="—",  font=STAT_FONT_VAL, bg="#f4f4f4", fg="#e74c3c")
stat_worst_val.grid(row=0, column=5, padx=6, sticky="w")

tk.Label(stats_inner, text="Portfolio Return %:", font=STAT_FONT_LBL, bg="#f4f4f4", fg="#555").grid(row=0, column=6, padx=18, sticky="e")
stat_return_val = tk.Label(stats_inner, text="0.00%", font=("Arial", 11, "bold"), bg="#f4f4f4", fg="#2c3e50")
stat_return_val.grid(row=0, column=7, padx=6, sticky="w")

# ── Portfolio Table ───────────────────────────
table_frame = tk.Frame(root, bg="#f4f4f4")
table_frame.pack(pady=10, fill="both", expand=True)

columns = ("Stock", "Qty", "Avg Buy", "Current", "Invested", "Value", "P/L", "P/L %", "Alloc %")
tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=110, anchor="center")

scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
tree.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

tree.bind("<<TreeviewSelect>>", on_tree_select)

# ── Summary Labels ────────────────────────────
summary_frame = tk.Frame(root, bg="#f4f4f4")
summary_frame.pack(pady=5)

invested_label = tk.Label(summary_frame, text="Total Invested: ₹0.00",
                           font=("Arial", 12, "bold"), bg="#f4f4f4", fg="#2c3e50")
invested_label.grid(row=0, column=0, padx=20)

current_label = tk.Label(summary_frame, text="Current Value:  ₹0.00",
                          font=("Arial", 12, "bold"), bg="#f4f4f4", fg="#2c3e50")
current_label.grid(row=0, column=1, padx=20)

profit_label = tk.Label(summary_frame, text="Profit/Loss: ₹0.00",
                         font=("Arial", 12, "bold"), bg="#f4f4f4", fg="#2c3e50")
profit_label.grid(row=0, column=2, padx=20)

# ── Stock Details Panel ───────────────────────
details_frame = tk.Frame(root, bg="#ffffff", bd=2, relief="groove")
details_frame.pack(pady=10, fill="both", expand=False, padx=20)

tk.Label(details_frame, text="Stock Details",
         font=("Arial", 14, "bold"), bg="#ffffff").pack(pady=5)

details_text = tk.Text(details_frame, height=8, width=120, font=("Consolas", 11))
details_text.pack(padx=10, pady=10, fill="both", expand=True)
details_text.config(state="disabled")

update_details()
refresh_table()
root.mainloop()
