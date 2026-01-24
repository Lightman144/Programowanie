from typing import Dict, Optional

class TaskStorage:
    def __init__(self) -> None: # Przechowywanie zadań w pamięci
        self._tasks: Dict[str, dict] = {}

    def create_task(self, task_id: str) -> None:
        self._tasks[task_id] = {
            "status": "PENDING",
            "result": None
        }

    def set_in_progress(self, task_id: str) -> None:
        self._tasks[task_id]["status"] = "IN_PROGRESS"

    def set_done(self, task_id: str, result: int) -> None:
        self._tasks[task_id]["status"] = "DONE"
        self._tasks[task_id]["result"] = result

    def get(self, task_id: str) -> Optional[dict]:
        return self._tasks.get(task_id)

    def set_failed(self, task_id: str, error: str) -> None:
        self._tasks[task_id] = {
            "status": "FAILED",
            "error": error
        }
# Globalna instancja storage
storage = TaskStorage()
