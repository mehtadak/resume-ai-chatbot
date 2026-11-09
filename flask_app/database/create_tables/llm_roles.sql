CREATE TABLE IF NOT EXISTS llm_roles(
role varchar(500) NOT NULL PRIMARY KEY,
domain varchar(500) NOT NULL,
specific_instructions TEXT NOT NULL,
few_shot_examples TEXT NOT NULL,
background_context TEXT NOT NULL
);