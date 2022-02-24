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






