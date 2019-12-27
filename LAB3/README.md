# КВ-72 Бєляєв Ілля
# Лабораторна робота №3
# Засоби оптимізації роботи СУБД PostgreSQL
# Варіант №2
![alt text](https://github.com/BelyaevIlyaUkraine/KV72_BelyaevIlya_DB/blob/master/LAB3/Variant.png)
# Структура БД
![alt text](https://github.com/BelyaevIlyaUkraine/KV72_BelyaevIlya_DB/blob/master/LAB3/BD_Structure.JPG)

**[Опис структури БД](https://github.com/BelyaevIlyaUkraine/KV72_BelyaevIlya_DB/blob/master/LAB1/DB%20structure%20describing.docx)**

**[Додаток з роботою з індексами,тригером та транзакціями](https://github.com/BelyaevIlyaUkraine/KV72_BelyaevIlya_DB/blob/master/LAB3/Extra.docx)**

**Сутності:**

1)**Мережа:**
```
 -- Table: public."Network"

-- DROP TABLE public."Network";

CREATE TABLE public."Network"
(
    "Name" text COLLATE pg_catalog."default" NOT NULL,
    "Owner" text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "Network_pkey" PRIMARY KEY ("Name")
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public."Network"
    OWNER to postgres;

-- Trigger: thebesttriggerinhistory

-- DROP TRIGGER thebesttriggerinhistory ON public."Network";

CREATE TRIGGER thebesttriggerinhistory
    AFTER INSERT OR UPDATE 
    ON public."Network"
    FOR EACH ROW
    EXECUTE PROCEDURE public.func();
```
2)**Кінотеатр**
```
-- Table: public."Cinema"

-- DROP TABLE public."Cinema";

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

-- Index: gennumberofseats_idx

-- DROP INDEX public.gennumberofseats_idx;

CREATE INDEX gennumberofseats_idx
    ON public."Cinema" USING hash
    ("GenNumberOfSeats" COLLATE pg_catalog."default")
    TABLESPACE pg_default;
```
3)**Сеанс**

```
-- Table: public."Session"

-- DROP TABLE public."Session";

CREATE TABLE public."Session"
(
    "ID" integer NOT NULL DEFAULT nextval('"Session_ID_seq"'::regclass),
    "Start" timestamp(0) without time zone NOT NULL,
    "Film" integer NOT NULL,
    "HallNumber" text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "Session_pkey" PRIMARY KEY ("ID"),
    CONSTRAINT "FilmFK" FOREIGN KEY ("Film")
        REFERENCES public."Film" ("ID") MATCH FULL
        ON UPDATE CASCADE
        ON DELETE CASCADE
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public."Session"
    OWNER to postgres;

-- Index: BRIN_idx

-- DROP INDEX public."BRIN_idx";

CREATE INDEX "BRIN_idx"
    ON public."Session" USING brin
    ("Start")
    TABLESPACE pg_default;
```
4)**Фільм**
```
-- Table: public."Film"

-- DROP TABLE public."Film";

CREATE TABLE public."Film"
(
    "ID" integer NOT NULL DEFAULT nextval('"Film_ID_seq"'::regclass),
    "Name" text COLLATE pg_catalog."default" NOT NULL,
    "Genre" text COLLATE pg_catalog."default" NOT NULL,
    "Year" text COLLATE pg_catalog."default" NOT NULL,
    "Budget" text COLLATE pg_catalog."default" NOT NULL,
    "Country" text COLLATE pg_catalog."default" NOT NULL,
    "Duration" text COLLATE pg_catalog."default" NOT NULL,
    "Oscar" boolean NOT NULL,
    CONSTRAINT "Film_pkey" PRIMARY KEY ("ID")
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public."Film"
    OWNER to postgres;
```

5)**Кінотеатр-Сеанс**
```
-- Table: public."Cinema-Session"

-- DROP TABLE public."Cinema-Session";

CREATE TABLE public."Cinema-Session"
(
    "ID" integer NOT NULL DEFAULT nextval('"Cinema-Session_ID_seq"'::regclass),
    "CinemaID" text COLLATE pg_catalog."default" NOT NULL,
    "SessionID" integer NOT NULL,
    CONSTRAINT "Cinema-Session_pkey" PRIMARY KEY ("ID"),
    CONSTRAINT "CinemaID_SessionID_UN" UNIQUE ("CinemaID", "SessionID")
,
    CONSTRAINT "CinemaID_FK" FOREIGN KEY ("CinemaID")
        REFERENCES public."Cinema" ("Address") MATCH FULL
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT "SessionID_FK" FOREIGN KEY ("SessionID")
        REFERENCES public."Session" ("ID") MATCH FULL
        ON UPDATE CASCADE
        ON DELETE CASCADE
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public."Cinema-Session"
    OWNER to postgres;
```
# Файли з командами,які стосуються індексів та тригера,лежать відповідно у папках Index SQL Commands та Trigger SQL Commands
