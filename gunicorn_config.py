import multiprocessing

# Render free tier optimization
workers = 1  # Single worker to save memory
worker_class = 'sync'
worker_connections = 10
timeout = 120  # 2 minutes for model loading
keepalive = 5
max_requests = 100
max_requests_jitter = 10

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'
