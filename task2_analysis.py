# Task 2: EDA on cleaned_data.csv  -> charts/ + stats_summary.csv
import pandas as pd, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
df = pd.read_csv("cleaned_data.csv", parse_dates=["order_date"])
df["month"] = df["order_date"].dt.to_period("M").dt.to_timestamp()

def save(name):
    plt.tight_layout(); plt.savefig(f"charts/{name}.png", dpi=150); plt.close()

# ---- Key statistics ----
stats = df[["age", "quantity", "amount", "rating"]].describe().T
stats["median"] = df[["age", "quantity", "amount", "rating"]].median()
stats.round(2).to_csv("stats_summary.csv")
print(stats.round(2))
print("Total revenue:", df.amount.sum(), "| Orders:", len(df), "| Avg order:", round(df.amount.mean()))

# 1 Revenue by product + rating
p = df.groupby("product").agg(revenue=("amount", "sum"), orders=("amount", "size"),
                              rating=("rating", "mean")).sort_values("revenue", ascending=False)
fig, ax = plt.subplots(1, 2, figsize=(11, 4))
sns.barplot(x=p.revenue / 1e5, y=p.index, ax=ax[0], color="#4C78A8")
ax[0].set(title="Total revenue by product (₹ lakh)", xlabel="₹ lakh", ylabel="")
sns.barplot(x=p.rating, y=p.index, ax=ax[1], color="#F58518")
ax[1].set(title="Average rating by product", xlabel="Rating (1-5)", ylabel="", xlim=(0, 5))
save("1_product_revenue_rating")

# 2 Revenue by city
c = df.groupby("city").amount.sum().sort_values(ascending=False) / 1e5
plt.figure(figsize=(7, 4)); sns.barplot(x=c.values, y=c.index, color="#54A24B")
plt.title("Total revenue by city (₹ lakh)"); plt.xlabel("₹ lakh"); plt.ylabel("")
save("2_city_revenue")

# 3 Monthly trend
m = df.groupby("month").agg(revenue=("amount", "sum"), orders=("amount", "size"))
fig, ax = plt.subplots(figsize=(9, 4))
ax.plot(m.index, m.revenue / 1e5, marker="o", color="#4C78A8"); ax.set_ylabel("Revenue (₹ lakh)")
ax2 = ax.twinx(); ax2.bar(m.index, m.orders, width=18, alpha=.25, color="#F58518"); ax2.set_ylabel("Orders")
ax.set_title("Monthly revenue (line) and orders (bars), 2025"); ax2.grid(False)
save("3_monthly_trend")

# 4 Age group order value
df["age_group"] = pd.cut(df.age, [17, 30, 45, 60, 70], labels=["18-30", "31-45", "46-60", "61-65+"])
a = df.groupby("age_group", observed=True).amount.mean()
plt.figure(figsize=(6, 4)); sns.barplot(x=a.index.astype(str), y=a.values, color="#B279A2")
plt.title("Average order value by age group"); plt.ylabel("₹"); plt.xlabel("")
save("4_age_order_value")

# 5 Payment method share
pm = df.payment_method.value_counts()
plt.figure(figsize=(5, 5)); plt.pie(pm, labels=pm.index, autopct="%1.0f%%", startangle=90)
plt.title("Orders by payment method"); save("5_payment_share")

# 6 Rating distribution (anomaly: invalid ratings were blanked in cleaning)
plt.figure(figsize=(6, 4)); sns.countplot(x=df.rating.dropna().astype(int), color="#E45756")
plt.title("Rating distribution (flat / polarised)"); plt.xlabel("Rating"); save("6_rating_distribution")

# 7 Correlation heatmap
plt.figure(figsize=(5.5, 4.5))
sns.heatmap(df[["age", "quantity", "amount", "rating"]].corr(), annot=True, fmt=".2f", cmap="coolwarm", center=0)
plt.title("Correlation heatmap"); save("7_correlation")

# 8 Amount vs rating scatter
plt.figure(figsize=(6, 4)); sns.regplot(data=df, x="amount", y="rating", scatter_kws={"alpha": .5}, line_kws={"color": "red"})
plt.title("Order amount vs rating"); save("8_amount_vs_rating")

# 9 Anomaly: price by product (box)
plt.figure(figsize=(8, 4)); sns.boxplot(data=df, x="product", y="amount")
plt.title("Order amount by product: almost identical ranges"); save("9_amount_by_product_box")

# Anomaly checks
q1, q3 = df.amount.quantile([.25, .75]); iqr = q3 - q1
print("Amount IQR outliers:", ((df.amount < q1 - 1.5*iqr) | (df.amount > q3 + 1.5*iqr)).sum())
print("Missing ratings:", df.rating.isna().sum())
print("Repeat customers:", (df.customer_name.value_counts() > 1).sum(), "of", df.customer_name.nunique())
print("Corr amount-rating:", round(df.amount.corr(df.rating), 2))
print("Amount range by product:\n", df.groupby("product").amount.agg(["min", "median", "max"]).round(0))
print("Rating share 1-2 vs 4-5:", round((df.rating <= 2).mean(), 2), round((df.rating >= 4).mean(), 2))
print(p.round(1)); print(c.round(1)); print(m.round(0))
