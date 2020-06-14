#!/usr/bin/env python
# coding: utf-8

# # Let's get used to the Spark API
# 
# The new version of Spark allows us to use dataframes just like we're used to. The main changes come around in the fact that Spark is designed to work on huge data. Thus, the way it actually does the manipulations is called "Lazy Evaluation." Basically, Spark keeps track of the things we ask it to do, but doesn't actually do them until we're ready to see a result. Let's get some data loaded and check things out.
# 
# >Sidenote: 
# >
# >The last thing to keep in mind is that Spark more or less promises us that when we write code and get it working on our local machine, the same code will work on a huge cluster. Behind the scenes, it handles all of the data loading and process management, so we can write code on a single machine that should also be efficient on a huge cluster. 

# In[ ]:


import pyspark

spark = pyspark.sql.SparkSession.builder.getOrCreate()


# In[ ]:


cars = spark.read.csv('data/auto-mpg.csv', header='true', inferSchema='true', sep=',')


# In[ ]:


cars.printSchema()


# In[ ]:


cars.show(5)


# Let's take a look at what a Dataframe really is in Spark.

# In[ ]:


# Note: DON'T DO THIS, THIS IS JUST FOR DEMO PURPOSES
for x in cars.head(5):
    print(x)


# ## Filtering

# In[ ]:


my_filter_plan = cars.filter(cars.model_year >75)


# Note that it didn't do anything! We haven't asked us to show anything yet, so it's still in the planning stages of the action.

# In[ ]:


my_filter_plan.filter(cars.model_year >76).show()


# In[ ]:


cars.filter(cars.model_year >75).show(5)


# Multiple filters can just be stacked together.

# In[ ]:


cars.filter(cars.model_year >75).filter(cars.weight > 2300).show(5)


# In[ ]:


print(cars.filter(cars.model_year >75).filter(cars.weight > 2300).explain())


# ## Selection

# In[ ]:


cars.select(['displacement','car_name']).show(5)


# In[ ]:


cars.filter(cars.model_year >75).filter(cars.weight > 2300).select(['weight','car_name']).show(5)


# ## Renaming/Making new columns

# In[ ]:


cars.withColumn('YEAH', cars.car_name).select(['car_name','YEAH']).show(5)


# In[ ]:


cars.withColumn('Year_1', cars.model_year + 1).select(['model_year','Year_1']).show(5)


# ## Groupby

# In[ ]:


cars.select(["model_year",'mpg']).groupby('model_year').mean().orderBy('model_year').show(10)


# ## UDF - User Defined Functions

# This is sort of the Spark equivalent of doing an Apply in pandas. Let's see how it works.

# In[ ]:


# Define our function
def squared(s):
    return s * s

# Now tell spark that this function is a legal function for use with Spark SQL (see below)
spark.udf.register("squaredWithPython", squared)


# In[ ]:


cars.select()


# In[ ]:


# prepare the function for use with the dataframe style manipulation
from pyspark.sql.functions import udf
from pyspark.sql.types import FloatType
squared_udf = udf(lambda x: squared(x), FloatType())

cars.select("mpg", squared_udf('mpg').alias("mpg_squared")).show()


# # Using SQL with Spark

# The first step is to tell spark to treat our dataframe as a table we can query.

# In[ ]:


cars.createOrReplaceTempView("cars")


# Now we can just query it with all of our normal SQL queries.

# In[ ]:


spark.sql('SELECT car_name, mpg, model_year FROM cars WHERE model_year="75"').show()


# In[ ]:


cmd = '''SELECT MAX(mpg), model_year 
FROM cars 
GROUP BY model_year'''

spark.sql(cmd).show()


# In[ ]:


cmd = '''SELECT MAX(mpg), model_year, squaredWithPython(MAX(mpg))
FROM cars 
GROUP BY model_year'''

spark.sql(cmd).show()


# # More advanced functionality

# ## Create From Pandas

# In[ ]:


import pandas as pd

df = pd.read_csv("data/auto-mpg.csv")

df_spark = spark.createDataFrame(df)


# In[ ]:


df_spark.show(5)


# The `createDataFrame` method can choke if your pandas dataframe has uneven types (it says object, but some of them are integers or nulls or whatever. If that's the case, you'll have to create a SCHEMA by hand. Example:

# In[ ]:


from pyspark.sql.types import *

mySchema = StructType([ StructField("mpg", FloatType(), True)                       ,StructField("cylinders", IntegerType(), True)                       ,StructField("displacement", FloatType(), True)                       ,StructField("horsepower", FloatType(), True)                       ,StructField("weight", IntegerType(), True)                       ,StructField("acceleration", FloatType(), True)                       ,StructField("model_year", IntegerType(), True)                       ,StructField("origin", IntegerType(), True)                       ,StructField("car_name", StringType(), True) ])

df_spark = spark.createDataFrame(df, schema=mySchema)


# In[ ]:


df_spark.printSchema()


# ## Create From Lists

# In[ ]:


spark.createDataFrame([[1,2,3],[4,5,6]]).show()


# ## Working with Strings

# In[ ]:


from pyspark.sql.functions import split, explode, col, lower, sort_array
(
cars.withColumn('split_names', split(lower(col('car_name')), ":"))
    .select('split_names','car_name').show(10, truncate=False)
)


# In[ ]:


(
cars.withColumn('split_names', sort_array(split(lower(col('car_name')), "")))
    .select('split_names','car_name').show(10, truncate=False)
)


# In[ ]:


(
cars.withColumn('split_names', split(lower(col('car_name')), ","))
    .select('split_names','car_name').show(10, truncate=False)
)


# In[ ]:


(
cars.withColumn('split_names', explode(split(lower(col('car_name')), ",")))
    .select('split_names','car_name').show(10, truncate=False)
)


# In[ ]:

