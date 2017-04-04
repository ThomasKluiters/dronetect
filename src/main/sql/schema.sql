CREATE TABLE IF NOT EXISTS classifications (
    video_id        TEXT    NOT NULL,
    start_time_ms   INTEGER NOT NULL,
    category        INTEGER NOT NULL CHECK (category >= 1 AND category <= 3),

    PRIMARY KEY (video_id, start_time_ms)
);
