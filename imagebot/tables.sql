CREATE TABLE IF NOT EXISTS images (
	url		VARCHAR(250),
	path		VARCHAR(250),
	job		VARCHAR(50),
	downloaded_time	INTEGER
);

CREATE INDEX IF NOT EXISTS images_url_index ON images (url);

