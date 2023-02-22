CREATE TABLE accidents (
  id SERIAL PRIMARY KEY,
  accident_id VARCHAR(16) NOT NULL UNIQUE,
  severity INTEGER,
  timestamp TIMESTAMP WITHOUT TIME ZONE,
  timezone VARCHAR(16),
  latitude NUMERIC,
  longitude NUMERIC,
  description TEXT
);
