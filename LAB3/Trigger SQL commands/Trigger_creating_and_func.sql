drop trigger if exists "thebesttriggerinhistory" on "Network";
create or replace function func() returns trigger as $$
declare
	curs cursor for select * from "Network";
	m_row "Network"%rowtype;
begin
	if TG_OP = 'INSERT' then
		for m_row in curs loop
			update "Network" set "Owner" = m_row."Owner" || 'a' where current of curs;
		end loop;
		raise notice 'Triggered on inserting!';
		return m_row;
	else
		raise notice 'Triggered on updating';
		return NULL;
	end if;
end;
$$ LANGUAGE plpgsql;

create trigger thebesttriggerinhistory
	after update or insert on "Network"
	for each row
	execute procedure func()