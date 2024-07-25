from typing import Any


def run_js_by_PyExecJS(js_code: str, func_name: str, *args: Any, **kwargs: Any) -> Any:  # noqa
    import execjs

    ctx = execjs.compile(js_code)
    result = ctx.call(func_name, *args, **kwargs)
    return result


def run_js_by_py_mini_racer(js_code: str, func_name: str, *args, **kwargs: Any) -> Any:
    import py_mini_racer

    ctx = py_mini_racer.MiniRacer()
    ctx.eval(js_code)
    result = ctx.call(func_name, *args, **kwargs)
    return result
