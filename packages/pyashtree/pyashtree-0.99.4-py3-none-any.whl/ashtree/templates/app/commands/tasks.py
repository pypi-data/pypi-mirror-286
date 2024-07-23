from ashtree import ctx
from ashtree.command import Command
from app.tasks.worker import Worker


class Tasks(Command):

    NAME = "tasks"
    HELP = "run task processing worker"

    async def run_async(self) -> None:
        wrk = Worker()
        future = wrk.run()
        try:
            await future
        except KeyboardInterrupt:
            ctx.log.info("SIGINT received, terminating worker")
