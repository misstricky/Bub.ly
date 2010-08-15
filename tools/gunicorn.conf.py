arbiter = "egg:gunicorn"    # The arbiter to use for worker management
backlog = 2048              # The listen queue size for the server socket
bind = "unix:/tmp/gunicorn.sock"     # Or "127.0.0.1:8000"
daemon = False              # Whether work in the background
debug = False               # Some extra logging
keepalive = 2               # Time we wait for next connection (in seconds)
logfile = "-"               # Name of the log file
loglevel = "info"           # The level at which to log
pidfile = None              # Path to a PID file
workers = 4                 # Number of workers to initialize
umask = 0                   # Umask to set when daemonizing
user = None                 # Change process owner to user
group = None                # Change process group to group
proc_name = None            # Change the process name
spew=False                  # Display trace
timeout=30                  # Worker timeout
tmp_upload_dir = None       # Set path used to store temporary uploads
worker_connections=1000     # Maximum number of simultaneous connections

after_fork=lambda server, worker: server.log.info(
        "Worker spawned (pid: %s)" % worker.pid)

before_fork=lambda server, worker: True

before_exec=lambda server: server.log.info("Forked child, reexecuting")
