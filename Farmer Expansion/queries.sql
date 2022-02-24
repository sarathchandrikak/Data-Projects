%%sql
postgresql:///groceries 

# 1

with TotalSales(month, total_sales) as
(
    select substring(p.fulldate, 6, 2), count(*) from purchases_2020 p 
    inner join categories c on p.purchaseid = c.purchase_id
    where LEFT(p.fulldate, 4) = '2020' and c.category in ('whole milk', 'yogurt', 'domestic eggs')
    group by substring(p.fulldate, 6, 2) 
)

select * from TotalSales


# 2


with CTE1 (month, total_sales)
as 
(
    select substring(p.fulldate, 6, 2), count(*) from purchases_2020 p 
    inner join categories c on p.purchaseid = c.purchase_id
    where LEFT(p.fulldate, 4) = '2020' 
    group by substring(p.fulldate, 6, 2) 
)
, CTE2(month, diary_sales) as 
(

    select substring(p.fulldate, 6, 2), count(*) from purchases_2020 p 
    inner join categories c on p.purchaseid = c.purchase_id
    where LEFT(p.fulldate, 4) = '2020' and c.category in ('whole milk', 'yogurt', 'domestic eggs')
    group by substring(p.fulldate, 6, 2) 
)
    

select 
    c1.month, 
    Round((100 *(cast(c2.diary_sales as Numeric(8, 2)) / cast(c1.total_sales as Numeric(8,2)))), 2) 
    as market_share 
    from CTE1 c1 inner join CTE2 c2 
    on c1.month = c2.month
    
    
# 3 

with CTE1 (month, dairy_sales_2020)
as 
(
    select substring(p.fulldate, 6, 2), count(*) from purchases_2020 p 
    inner join categories c on p.purchaseid = c.purchase_id
    where LEFT(p.fulldate, 4) = '2020' and c.category in ('whole milk', 'yogurt', 'domestic eggs')
    group by substring(p.fulldate, 6, 2) 
)
, CTE2 (month, dairy_sales_2019) as 
(

    select substring(p.full_date, 6, 2), count(*) from purchases_2019 p 
    inner join categories c on p.purchase_id = c.purchase_id
    where LEFT(p.full_date, 4) = '2019' and c.category in ('whole milk', 'yogurt', 'domestic eggs')
    group by substring(p.full_date, 6, 2) 
)


select c1.month, 
        (
            ROUND(100 * 
             (( CAST(c1.dairy_sales_2020 as Numeric(8,2)) - CAST(c2.dairy_sales_2019 as Numeric(8,2))) / CAST(c1.dairy_sales_2020 as Numeric(8,2))), 2)
        ) as year_change
        
        from CTE1 c1 inner join CTE2 c2 on c1.month = c2.month
    


# Combined Query

%%sql
postgresql:///groceries

with 
DairySales_2020 (month, dairy_sales_2020) as
(
    select substring(p.fulldate, 6, 2), count(*) from purchases_2020 p 
    inner join categories c on p.purchaseid = c.purchase_id
    where LEFT(p.fulldate, 4) = '2020' and c.category in ('whole milk', 'yogurt', 'domestic eggs')
    group by substring(p.fulldate, 6, 2) 
)

,TotalSales_2020 (month, total_sales_2020)
as 
(
    select substring(p.fulldate, 6, 2), count(*) from purchases_2020 p 
    inner join categories c on p.purchaseid = c.purchase_id
    where LEFT(p.fulldate, 4) = '2020' 
    group by substring(p.fulldate, 6, 2) 
)
,DairySales_2019(month, dairy_sales_2019) as 
(

    select substring(p.full_date, 6, 2), count(*) from purchases_2019 p 
    inner join categories c on p.purchase_id = c.purchase_id
    where LEFT(p.full_date, 4) = '2019' and c.category in ('whole milk', 'yogurt', 'domestic eggs')
    group by substring(p.full_date, 6, 2) 
)

select 
    ds_20.month, 
    ds_20.dairy_sales_2020 as total_sales,
    Round((100 *(cast(ds_20.dairy_sales_2020 as Numeric(8, 2)) / cast(ts_20.total_sales_2020 as Numeric(8,2)))), 2) as market_share, 
    ROUND(100 * ((CAST(ds_20.dairy_sales_2020 as Numeric(8,2)) - CAST(ds_19.dairy_sales_2019 as Numeric(8,2))) / CAST(ds_20.dairy_sales_2020 as Numeric(8,2))), 2) as year_change
    from DairySales_2020 ds_20 left join TotalSales_2020 ts_20 
    on (ds_20.month = ts_20.month) 
    left join DairySales_2019 as ds_19 
    on (ds_20.month = ds_19.month) 
    order by ds_20.month



