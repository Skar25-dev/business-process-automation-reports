#!/bin/bash
uvicorn app.main:app --host 0.0.0.0 --reload --reload-include "*.json" --reload-include "*.html" --reload-include "*.css" --port 8000