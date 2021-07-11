create table if not exists users (
	id serial primary key,
	settings varchar(100)
);

create table if not exists favorite_list (
	id_users integer references users(id),
	id_vk integer,
	constraint pk_favorite_list primary key (id_users, id_vk)
);

create table if not exists black_list (
	id_users integer references users(id),
	id_vk integer,
	constraint pk_black_list primary key (id_users, id_vk)
);
