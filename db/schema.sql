PRAGMA foreign_keys = ON;

CREATE TABLE companies (
    company_id INTEGER PRIMARY KEY,
    company_name TEXT NOT NULL,
    ticker TEXT UNIQUE,
    sector_id INTEGER
);

CREATE TABLE sectors (
    sector_id INTEGER PRIMARY KEY,
    sector_name TEXT UNIQUE
);

CREATE TABLE profitandloss (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER,
    year INTEGER,
    sales REAL,
    profit REAL,
    FOREIGN KEY(company_id) REFERENCES companies(company_id)
);

CREATE TABLE balancesheet (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER,
    year INTEGER,
    assets REAL,
    liabilities REAL,
    FOREIGN KEY(company_id) REFERENCES companies(company_id)
);

CREATE TABLE cashflow (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER,
    year INTEGER,
    net_cash REAL,
    FOREIGN KEY(company_id) REFERENCES companies(company_id)
);

CREATE TABLE analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER,
    year INTEGER,
    opm REAL,
    FOREIGN KEY(company_id) REFERENCES companies(company_id)
);

CREATE TABLE documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER,
    url TEXT,
    FOREIGN KEY(company_id) REFERENCES companies(company_id)
);

CREATE TABLE prosandcons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER,
    pros TEXT,
    cons TEXT,
    FOREIGN KEY(company_id) REFERENCES companies(company_id)
);

CREATE TABLE stock_prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER,
    trade_date DATE,
    close_price REAL,
    FOREIGN KEY(company_id) REFERENCES companies(company_id)
);

CREATE TABLE financial_ratios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER,
    year INTEGER,
    eps REAL,
    roe REAL,
    FOREIGN KEY(company_id) REFERENCES companies(company_id)
);

CREATE TABLE peer_groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER,
    peer_company_id INTEGER,
    FOREIGN KEY(company_id) REFERENCES companies(company_id)
);
