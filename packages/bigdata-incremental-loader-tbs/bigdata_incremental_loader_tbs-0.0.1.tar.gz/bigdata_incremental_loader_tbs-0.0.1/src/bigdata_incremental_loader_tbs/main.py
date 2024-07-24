import datetime
def last_time_for(spark, target_db_name, table_name, timestmp_col, decrease_size_in_mins):
  q = f'select max({timestmp_col}) from {target_db_name}.{table_name}'
  print('last_time_for query:', q)
  df = spark.sql(q)
  max_updated_at = df.collect()[0][0]
  print('max_updated_at:', max_updated_at)
  max_updated_prev = max_updated_at + datetime.timedelta(minutes=-decrease_size_in_mins)
  print('max_updated_prev:', max_updated_prev)
  return max_updated_prev

def fetch_from_external_src(spark, secrets, src_db_name, target_db_name, table_name, timestmp_col):
  print("Fetching data from source...")
  max_updated_prev_minute = last_time_for(target_db_name, table_name, timestmp_col, 1)
  query = f"""
  select * from `{src_db_name}`.{table_name}
  where {timestmp_col} >= '{max_updated_prev_minute}'
  """
  data_df = spark \
      .read \
     .format("jdbc") \
     .option("url", 'jdbc:mysql://' + secrets['host'] + "/" + src_db_name) \
      .option("driver", secrets['driver']) \
      .option("user", secrets['username']) \
      .option("password", secrets['password']) \
      .option("query", query) \
     .load()
  return data_df

temp_view_suffix = '_temp_src'
def external_src_incremental_load(spark, src_db_name, target_db_name, table_name):
  print("Loading data from external source...")
  df = fetch_from_external_src(src_db_name, target_db_name, table_name, 'updatedAt')
  df.createOrReplaceTempView(f'{table_name}{temp_view_suffix}')
  print("Creating merge script...")
  cols = list(map(lambda n: f"t.{n} = s.{n}", df.columns))
  query = f"""
  MERGE INTO {target_db_name}.{table_name} t
  USING {table_name}{temp_view_suffix} s
  ON t.id = s.id
  WHEN MATCHED THEN
  UPDATE SET
  {', '.join(cols)}
  WHEN NOT MATCHED BY TARGET THEN
  INSERT ({', '.join(df.columns)})
  VALUES ({', '.join(map(lambda n: f"s.{n}", df.columns))})
  """
  #print(query)
  result_df = spark.sql(query)
  result_df.show()
#spark.catalog.dropTempView(f'{table_name}{temp_view_suffix}') # dont forget to drop temp view

def add_one(number):
    return number + 1