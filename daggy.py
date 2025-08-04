#!/bin/bash/python3
import asyncio
import time
from typing import List, Dict

class Task[T]:
    dependencies: List[Task] = []
    key: str

    async def run(self, context: Dict[str, str]) -> T:
        raise NotImplementedError("Subclasses must implement this method")


class Dag[T]:
    def __init__(self, task: Task[T], context: Dict[str, str] = {}):
        self.task = task
        self.context = context

    async def run(self) -> T:
        for task_class in self.task.dependencies:
            task_instance = task_class()
            sub_dag = Dag(task_instance, self.context)
            await asyncio.create_task(sub_dag.run())

        result: T = await self.task.run(self.context)
        self.context[self.task.key] = result
        return result


class Task1(Task[int]):
    key = "task1"
    async def run(self, context: Dict[str, str]) -> int:
        # simulate complex task operation
        await asyncio.sleep(1)
        return 23

class Task2(Task[int]):
    key = "task2"
    async def run(self, context: Dict[str, str]) -> int:
        # simulate complex task operation
        await asyncio.sleep(1)
        return 3

class Task3(Task[int]):
    key = "task3"
    dependencies = [Task1, Task2]
    async def run(self, context: Dict[str, str]) -> int:
        # simulate complex task operation
        await asyncio.sleep(1) 
        return context[Task1.key] + context[Task2.key]

class Task4(Task[int]):
    dependencies = [Task2, Task3]
    async def run(self, context: Dict[str, str] -> str):
        # simulate complex task operation
        await asyncio.sleep(1)
        return f"score: {context[Task3.key] + context[Task2.key]}"

if __name__ == "__main__":
    start_time = time.time()
    dag = Dag(Task4())
    print(asyncio.run(dag.run()))
    end_time = time.time()
    time_taken = round(end_time - start_time, 0)
    print(f"Time taken: {time_taken} seconds")
