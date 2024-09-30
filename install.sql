CREATE TABLE "clubs" (
	"id"	INTEGER NOT NULL,
	"denominazione"	TEXT NOT NULL,
	"codicefiscale"	TEXT,
	"partitaiva"	TEXT,
	"indirizzo"	TEXT,
	"civ"	TEXT,
	"comune"	TEXT,
	"prov"	TEXT,
	"cap"	TEXT,
	"email"	TEXT,
	"email2"	TEXT,
	"tel"	TEXT,
	"cell"	TEXT,
	"cell2"	TEXT,
	"codiceaffiliazione"	TEXT,
	"url"	TEXT,
	"url2"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE "people" (
	"id"	INTEGER NOT NULL,
	"nome"	TEXT NOT NULL,
	"cognome"	TEXT,
	"sesso"	INTEGER,
	"datanascita"	TEXT,
	"comunenascita"	TEXT,
	"provnascita"	TEXT,
	"codicefiscale"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
)