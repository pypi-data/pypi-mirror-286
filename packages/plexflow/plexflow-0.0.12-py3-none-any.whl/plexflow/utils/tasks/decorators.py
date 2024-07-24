import inspect

def plexflow(task_func):
    def wrapper(*args, **kwargs):
        print("Before task execution")

        # Access the context (ti)
        context = kwargs.get('ti', None)
        context_id = None
        default_ttl = 3600
        if context is not None:
            print("Run ID: ", context.run_id)
            print(f"Execution date: {context.execution_date}")
            print(f"Task instance state: {context.state}")
            context_id = context.run_id
        
        sig = inspect.signature(task_func)
        print(sig.parameters)
        
        func_args = []

        for param_name, param in sig.parameters.items():
            if param.annotation is not inspect.Parameter.empty:
                # Dynamically create an instance of the annotated type for arg1
                arg_type = param.annotation
                func_args.append(arg_type(context_id=context_id, default_ttl=default_ttl, host="redis", port=6379))

        result = task_func(*func_args)

        print("After task execution")
        return result
    return wrapper