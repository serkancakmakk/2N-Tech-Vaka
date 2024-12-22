from fakers.providers.retail import Retail
from pyspark.sql import DataFrame, SparkSession

spark = (
    SparkSession
    .builder
    .appName("AshSparkApp")
    .master("local[*]")
    .getOrCreate()
)

user = Retail.fake_user()
users = Retail.fake_users(5)
order = Retail.fake_order()
orders = Retail.fake_orders(4)
product = Retail.fake_product()
products = Retail.fake_products(4)
sale = Retail.fake_sale()
sales = Retail.fake_sales(5)

products_df = products.to_pandas()
users_df = users.to_pandas()
orders_sdf = orders.to_spark(spark)

print(products_df.head())

