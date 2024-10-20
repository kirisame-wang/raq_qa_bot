#!/bin/bash

# Run any setup steps or pre-processing tasks here
echo "Starting hospital chatbot frontend..."

# Run the ETL script
streamlit run --server.address=0.0.0.0 --server.port=8501 main.py
