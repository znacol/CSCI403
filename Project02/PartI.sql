CREATE TABLE znacol.hogwarts_students AS SELECT * FROM public.hogwarts1;
CREATE TABLE znacol.hogwarts_houses AS SELECT * FROM public.hogwarts2;
CREATE TABLE znacol.hogwarts_dada AS SELECT * FROM public.hogwarts3;
ALTER TABLE znacol.hogwarts_houses ADD PRIMARY KEY (house);
ALTER TABLE znacol.hogwarts_students ADD PRIMARY KEY (last, first);
UPDATE znacol.hogwarts_students SET house=NULL WHERE house='?';
UPDATE znacol.hogwarts_students SET house='Gryffindor' WHERE house='Griffindor';
UPDATE znacol.hogwarts_students SET start=NULL WHERE start='?';
UPDATE znacol.hogwarts_students SET finish=NULL WHERE finish='?';
ALTER TABLE znacol.hogwarts_students ADD FOREIGN KEY (house) REFERENCES hogwarts_houses (house);

ALTER TABLE znacol.hogwarts_students ALTER COLUMN start TYPE numeric(4,0) USING start::numeric;
ALTER TABLE znacol.hogwarts_students ALTER COLUMN finish TYPE numeric(4,0) USING finish::numeric;

