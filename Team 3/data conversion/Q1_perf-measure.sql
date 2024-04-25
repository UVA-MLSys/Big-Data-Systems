set enable_result_cache_for_session to off;

Select finaldisposition ,sentencetime , court , complainant , publicdefender, gender , race , casetype , class , codesection , chargeamended , count(*)
from dev.team3.output_parquet_gzip 
group by finaldisposition , sentencetime , court , complainant , publicdefender, gender , race , casetype , class , codesection , chargeamended ;

Select finaldisposition ,sentencetime , court , complainant , publicdefender, gender , race , casetype , class , codesection , chargeamended , count(*)
from dev.team3.output_parquet_snappy
group by finaldisposition , sentencetime , court , complainant , publicdefender, gender , race , casetype , class , codesection , chargeamended ;

Select finaldisposition ,sentencetime , court , complainant , publicdefender, gender , race , casetype , class , codesection , chargeamended , count(*)
from dev.team3.output_parquet_zstd
group by finaldisposition , sentencetime , court , complainant , publicdefender, gender , race , casetype , class , codesection , chargeamended ;

Select finaldisposition ,sentencetime , court , complainant , publicdefender, gender , race , casetype , class , codesection , chargeamended , count(*)
from dev.team3.output_orc_zlib
group by finaldisposition , sentencetime , court , complainant , publicdefender, gender , race , casetype , class , codesection , chargeamended ;

Select finaldisposition ,sentencetime , court , complainant , publicdefender, gender , race , casetype , class , codesection , chargeamended , count(*)
from dev.team3.output_orc_snappy 
group by finaldisposition , sentencetime , court , complainant , publicdefender, gender , race , casetype , class , codesection , chargeamended ;

Select finaldisposition ,sentencetime , court , complainant , publicdefender, gender , race , casetype , class , codesection , chargeamended , count(*)
from dev.team3.output_json_snappy 
group by finaldisposition , sentencetime , court , complainant , publicdefender, gender , race , casetype , class , codesection , chargeamended ;

Select finaldisposition ,sentencetime , court , complainant , publicdefender, gender , race , casetype , class , codesection , chargeamended , count(*)
from dev.team3.output_json_lz 
group by finaldisposition , sentencetime , court , complainant , publicdefender, gender , race , casetype , class , codesection , chargeamended ;

Select finaldisposition ,sentencetime , court , complainant , publicdefender, gender , race , casetype , class , codesection , chargeamended , count(*)
from dev.team3.output_csv_snappy
group by finaldisposition , sentencetime , court , complainant , publicdefender, gender , race , casetype , class , codesection , chargeamended ;

Select finaldisposition ,sentencetime , court , complainant , publicdefender, gender , race , casetype , class , codesection , chargeamended , count(*)
from dev.team3.output_csv_gzip
group by finaldisposition , sentencetime , court , complainant , publicdefender, gender , race , casetype , class , codesection , chargeamended ;




SELECT *
FROM stl_query  
where querytxt like '%output_parquet_gzip%'
ORDER BY starttime DESC


SELECT query,querytxt,
  --COUNT(*) as num_queries,
  AVG(DATEDIFF(sec,starttime,endtime)) avg_duration,
  MIN(starttime) as oldest_ts,
  MAX(endtime) as latest_ts
FROM stl_query
where querytxt like '%count(*)%output_%' 
GROUP BY query , querytxt
Having  avg_duration > 0
Order by oldest_ts desc;
                           
         