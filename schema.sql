drop table if exists entries;
create table test.t_entries (
	Fid int(10) not null auto_increment,
	Ftitle varchar(20) not null default '',
	Ftext varchar(128) not null default '',
	primary_key(Fid)
)engine=innodb default charset=utf8;