import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job



# Create a GlueContext
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# Read parameters from command line
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'S3_INPUT_PATH', 'S3_OUTPUT_PATH'])

# Read CSV file from S3
s3_input_path = args['S3_INPUT_PATH']
df = spark.read.csv(s3_input_path, header=True)

# Define compression options
snap_compression = "snappy"
zlib_compression = "zlib" 
lz4_compression ="lz4"
gz_compression ="gzip"
lzo_compression ="lzo"
zstd_compression="zstd"

# Write DataFrame to Parquet format with specified compression
s3_output_parquet_path = args['S3_OUTPUT_PATH'] + '/output_parquet_snappy'
df.write.option("compression", snap_compression).parquet(s3_output_parquet_path, mode='overwrite')

s3_output_parquet_path = args['S3_OUTPUT_PATH'] + '/output_parquet_lz4'
df.write.option("compression", lz4_compression).parquet(s3_output_parquet_path, mode='overwrite')

s3_output_parquet_path = args['S3_OUTPUT_PATH'] + '/output_parquet_gzip'
df.write.option("compression", gz_compression).parquet(s3_output_parquet_path, mode='overwrite')

s3_output_parquet_path = args['S3_OUTPUT_PATH'] + '/output_parquet_lzo'
df.write.option("compression", lzo_compression).parquet(s3_output_parquet_path, mode='overwrite')

s3_output_parquet_path = args['S3_OUTPUT_PATH'] + '/output_parquet_zstd'
df.write.option("compression", zstd_compression).parquet(s3_output_parquet_path, mode='overwrite')

# Write DataFrame to ORC format with specified compression
s3_output_orc_path = args['S3_OUTPUT_PATH'] + '/output_orc_zlib'
df.write.option("compression", zlib_compression).orc(s3_output_orc_path, mode='overwrite')

s3_output_orc_path = args['S3_OUTPUT_PATH'] + '/output_orc_snappy'
df.write.option("compression", snap_compression).orc(s3_output_orc_path, mode='overwrite')

print("Conversion completed successfully.")



#job = Job(glueContext)
#job.init(args['JOB_NAME'], args)
#job.commit()