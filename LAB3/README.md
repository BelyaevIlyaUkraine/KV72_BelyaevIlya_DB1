# КВ-72 Бєляєв Ілля
# Лабораторна робота №3
# Засоби оптимізації роботи СУБД PostgreSQL
# Варіант №2
![alt text](https://github.com/BelyaevIlyaUkraine/KV72_BelyaevIlya_DB/blob/master/LAB3/Variant.png)
# Структура БД
![alt text](https://github.com/BelyaevIlyaUkraine/KV72_BelyaevIlya_DB/blob/master/LAB3/BD_Structure.JPG)

[Опис структури БД](https://github.com/BelyaevIlyaUkraine/KV72_BelyaevIlya_DB/blob/master/LAB1/DB%20structure%20describing.docx)
**Сутності:**
1)Мережа:
'''
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
'''
