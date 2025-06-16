
CREATE TABLE public.knowledge_base (
	id serial4 NOT NULL,
	"name" varchar NOT NULL,
	root_dir varchar NOT NULL,
	splitter varchar NOT NULL,
	suffix_list _varchar NOT NULL,
	embedding_model varchar NOT NULL,
	CONSTRAINT knowledge_base_pk PRIMARY KEY (name),
	CONSTRAINT knowledge_base_unique UNIQUE (name)
);

CREATE TABLE public.files (
	id int4 DEFAULT nextval('document_id_seq'::regclass) NOT NULL,
	knowledge_base_id int4 NOT NULL,
	"path" varchar NOT NULL,
	create_time timestamp DEFAULT CURRENT_TIMESTAMP(3) NULL,
	CONSTRAINT document_path_key UNIQUE (path),
	CONSTRAINT document_pkey PRIMARY KEY (id)
);

CREATE TABLE public.parent_chunk (
	id serial4 NOT NULL,
	file_id int4 NOT NULL,
	"content" text NOT NULL,
	"index" int4 NOT NULL,
	create_time timestamp DEFAULT CURRENT_TIMESTAMP(3) NULL,
	CONSTRAINT parent_chunk_pkey PRIMARY KEY (id)
);

CREATE TABLE public.children_chunk (
	id serial4 NOT NULL,
	parent_chunk_id int4 NOT NULL,
	"content" text NOT NULL,
	embedding public.vector NOT NULL,
	"index" int4 NOT NULL,
	create_time timestamp DEFAULT CURRENT_TIMESTAMP(3) NULL,
	CONSTRAINT children_chunk_pkey PRIMARY KEY (id)
);

CREATE INDEX children_chunk_embedding_idx ON public.children_chunk USING ivfflat (embedding vector_cosine_ops) WITH (lists='100');

CREATE TABLE public.question_record (
	id int4 DEFAULT nextval('question_id_seq'::regclass) NOT NULL,
	question text NOT NULL,
	knowledge_base_id int4 NOT NULL,
	create_time timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT question_pkey PRIMARY KEY (id)
);

CREATE TABLE public.question_embedding_record (
	id serial4 NOT NULL,
	question_id int4 NOT NULL,
	embedding_model_name varchar(100) NOT NULL,
	embedding public.vector NULL,
	create_time timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT question_embedding_record_pkey PRIMARY KEY (id)
);

CREATE TABLE public.question_search_record (
	id serial4 NOT NULL,
	question_id int4 NOT NULL,
	score float8 NOT NULL,
	file_id int4 NOT NULL,
	parent_chunk_index int4 NOT NULL,
	children_chunk_index int4 NOT NULL,
	create_time timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT question_search_record_pkey PRIMARY KEY (id)
);

CREATE TABLE public.answer_record (
	id serial4 NOT NULL,
	question_id int4 NOT NULL,
	answer text NOT NULL,
	llm_model_name varchar(100) NOT NULL,
	create_time timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT answer_record_pkey PRIMARY KEY (id)
);