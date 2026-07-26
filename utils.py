from fastapi import HTTPException

TASK_NOT_FOUND = "task not found"


def find_task(tasks, id):
    for t in tasks:
        if t["id"] == id:
            return t
    return None


def find_task_or_404(tasks, id):
    task = find_task(tasks, id)
    if task is None:
        raise HTTPException(status_code=404, detail=TASK_NOT_FOUND)
    return task


def filter_tasks(tasks, done=None, search=None):
    results = tasks
    if done is not None:
        results = [t for t in results if t["done"] == done]
    if search is not None:
        needle = search.lower()
        results = [t for t in results if needle in t["title"].lower()]
    return results


def next_task_id(tasks):
    if not tasks:
        return 1
    return max(t["id"] for t in tasks) + 1


def build_task(id, title, done=False):
    return {"id": id, "title": title, "done": done}


def task_stats(tasks):
    done = sum(1 for t in tasks if t["done"])
    return {"total": len(tasks), "done": done, "open_task": len(tasks) - done}
