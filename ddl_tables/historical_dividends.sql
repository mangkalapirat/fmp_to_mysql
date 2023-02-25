CREATE TABLE IF NOT EXISTS historical_dividends(
    symbol varchar(10),
    date date,
    label varchar(30),
    adjDividend float,
    dividend float,
    recordDate date,
    paymentDate date,
    declarationDate date,

    PRIMARY KEY (symbol, date)
)
