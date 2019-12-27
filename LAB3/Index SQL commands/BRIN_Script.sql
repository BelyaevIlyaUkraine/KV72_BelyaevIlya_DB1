drop index if exists "BRIN_idx";
create index "BRIN_idx" on "Session" using brin("Start");
explain analyze select * from "Session" where "Start" = '4103-01-08';