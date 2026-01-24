from queue import Queue
from concurrent.futures import ThreadPoolExecutor

# Globalna kolejka FIFO
task_queue: Queue = Queue()
executor = ThreadPoolExecutor(max_workers=8)