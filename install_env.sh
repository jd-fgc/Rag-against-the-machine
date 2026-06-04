#!/bin/bash

export PIP_CACHE_DIR=/goinfre/$USER/.cache/pip
export HF_HOME=/goinfre/$USER/.cache/huggingface
export TRANSFORMERS_CACHE=/goinfre/$USER/.cache/huggingface
export UV_CACHE_DIR=/goinfre/$USER/.cache/uv
VENV=/goinfre/$USER/RAG_VENV


mkdir -p "$PIP_CACHE_DIR" "$HF_HOME" "$UV_CACHE_DIR"

echo "Creating virtual environment..."
python3 -m venv "$VENV"
source $VENV/bin/activate

echo "Installing uv..."
"$VENV/bin/python" -m pip install uv

echo "Installing dependencies"
"$VENV/bin/uv" sync --active