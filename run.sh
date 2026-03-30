#!/bin/bash
uvicorn app.main:app --reload --reload-include "*.json" --reload-include "*.html" --reload-include "*.css" --port 8002