create table users(
	id serial primary key not null,
	username VARCHAR(100),
	phone VARCHAR(100)
	-- loginid VARCHAR(100),
	password VARCHAR(225),
	email VARCHAR(255) UNIQUE NOT NULL,
	condition VARCHAR(50),
	apikey VARCHAR(255),
	secretKey VARCHAR(255),
	verification VARCHAR(255),
	swing_point VARCHAR(100) DEFAULT '1.5',
	swing_cockpit VARCHAR(100) DEFAULT '3',
	registered BOOLEAN NOT NULL DEFAULT FALSE,
	type VARCHAR(50) NOT NULL DEFAULT 'user'
);

--이용권, 구매내역(voucher)
create table voucher (
	voucher_id serial primary key not null,
	user_id integer REFERENCES users(id) ON DELETE CASCADE,
	voucher_type VARCHAR(50) not null,
	voucher_fee REAL,
	use_coin VARCHAR(50) not null,
	created_time TIMESTAMP NOT NULL DEFAULT NOW(),
	terminated_time TIMESTAMP,
	invest_type VARCHAR(100)
)

--이용권을 사기위해서 코인구매
--거래내역
create table transactions(
	trans_id serial primary key not null,
	user_id integer REFERENCES users(id) ON DELETE CASCADE,
	market VARCHAR(50) not null,
	side VARCHAR(50) not null,
	volume REAL,
	price REAL,
	work_time TIMESTAMP,
	escape_price REAL,
	uuid TEXT not null
);


create table notice(
	notice_id serial primary key not null, 
	notice_type VARCHAR(50), -- 공지 구분
	title VARCHAR(100) NOT NULL,
	description TEXT NOT NULL,
	notice_time TIMESTAMP NOT NULL DEFAULT NOW()
);

create table question (
	q_id serial primary key not null,
	q_type VARCHAR(100),
	user_id integer REFERENCES users(id) ON DELETE CASCADE,
	title VARCHAR(225) NOT NULL,
	description TEXT  NOT NULL,
	answer TEXT
);


create table curPrice (
	cp_id serial primary key not null,
	market VARCHAR(100) not null,
	user_id integer REFERENCES users(id) ON DELETE CASCADE,
	trade_price VARCHAR(100) not null,
	cur_time VARCHAR(100) not null,
);


create table auto_bidset (
	abs_id serial primary key not null,
	user_id integer REFERENCES users(id) ON DELETE CASCADE,
	step_gain_trade VARCHAR(100),
	setp_candle VARCHAR(100),
	panic_cell_bid VARCHAR(100),
);

create table auto_askset (
	aas_id serial primary key not null,
	user_id integer REFERENCES users(id) ON DELETE CASCADE,
	auto_ask VARCHAR(100),
	auto_stoploss VARCHAR(100),
	option_swing_bullmarket VARCHAR(100),
	option_swing_bearmarket VARCHAR(100),
);

create table limit_set (
	ls_id serial primary key not null,
	user_id integer REFERENCES users(id) ON DELETE CASCADE,
	limit_bull_market_bid VARCHAR(100),
	limit_double_bid VARCHAR(100),
	limit_start_bid VARCHAR(100),
	participate_start_bid VARCHAR(100),
	limit_bear_market_bid VARCHAR(100),
	limit_bid_start_double VARCHAR(100),
	-- 동시 거래 코인 수 
	amount_smltn_trcns VARCHAR(100),
)


create table week_profit (
	week_id serial primary key not null,
	user_id integer REFERENCES users(id) ON DELETE CASCADE,
	trade_count VARCHAR(100),
	sum_profit_rate VARCHAR(100),
	update_time TIMESTAMP NOT NULL DEFAULT NOW()
)


create table volatility ( 
	v_id serial primary key not null,
	market varchar(100),
	profit_rate double precision,
	update_time TIMESTAMP NOT NULL DEFAULT NOW()
)

create table erc_tokentxns (
	erc_id serial primary key not null,
	hash text unique,
	contract_addr text,
	from_add text,
	to_add text,
	value double precision,
	p_proived boolean DEFAULT false,
	currency integer,
	trans_time TIMESTAMP
);

create table yb_point (
	erc_id serial primary key not null,
	user_id integer REFERENCES users(id) ON DELETE CASCADE,
	provided_p double precision DEFAULT 0,
	used_p double precision DEFAULT 0,
	hash text unique,
	update_time TIMESTAMP NOT NULL DEFAULT NOW()
)



create table day_quotation (
	day_qu_id serial primary key not null,
	market varchar(100),
	trade_price integer DEFAULT 0,
	change_rate double precision DEFAULT 0,
	update_time TIMESTAMP NOT NULL DEFAULT NOW()
)

create table admins (
     id serial primary key not null,
     login_id varchar(256) not null, 
     password varchar(256) not null,
     wallet TEXT,
     privatekey TEXT,
);


create table voucher (
	v_id serial primary key not null,
	user_id integer REFERENCES users(id) ON DELETE CASCADE,
	voucher double precision DEFAULT 0,
	used_voucher double precision DEFAULT 0,
	update_time TIMESTAMP NOT NULL DEFAULT NOW(),
	finish_time TIMESTAMP NOT NULL DEFAULT NOW() + interval '180 day' 
)

create table rate (
	id serial primary key not null,
	market VARCHAR(256),
	trade_price float,
	change_rate float,
	type VARCHAR(256),
	update_time TIMESTAMP NOT NULL DEFAULT NOW()
)


create table onetoone (
	id serial primary key not null,
	username VARCHAR(256),
	email VARCHAR(1000),
	phone VARCHAR(256),
	title TEXT NOT NULL,
	description TEXT NOT NULL,
	update_time TIMESTAMP NOT NULL DEFAULT NOW()
)


create table swing(
	id serial primary key not null,
	user_id integer REFERENCES users(id) ON DELETE CASCADE,
	market VARCHAR(1000),
	all_buy float,
	volume float,
	profit_rate float,
	update_time TIMESTAMP NOT NULL DEFAULT NOW()
)

create table balances(
	id serial primary key not null,
	user_id integer REFERENCES users(id) ON DELETE CASCADE,
	market VARCHAR(1000),
	all_buy float,
	volume float,
	profit_rate float,
	trade_time VARCHAR(1000),
	update_time TIMESTAMP NOT NULL DEFAULT NOW()
)

create table orders(
	id serial primary key not null,
	user_id integer REFERENCES users(id) ON DELETE CASCADE,
	market VARCHAR(1000),
	volume float,
	bid_price float,
	profit_rate float,
	work_time VARCHAR(1000),
	auto_set VARCHAR(256),
	update_time TIMESTAMP NOT NULL DEFAULT NOW()
)



create table shield_rate (
	id serial primary key not null,
	market VARCHAR(256),
	change_rate float,
	type VARCHAR(256),
	update_time TIMESTAMP NOT NULL DEFAULT NOW()
)

create table rsi_rate (
	id serial primary key not null,
	market VARCHAR(256),
	rsi_value float,
	update_time TIMESTAMP NOT NULL DEFAULT NOW()
)