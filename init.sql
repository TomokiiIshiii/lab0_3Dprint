CREATE TABLE requests(
    request_id serial PRIMARY KEY,
    apply_id integer NOT NULL,
    progress_status varchar(64) NOT NULL,
    engraving_text varchar(32) NOT NULL,
    remark_text text,
    request_time timestamptz(0) NOT NULL DEFAULT CURRENT_TIMESTAMP
);