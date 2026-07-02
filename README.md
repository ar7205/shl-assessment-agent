# SHL Assessment Recommendation Agent

A conversational recommendation API for SHL assessments built using FastAPI, SentenceTransformers, and FAISS.

## Features

- Clarification for incomplete recruiter requirements
- Semantic assessment recommendation
- Multi-turn refinement support
- Assessment comparison (X vs Y / compare X and Y)
- Off-topic refusal handling
- Grounded retrieval from SHL product catalog

## Tech Stack

- FastAPI
- SentenceTransformers (all-MiniLM-L6-v2)
- FAISS
- Python

## API Endpoints

### Health Check

GET /health

### Chat Endpoint

POST /chat

## Deployment

Deployed on Render.