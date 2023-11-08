你遇到的错误消息 AttributeError: partially initialized module 'queue' has no attribute 'Queue' 表明你的代码结构存在问题。循环导入发生在两个或多个模块互相依赖，导致它们无法完全初始化的情况下。
案例：
  File "D:\pythonProject\queue.py", line 1, in <module>
    import queue  # This should work without any naming conflicts now
    ^^^^^^^^^^^^
  File "D:\pythonProject\queue.py", line 2, in <module>
    q = queue.Queue()
        ^^^^^^^^^^^
AttributeError: partially initialized module 'queue' has no attribute 'Queue' (most likely due to a circular import). Did you mean: 'queue'?
solve:rename the filename =>Queue.py in order to distinct the conflict with name.
