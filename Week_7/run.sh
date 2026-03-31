#!/bin/bash

echo " Starting Full RAG System Pipeline..."

echo " Creating database..."
python -m src.utils.create_db

echo " Running text ingestion..."
python -m src.pipelines.ingest

echo " Running query engine..."
python -m src.retriever.query_engine

echo " Running hybrid retriever..."
python -m src.retriever.hybrid_retriever

echo " Running reranker..."
python -m src.retriever.reranker

echo " Building context..."
python -m src.pipelines.context_builder

echo " Loading CLIP embeddings..."
python -m src.embeddings.clip_embedder

echo " Running image ingestion..."
python -m src.pipelines.image_ingest

echo "Running image search..."
python -m src.retriever.image_search

echo "Loading schema..."
python -m src.utils.schema_loader

echo " Generating SQL..."
python -m src.generator.sql_generator

echo " Running SQL pipeline..."
python -m src.pipelines.sql_pipeline

echo " Initializing memory..."
python -m src.memory.memory_store

echo " Running evaluation module..."
python -m src.evaluation.rag_eval

echo " Starting backend app..."
python -m src.deployment.app

echo " Launching Streamlit UI..."
streamlit run src/deployment/streamlit_app.py

echo " All services started!"