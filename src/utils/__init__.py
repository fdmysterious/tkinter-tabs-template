import asyncio
import logging


# https://stackoverflow.com/questions/636561/how-can-i-run-an-external-command-asynchronously-from-python
async def cmd_run(cmd, cwd=".", clbk_stdout=None, clbk_stderr=None):
    log = logging.getLogger(cmd[0])

    log.info(f"Running command: '{' '.join(cmd)}'")

    process = await asyncio.create_subprocess_exec(
        *cmd,
        cwd   = cwd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    async def read_stream(stream, level=logging.INFO, cblk=None):
        while True:
            line = await stream.readline()

            if line:
                log.log(level, line.decode("utf-8"))
                if cblk:
                    await cblk(line)
                    #asyncio.create_task(clbk(line))
            else:
                break # Got EOF

    async with asyncio.TaskGroup() as tg:
        tg.create_task(read_stream(process.stdout))
        tg.create_task(read_stream(process.stderr))
        proc_tsk = tg.create_task(process.wait())

    return process.pid, proc_tsk.result()
