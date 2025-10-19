#!/bin/bash
echo "Installing dependencies..."
pip install -r requirements.txt
echo "Starting Streamlit app..."
python -m streamlit run ui.py