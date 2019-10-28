USE datagenerator
GO

BULK INSERT dbo.[Klienci] FROM 'C:\Users\zalli\Desktop\sql\klienci.bulk' WITH (FIELDTERMINATOR='|', CODEPAGE = '65001')
BULK INSERT dbo.[Rowery] FROM 'C:\Users\zalli\Desktop\sql\rowery.bulk' WITH (FIELDTERMINATOR='|', CODEPAGE = '65001')
BULK INSERT dbo.[Lista stacji] FROM 'C:\Users\zalli\Desktop\sql\listastacji.bulk' WITH (FIELDTERMINATOR='|', CODEPAGE = '65001')
BULK INSERT dbo.[Stan stacji] FROM 'C:\Users\zalli\Desktop\sql\stanstacji.bulk' WITH (FIELDTERMINATOR='|', CODEPAGE = '65001')
BULK INSERT dbo.[Historia serwisowania] FROM 'C:\Users\zalli\Desktop\sql\historiaserwisowania.bulk' WITH (FIELDTERMINATOR='|', CODEPAGE = '65001')
BULK INSERT dbo.[Historia wypozyczen] FROM 'C:\Users\zalli\Desktop\sql\historiawypozyczen.bulk' WITH (FIELDTERMINATOR='|', CODEPAGE = '65001')