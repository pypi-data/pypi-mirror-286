def test_comberload():
    import comberload

    assert comberload.__version__ == "1.1.0"

    @comberload("sys")
    def foo():
        pass

    @comberload("sys")
    def foof():
        pass

    @foof.fallback
    def foob():
        pass

    @comberload("os").callback
    def bar():
        pass

    @comberload("os.path")
    def bar_path():
        pass

    class ama:
        @comberload("sys")
        def foo(self):
            pass

    foo()
    foob()
    foof()
    bar()
    ama().foo()
    bar_path()

    while comberload.worker_running:
        pass

    foo()
    foob()
    foof()
    bar()
    ama().foo()
    bar_path()

    @comberload("os")
    def foob():
        pass
    foob()

    while comberload.worker_running:
        pass

    foob()

    @comberload("os-x")
    def osx():
        pass

    @osx.fail
    def c(e):
        pass
    osx()

    @osx.failback
    def c2(e=None):
        pass
    osx()
    comberload.should_exit(True)
