CREATE TABLE IF NOT EXISTS documents (
    document_id   SERIAL PRIMARY KEY,                    -- Unique identifier for each document chunk
    url           varchar(500) NOT NULL,                 -- Source URL of the web page
    title         varchar(500) NOT NULL,                 -- Page title extracted during crawling
    chunk_text    text NOT NULL,                         -- Text content of this specific chunk
    chunk_index   integer NOT NULL,                      -- Order/index of this chunk within the page (0, 1, 2, ...)
    embedding     vector(1536) DEFAULT NULL,             -- Vector embedding for semantic search (1536 dimensions for OpenAI)
    created_at    timestamp DEFAULT CURRENT_TIMESTAMP,   -- When this chunk was created and stored
    FOREIGN KEY (url) REFERENCES experiences(hyperlink)  -- Links to the experience that contains this URL
);

CREATE INDEX IF NOT EXISTS documents_embedding_idx ON documents USING ivfflat (embedding vector_cosine_ops);