drop index if exists "gennumberofseats_idx";
create index "gennumberofseats_idx" on "Cinema" using hash("GenNumberOfSeats");
explain analyze select * from "Cinema" where "GenNumberOfSeats" = '888';