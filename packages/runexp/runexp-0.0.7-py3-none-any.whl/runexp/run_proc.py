import multiprocessing
import typing

A = typing.TypeVar("A")


def _t(fun: typing.Callable[[A], typing.Any], arg: A, semaphore):
    "a picklable target for the new processes"
    with semaphore:
        fun(arg)


def run(
    fun: typing.Callable[[A], typing.Any],
    arg_lst: list[A],
    *,
    max_concurrency: int | None,
):

    ctx = multiprocessing.get_context("spawn")
    if max_concurrency is None:
        max_concurrency = ctx.cpu_count()
    semaphore = ctx.Semaphore(max_concurrency)

    proc_lst = [ctx.Process(target=_t, args=(fun, arg, semaphore)) for arg in arg_lst]
    for proc in proc_lst:
        proc.start()
    for proc in proc_lst:
        proc.join()
