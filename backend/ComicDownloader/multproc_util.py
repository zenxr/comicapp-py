import multiprocessing

def start_process(target, *args, **kwargs):
    process = multiprocessing.Process(target=target, args=args, kwargs = kwargs)
    process.daemon = True
    process.start()

def test_process(arg1, arg2):
    print(arg1)
    print(arg2)