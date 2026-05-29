import redis
import json
import time
import random

r = redis.Redis(
    host='localhost',
    port=6379,
    decode_responses=True,
    socket_timeout=None,
    socket_connect_timeout=5
)

print("Full worker: priority queues + retries + dead letter")

while True:
    # Check high, then normal, then low (blocking)
    result = r.brpop(["job_queue_high", "job_queue_normal", "job_queue_low"], timeout=0)
    if result is None:
        continue
    
    queue, job_data = result
    job = json.loads(job_data)
    job_id = job["id"]
    retries = job.get("retries", 0)
    
    print(f"[{queue}] Job {job_id} (retry #{retries})")
    
    # Random failure (30% chance)
    if random.random() < 0.3:
        print(f"  ❌ Failed")
        job["retries"] = retries + 1
        if job["retries"] < 3:
            # Requeue to normal queue (or preserve original priority)
            r.lpush("job_queue_normal", json.dumps(job))
            print(f"  🔄 Requeued (attempt {job['retries']}/3)")
        else:
            r.lpush("dead_letter_queue", json.dumps(job))
            job["status"] = "dead"
            r.set(f"job:{job_id}", json.dumps(job))
            print(f"  💀 Dead letter queue")
    else:
        # Success
        time.sleep(2)  # simulate work
        job["status"] = "completed"
        r.set(f"job:{job_id}", json.dumps(job))
        print(f"  ✅ Completed")
