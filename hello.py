from preswald import text, plotly, connect, get_df, table, selectbox, query
import pandas as pd
import plotly.express as px

text("# Welcome to ChocoMetrics")

# # Load the CSV
connect()
df = get_df('choco_sales_cleaned')

text("### Choose a Country")
choice = selectbox(
        label="Choose a Country",
        options=["India", "Australia", "USA", "UK", "New Zealand", "Canada"]
)
sql = f"""
SELECT Product, 
       AVG(boxes_shipped) AS avg_boxes, 
       AVG(Amount) AS avg_price, 
       SUM(Amount * boxes_shipped) AS total_revenue 
FROM choco_sales_cleaned
WHERE Country = '{choice}'
GROUP BY Product
"""
try:
    filtered_df = query(sql, "choco_sales_cleaned")
except ValueError as e:
    text(f"Configuration error: {e}")
except Exception as e:
    text(f"Query error: {e}")

filtered_df['total_revenue'] = filtered_df['total_revenue']/100000

# # Create a scatter plot

fig = px.scatter(
        filtered_df,
        x='avg_price',
        y='avg_boxes',
        size='total_revenue',
        color='Product',
        title=f"Revenue Efficiency for Chocolates in {choice}",
        labels={
            'avg_price': 'Average Price',
            'avg_boxes': 'Average Boxes Shipped',
            'total_revenue': 'Total Revenue'
        },
        size_max=60
    )
fig.update_traces(textposition='top center')
fig.update_layout(xaxis_title='Average Price',
                      yaxis_title='Average Boxes Shipped',
                      legend_title='Chocolate Type')
# # # Show the plot
plotly(fig)

sql2 = f"""
SELECT "Sales Person", SUM(Amount) AS revenue, SUM(boxes_shipped) AS boxes
FROM choco_sales_cleaned
WHERE Country = '{choice}'
GROUP BY "Sales Person"
ORDER BY revenue DESC
"""
filtered_df2 = query(sql2, "choco_sales_cleaned")
top5_df = filtered_df2.sort_values(by="revenue", ascending=False).head(5)

# Create a horizontal bar chart
fig2 = px.bar(
    top5_df,
    x="revenue",
    y="Sales Person",
    orientation='h',
    title=f"Top 5 Salespeople by Revenue in {choice}",
    labels={"revenue": "Revenue", "Sales Person": "Salesperson"}
)

fig2.update_layout(yaxis=dict(categoryorder='total ascending'))
plotly(fig2)


