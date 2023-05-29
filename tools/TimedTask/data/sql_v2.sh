month=$(date -d "30 days ago" +%Y-%m)
echo $month
hive -e "set hive.cli.print.header=True;
select 
  a.series_id as seriesid, 
  a.series_name as seriesname, 
  a.spec_level as spec_level,
  a.car_type as car_type,
  a.spec_brand as spec_brand,
  a.country as country,
  row_number() over(
    partition by mt 
    order by 
      a.sale_num desc
  ) as rn, 
  a.sale_num as salecnt,
  b.series_is_new_energy as energy
from 
  (
    select 
      mt, 
      trim(series_id) as series_id, 
      trim(series_name) as series_name, 
      sum(
        coalesce(
          cast(sale_num * 1 as bigint), 
          0
        )
      ) as sale_num, 
      sum(
        coalesce(
          cast(pro_num * 1 as bigint), 
          0
        )
      ) as pro_num,
      trim(spec_level) as spec_level,
      trim(car_type) as car_type,
      trim(spec_brand) as spec_brand,
      trim(country) as country
    from 
      dim.dim_bdp_ufeel_prosale_clh_result_mi 
    where 
      mt = '$month' 
    group by 
      mt, 
      trim(series_id), 
      trim(series_name),
      trim(spec_level),
      trim(car_type),
      trim(spec_brand),
      trim(country)
  ) a 
  join dim.dim_series_view b on a.series_id = b.series_id "|tr '\t' ','>'./data/'sales_board_$month.csv

