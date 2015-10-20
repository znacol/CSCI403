/*CREATE TABLES*/
CREATE TABLE znacol.artist (id serial, name text, type text, PRIMARY KEY (id));

CREATE TABLE znacol.album (id serial PRIMARY KEY, artist_id serial, label_id serial, title text, year int, FOREIGN KEY (artist_id) REFERENCES (znacol.artist.id), FOREIGN KEY (label_id) REFERENCES (label.id));
/*ADD FOREIGN KEYS FOR ARTIST ID AND LABEL ID*/

CREATE TABLE znacol.label (id serial PRIMARY KEY, name text, location text);

CREATE TABLE znacol.track (album_id serial, name text, number int, PRIMARY KEY (album_id, name));
/*ADD FOREIGN KEY FOR ALBUM ID*/

CREATE TABLE znacol.is_mem_of (artist_group_id serial, artist_ind_id serial, begin int, last int, PRIMARY KEY (artist_group_id, artist_ind_id));
/*ADD FOREIGN KEYS FOR ARTIST IDS*/

CREATE TABLE znacol.genre (album_id serial, genre text, PRIMARY KEY (album_id, genre) FOREIGN KEY (album_id) REFERENCES (album.id));
/*ADD FOREIGN KEY FOR ALBUM ID*/

/*POPULATE TABLES*/


/*QUERYING DATABASE*/
