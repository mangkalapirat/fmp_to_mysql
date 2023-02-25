CREATE TABLE IF NOT EXISTS delisted_companies(
    symbol varchar(10),
    companyName varchar(500),
    exchange varchar(20),
    ipoDate date,
    delistedDate date,

    PRIMARY KEY (symbol)
)
