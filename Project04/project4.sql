DROP TABLE IF EXISTS znacol.artist CASCADE;
DROP TABLE IF EXISTS znacol.album CASCADE;
DROP TABLE IF EXISTS znacol.label CASCADE;
DROP TABLE IF EXISTS znacol.track CASCADE;
DROP TABLE IF EXISTS znacol.is_mem_of CASCADE;
DROP TABLE IF EXISTS znacol.genre CASCADE;

/*-----------------CREATE TABLES-------------------------------------*/
CREATE TABLE znacol.artist 
	(id serial, 
	name text, 
	isBand boolean, 
	PRIMARY KEY (id));
CREATE TABLE znacol.label 
	(id serial PRIMARY KEY, 
	name text, 
	location text);
CREATE TABLE znacol.album 
	(id serial PRIMARY KEY, 
	artist_id int, 
	label_id int, 
	title text, 
	year int, 
	FOREIGN KEY (artist_id) REFERENCES znacol.artist (id), 
	FOREIGN KEY (label_id) REFERENCES znacol.label (id));
CREATE TABLE znacol.track 
	(album_id int REFERENCES znacol.album (id), 
	name text, 
	number text, 
	PRIMARY KEY (album_id, name));
CREATE TABLE znacol.is_mem_of 
	(artist_group_id int REFERENCES znacol.artist (id), 
	artist_ind_id int REFERENCES znacol.artist (id), 
	begin int, 
	last int, 
	PRIMARY KEY (artist_group_id, artist_ind_id));
CREATE TABLE znacol.genre 
	(album_id int REFERENCES znacol.album (id), 
	genre text, 
	PRIMARY KEY (album_id, genre));

/*--------------------POPULATE TABLES----------------------------------*/
/*Populate artist table*/
INSERT INTO znacol.artist (name) (
	SELECT DISTINCT artist_name
	FROM project4
	WHERE artist_type='Person');
INSERT INTO znacol.artist (name) (
	SELECT DISTINCT member_name 
	FROM project4
	WHERE artist_type='Group'
	AND member_name NOT IN (SELECT name FROM artist));
UPDATE artist SET isBand=FALSE;

INSERT INTO znacol.artist (name) (
	SELECT DISTINCT artist_name
	FROM project4
	WHERE artist_type='Group');
UPDATE artist SET isBand=TRUE WHERE isBand IS NULL;

/*Populate is_mem_of (cross reference table)*/
INSERT INTO znacol.is_mem_of (artist_ind_id, artist_group_id, begin, last) 
	(SELECT ind_id, artist.id as group_id, member_begin_year, member_end_year 
	FROM 
		(SELECT DISTINCT artist.id as ind_id, project4.member_name, project4.member_begin_year, member_end_year, project4.artist_name as group_name 
		FROM project4 
		JOIN artist ON artist.name=project4.member_name) as subquery 
	JOIN artist ON artist.name=subquery.group_name);
/*Populate label table*/
INSERT INTO znacol.label (name, location) (
	SELECT DISTINCT label, headquarters
	FROM project4);

/*Populate album table*/
INSERT INTO znacol.album (artist_id, label_id, title, year) (
	SELECT artist_id, label.id as label_id, album_title, album_year 
	FROM (
		SELECT DISTINCT artist.id as artist_id, artist_name, label, album_title, album_year 
		FROM project4 JOIN artist 
		ON artist.name=project4.artist_name) as subquery 
	JOIN label ON label.name=subquery.label);

/*Populate track table*/
INSERT INTO znacol.track (album_id, name, number) 
	(SELECT DISTINCT album.id, track_name, track_number 
	FROM project4 
	JOIN album ON album.title=project4.album_title);

/*Populate genre table*/
INSERT INTO znacol.genre (album_id, genre) (
	SELECT DISTINCT album.id, genre 
	FROM project4 
	JOIN album ON album.title=project4.album_title);

/*----------------------------QUERYING DATABASE---------------------------*/
/*1. Get all members of The Who and their begin/end years with the group ordered by their starting year and name.*/
SELECT name, begin, last 
	FROM 
		(SELECT * 
		FROM is_mem_of 
		WHERE artist_group_id=
			(SELECT artist.id 
			FROM artist 
			WHERE name='The Who')) as subquery 
	JOIN artist ON artist.id=subquery.artist_ind_id 
	ORDER BY begin, name;

/*2. Get all groups that Chris Thile has been a part of.*/
SELECT name 
	FROM 
		(SELECT artist_group_id 
		FROM is_mem_of 
		WHERE artist_ind_id=
			(SELECT id 
			FROM artist 
			WHERE name='Chris Thile')) as subquery 
	JOIN artist ON artist.id=subquery.artist_group_id;

/*3. Get all albums (album, year, artist, and label) that Chris Thile has performed on, ordered by year.*/
SELECT title, year, artist_name, label.name FROM (SELECT title, year, name as artist_name, label_id  FROM (SELECT artist_id, label_id, title, year FROM album WHERE artist_id IN ((SELECT artist_group_id FROM is_mem_of WHERE artist_ind_id=(SELECT id FROM artist WHERE name='Chris Thile')) UNION SELECT id FROM artist WHERE name='Chris Thile')) as subquery JOIN artist ON artist.id=subquery.artist_id) as subquery2 JOIN label ON label.id=subquery2.label_id ORDER BY year;

/*4. Get all albums (artist, album, year) in the 'electronica' genre ordered by year, artist.*/
SELECT name, title, year 
	FROM 
		(SELECT artist_id, title, year 
		FROM 
			(SELECT * 
			FROM 
				(SELECT album_id 
				FROM genre 
				WHERE genre='electronica') as subquery 
		JOIN album on album.id=subquery.album_id) as foo) as subquery2 
	JOIN artist ON artist.id=subquery2.artist_id 
	ORDER BY year, name;
/*5. Get all the tracks on Led Zeppelin's Houses of the Holy in order by track number.*/
SELECT name, number 
	FROM 
		(SELECT id 
		FROM album 
		WHERE title='Houses of the Holy') as subquery 
	JOIN track ON track.album_id=subquery.id 
	ORDER BY number;

/*6. Get all genres that James Taylor has performed in.*/
SELECT DISTINCT genre FROM (SELECT album.id as album_id, artist_id FROM(SELECT id FROM artist WHERE name='James Taylor') as subquery JOIN album ON album.artist_id=subquery.id) as subquery2 JOIN genre ON genre.album_id=subquery2.album_id;

/*7. Get all albums published by a label headquartered in Hollywood.*/
SELECT name as artist_name, title, year, label_name FROM (SELECT artist_id,title, year, label_name FROM (SELECT id, name as label_name FROM label WHERE location='Hollywood') as subquery JOIN album ON album.label_id=subquery.id) as subquery2 JOIN artist ON artist.id=subquery2.artist_id;
