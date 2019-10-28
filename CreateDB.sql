CREATE DATABASE datagenerator
GO
USE datagenerator
GO

CREATE TABLE [Klienci](
	[Imie] NVARCHAR(256) NOT NULL,
	[Nazwisko] NVARCHAR(256) NOT NULL,
	[Plec] [varchar](1) NOT NULL,
	[Data urodzenia] [date] NOT NULL,
	[ID] INTEGER PRIMARY KEY
)

CREATE TABLE [Rowery](
	[ID] INTEGER PRIMARY KEY,
	[Nazwa przyjazna] NVARCHAR(256)
)

CREATE TABLE [Lista stacji](
	[ID] INTEGER PRIMARY KEY,
	[Nazwa] NVARCHAR(256) NULL,
	[Szerokosc geograficzna] [float] NOT NULL,
	[Dlugosc geograficzna] [float] NOT NULL,
	[Pojemnosc] INTEGER NOT NULL
)

CREATE TABLE [Stan stacji](
	[ID] INTEGER PRIMARY KEY,
	[Data] [datetime] NOT NULL,
	[FK_IDStacji] INTEGER FOREIGN KEY REFERENCES [Lista stacji],
	[Ilosc wolnych rowerow] INTEGER NOT NULL
)

CREATE TABLE [Historia serwisowania](
	[ID] INTEGER PRIMARY KEY,
	[FK_StacjaPoczatkowa] INTEGER FOREIGN KEY REFERENCES [Lista stacji],
	[FK_StacjaKoncowa] INTEGER FOREIGN KEY REFERENCES [Lista stacji],
	[Data] [datetime] NOT NULL,
	[FK_Rower] INTEGER FOREIGN KEY REFERENCES Rowery
)

CREATE TABLE [Historia wypozyczen](
	[ID] INTEGER PRIMARY KEY,
	[FK_Klient] INTEGER FOREIGN KEY REFERENCES Klienci,
	[FK_StacjaPoczatkowa] INTEGER FOREIGN KEY REFERENCES [Lista stacji],
	[FK_StacjaKoncowa] INTEGER FOREIGN KEY REFERENCES [Lista stacji],
	[FK_RowerID] INTEGER FOREIGN KEY REFERENCES Rowery,
	[Data wypozyczenia] [datetime] NOT NULL,
	[Data zwrotu] [datetime] NOT NULL
)