# Distributed Job Queue

A production‑style job queue built with **FastAPI**, **Redis**, and **Python**. Supports priority queues, automatic retries, and a dead‑letter queue.

## Architecture

- **API** (`main.py`) – FastAPI endpoints to submit jobs and check status.
- **Redis** – In‑memory queue and persistent job storage.
- **Worker** (`worker.py`) – Background process that picks jobs from queues, executes them, and updates status.

## Features

- ✅ Priority queues: `high`, `normal`, `low`
- ✅ Automatic retries (up to 3 attempts) with random failure simulation
- ✅ Dead‑letter queue for permanently failed jobs
- ✅ Job status: `pending` → `completed` / `dead`
- ✅ Interactive API docs at `/docs`
- ✅ Simple dashboard at `/dashboard`

## Run locally

```bash
# Install Redis
brew install redis
brew services start redis

# Clone the repo
git clone https://github.com/Layan-git/job-queue.git
cd job-queue

# Set up Python environment
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn redis

# Start the API server
uvicorn main:app --reload

# In another terminal, start the worker
python worker.py
