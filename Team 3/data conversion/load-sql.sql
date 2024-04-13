

DROP TABLE team3.output_parquet_gzip ;
CREATE TABLE IF NOT EXISTS team3.output_parquet_gzip (
                finaldisposition varchar(256), sentencetime bigint, court varchar(256), complainant varchar(256), publicdefender varchar, gender varchar(256), race varchar(256), casetype varchar(256), class varchar(256), codesection varchar(256), chargeamended varchar
            );
Insert into  dev.team3.output_parquet_gzip  
Select 
finaldisposition , cast(sentencetime AS  bigint), court , complainant , publicdefender, gender , race , casetype , class , codesection , chargeamended 
   from 
dev.team3_data.output_parquet_gzip ;

DROP TABLE team3.output_parquet_snappy ;
CREATE TABLE IF NOT EXISTS team3.output_parquet_snappy (
                finaldisposition varchar(256), sentencetime bigint, court varchar(256), complainant varchar(256), publicdefender varchar, gender varchar(256), race varchar(256), casetype varchar(256), class varchar(256), codesection varchar(256), chargeamended varchar
            );
Insert into  dev.team3.output_parquet_snappy  
Select 
finaldisposition , cast(sentencetime AS  bigint), court , complainant , publicdefender, gender , race , casetype , class , codesection , chargeamended 
   from 
dev.team3_data.output_parquet_snappy ;
-----------


-----------


DROP TABLE team3.output_parquet_zstd ;
CREATE TABLE IF NOT EXISTS team3.output_parquet_zstd (
                finaldisposition varchar(256), sentencetime bigint, court varchar(256), complainant varchar(256), publicdefender varchar, gender varchar(256), race varchar(256), casetype varchar(256), class varchar(256), codesection varchar(256), chargeamended varchar
            );
Insert into  dev.team3.output_parquet_zstd  
Select 
finaldisposition , cast(sentencetime AS  bigint), court , complainant , publicdefender, gender , race , casetype , class , codesection , chargeamended 
   from 
dev.team3_data.output_parquet_zstd ;

--select * from dev.team3.output_parquet_zstd limit 10
-----------

DROP TABLE team3.output_parquet_lz4 ;  /*Not supported */ 
CREATE TABLE IF NOT EXISTS team3.output_parquet_lz4 (
                finaldisposition varchar(256), sentencetime bigint, court varchar(256), complainant varchar(256), publicdefender varchar, gender varchar(256), race varchar(256), casetype varchar(256), class varchar(256), codesection varchar(256), chargeamended varchar
            );
Insert into  dev.team3.output_parquet_lz4  
Select 
finaldisposition , cast(sentencetime AS  bigint), court , complainant , publicdefender, gender , race , casetype , class , codesection , chargeamended 
   from 
dev.team3_data.output_parquet_lz4;

----select * from dev.team3.output_parquet_lz4 limit 10

----------

DROP TABLE team3.output_parquet_lzo ;  /*Not supported */
CREATE TABLE IF NOT EXISTS team3.output_parquet_lzo (
                finaldisposition varchar(256), sentencetime bigint, court varchar(256), complainant varchar(256), publicdefender varchar, gender varchar(256), race varchar(256), casetype varchar(256), class varchar(256), codesection varchar(256), chargeamended varchar
            );
Insert into  dev.team3.output_parquet_lzo  
Select 
finaldisposition , cast(sentencetime AS  bigint), court , complainant , publicdefender, gender , race , casetype , class , codesection , chargeamended 
   from 
dev.team3_data.output_parquet_lzo ;

--select * from dev.team3.output_parquet_lzo limit 10

-------------

DROP TABLE team3.output_orc_zlib ;  /*Not supported */
CREATE TABLE IF NOT EXISTS team3.output_orc_zlib (
                finaldisposition varchar(256), sentencetime bigint, court varchar(256), complainant varchar(256), publicdefender varchar, gender varchar(256), race varchar(256), casetype varchar(256), class varchar(256), codesection varchar(256), chargeamended varchar
            );
Insert into  dev.team3.output_orc_zlib  
Select 
finaldisposition , cast(sentencetime AS  bigint), court , complainant , publicdefender, gender , race , casetype , class , codesection , chargeamended 
   from 
dev.team3_data.output_orc_zlib ;

--select * from dev.team3.output_orc_zlib limit 100;

----------------------

DROP TABLE team3.output_orc_snappy ;  
CREATE TABLE IF NOT EXISTS team3.output_orc_snappy (
                finaldisposition varchar(256), sentencetime bigint, court varchar(256), complainant varchar(256), publicdefender varchar, gender varchar(256), race varchar(256), casetype varchar(256), class varchar(256), codesection varchar(256), chargeamended varchar
            );
Insert into  dev.team3.output_orc_snappy  
Select 
finaldisposition , cast(sentencetime AS  bigint), court , complainant , publicdefender, gender , race , casetype , class , codesection , chargeamended 
   from 
dev.team3_data.output_orc_snappy ;

--select count(*) from dev.team3.output_orc_snappy ;

----------

DROP TABLE team3.output_orc_zlib ;  
CREATE TABLE IF NOT EXISTS team3.output_orc_zlib (
                finaldisposition varchar(256), sentencetime bigint, court varchar(256), complainant varchar(256), publicdefender varchar, gender varchar(256), race varchar(256), casetype varchar(256), class varchar(256), codesection varchar(256), chargeamended varchar
            );
Insert into  dev.team3.output_orc_zlib  
Select 
finaldisposition , cast(sentencetime AS  bigint), court , complainant , publicdefender, gender , race , casetype , class , codesection , chargeamended 
   from 
dev.team3_data.output_orc_zlib ;

--select count(*) from dev.team3.output_orc_zlib limit 10;

--------------------

DROP TABLE team3.output_json_snappy ;  
CREATE TABLE IF NOT EXISTS team3.output_json_snappy (
                finaldisposition varchar(256), sentencetime bigint, court varchar(256), complainant varchar(256), publicdefender varchar, gender varchar(256), race varchar(256), casetype varchar(256), class varchar(256), codesection varchar(256), chargeamended varchar
            );
Insert into  dev.team3.output_json_snappy  
Select 
finaldisposition , cast(sentencetime AS  bigint), court , complainant , publicdefender, gender , race , casetype , class , codesection , chargeamended 
   from 
dev.team3_data.output_json_snappy ;

--select * from dev.team3.output_json_snappy limit 10;

-------------

DROP TABLE team3.output_json_gzip;  
CREATE TABLE IF NOT EXISTS team3.output_json_gzip (
                finaldisposition varchar(256), sentencetime bigint, court varchar(256), complainant varchar(256), publicdefender varchar, gender varchar(256), race varchar(256), casetype varchar(256), class varchar(256), codesection varchar(256), chargeamended varchar
            );
Insert into  dev.team3.output_json_gzip  
Select 
finaldisposition , cast(sentencetime AS  bigint), court , complainant , publicdefender, gender , race , casetype , class , codesection , chargeamended 
   from 
dev.team3_data.output_json_gzip  ;

--select count(*) from dev.team3.output_json_gzip limit 10;

-------------

DROP TABLE team3.output_csv_snappy;  
CREATE TABLE IF NOT EXISTS team3.output_csv_snappy (
                finaldisposition varchar(256), sentencetime bigint, court varchar(256), complainant varchar(256), publicdefender varchar, gender varchar(256), race varchar(256), casetype varchar(256), class varchar(256), codesection varchar(256), chargeamended varchar
            );
Insert into  dev.team3.output_csv_snappy  
Select 
col0 , cast(col1 AS  bigint) , col2, col3 , cast(col4 as boolean) , col5, col6 , col7 , col8 , col9 , col10 
   from 
dev.team3_data.output_csv_snappy ;

--select count(*) from dev.team3.output_csv_snappy  limit 10;

-----------

DROP TABLE team3.output_csv_gzip;  
CREATE TABLE IF NOT EXISTS team3.output_csv_gzip (
                finaldisposition varchar(256), sentencetime bigint, court varchar(256), complainant varchar(256), publicdefender varchar, gender varchar(256), race varchar(256), casetype varchar(256), class varchar(256), codesection varchar(256), chargeamended varchar
            );
Insert into  dev.team3.output_csv_gzip  
Select 
col0 , cast(col1 AS  bigint) , col2, col3 ,  cast(col4 as boolean) , col5, col6 , col7 , col8 , col9 , col10 
   from 
dev.team3_data.output_csv_gzip ;

--select count(*) from dev.team3.output_csv_gzip  limit 10;