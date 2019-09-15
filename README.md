# KV72_BelyaevIlya_DB1
Лабораторна робота № 1.

Ознайомлення з базовими операціями СУБД PostgreSQL

КВ-72 Бєляєв Ілля Дмитрович

Варіант(2): Мережі кінотеатрів

Сутності:

1)Мережа
` ` `
CREATE TABLE public."Network"
(
    "Name" text COLLATE pg_catalog."default" NOT NULL,
    "Owner" text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "Name_pkey" PRIMARY KEY ("Name")
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public."Network"
    OWNER to postgres;
` ` `

2)Кінотеатр
` ` `
CREATE TABLE public."Cinema"
(
    "Network" text COLLATE pg_catalog."default" NOT NULL,
    "Address" text COLLATE pg_catalog."default" NOT NULL,
    "NumberOfHalls" text COLLATE pg_catalog."default" NOT NULL,
    "GenNumberOfSeats" text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "Cinema_pkey" PRIMARY KEY ("Address"),
    CONSTRAINT "NetworkFK" FOREIGN KEY ("Network")
        REFERENCES public."Network" ("Name") MATCH FULL
        ON UPDATE CASCADE
        ON DELETE CASCADE
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public."Cinema"
    OWNER to postgres;
` ` `

3)Сеанс
` ` `
CREATE TABLE public."Session"
(
    "Id" integer NOT NULL DEFAULT nextval('"Session_Id_seq"'::regclass),
    "Start" text COLLATE pg_catalog."default" NOT NULL,
    "Film" integer NOT NULL,
    "HallNumber" text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "Session_pkey" PRIMARY KEY ("Id"),
    CONSTRAINT "Film_FK" FOREIGN KEY ("Film")
        REFERENCES public."Film" ("Id") MATCH FULL
        ON UPDATE CASCADE
        ON DELETE CASCADE
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public."Session"
    OWNER to postgres;
` ` `4)Фільм

` ` `
CREATE TABLE public."Film"
(
    "Id" integer NOT NULL DEFAULT nextval('"Film_Id_seq"'::regclass),
    "Name" text COLLATE pg_catalog."default" NOT NULL,
    "Genre" text COLLATE pg_catalog."default" NOT NULL,
    "Year" text COLLATE pg_catalog."default" NOT NULL,
    "Budget" text COLLATE pg_catalog."default" NOT NULL,
    "Country" text COLLATE pg_catalog."default" NOT NULL,
    "Duration" text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "Film_pkey" PRIMARY KEY ("Id")
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public."Film"
    OWNER to postgres;
` ` `
