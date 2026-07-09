-- 1
SELECT COUNT(*) FROM companies;

-- 2
SELECT COUNT(*) FROM stock_prices;

-- 3
SELECT year, SUM(sales)
FROM profitandloss
GROUP BY year;

-- 4
SELECT company_id, AVG(opm)
FROM analysis
GROUP BY company_id;

-- 5
SELECT company_id, AVG(eps)
FROM financial_ratios
GROUP BY company_id;

-- 6
SELECT company_id, COUNT(*)
FROM balancesheet
GROUP BY company_id;

-- 7
SELECT company_id, COUNT(*)
FROM cashflow
GROUP BY company_id;

-- 8
SELECT company_id, COUNT(*)
FROM documents
GROUP BY company_id;

-- 9
SELECT sector_name, COUNT(*)
FROM sectors
GROUP BY sector_name;

-- 10
SELECT company_id, MAX(close_price)
FROM stock_prices
GROUP BY company_id;