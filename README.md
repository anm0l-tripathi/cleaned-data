# cleaned-data
Task 2: Exploratory Data Analysis (Sales Data)
Data: cleaned_data.csv (200 orders, Jan-Dec 2025, 7 cities, 5 products) from Task 1. Run: python task1_clean.py then python task2_analysis.py (needs pandas, matplotlib, seaborn). Charts go in charts/, statistics in stats_summary.csv.
Key statistics
Total revenue: ₹80.6 lakh from 200 orders; average order ₹40,288 (median ₹37,984).
Average age 41.5 (range 18-65); average quantity 3.1 per order; average rating 3.07 / 5.
129 unique customers, 50 of them ordered more than once.
Insights
Mobile and Tablet drive revenue. Together they bring in about ₹36.2 lakh (45% of revenue). Headphones and Laptop are the weakest. See 1_product_revenue_rating.png.
Tablet and Laptop are top-selling but poorly rated. Tablet (2.8) and Laptop (2.7) are below the 3.07 average, while Smartwatch (3.4) and Mobile (3.3) are highest. Tablets earn almost as much as Mobiles, so improving their quality is a revenue-protection priority.
Revenue is concentrated in three cities. Chennai (₹15.0L), Delhi (₹14.7L) and Pune (₹13.4L) generate over half of revenue. Kolkata and Hyderabad (₹8.1L each) earn about half of Chennai, so they are growth opportunities. See 2_city_revenue.png.
Sales peak mid-year and dip in spring and November. June-July are the strongest months (22-24 orders, about ₹10L each), while April (10 orders) and November (12) are the weakest. Promotions could target those dips. See 3_monthly_trend.png.
Younger customers spend more. The 18-30 group averages about ₹43k per order versus about ₹32k for the 60+ group. See 4_age_order_value.png.
Higher spend does not mean happier customers. Amount and rating are weakly negatively correlated (r = -0.14), so expensive orders are not rated better. This is weak, so treat it as a hint only. See 7_correlation.png.
Anomalies and data quality
Invalid values: 7 ratings outside 1-5 and 4 negative quantities were set to missing during cleaning.
Prices look synthetic: every product has almost the same amount range (about ₹1.5k-₹80k), so a Laptop can cost less than a Headphones order. Real data would show clear price differences. See 9_amount_by_product_box.png.
Polarised ratings: 37% of ratings are 1-2 and 38% are 4-5, with a flat distribution and few neutral scores. See 6_rating_distribution.png.
No statistical outliers in amount using the IQR rule.
Assumption: "Head Mobiles" was treated as a typo for Headphones.
