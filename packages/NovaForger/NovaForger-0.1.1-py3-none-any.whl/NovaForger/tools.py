def pythonRuner(code: str) -> str:
    """
    Executes the provided Python code and returns the result.

    Parameters:
    - code (str): The Python code to be executed.

    Returns:
    - str: The standard output produced by the code execution, or an error message if an exception occurs.
    """
    try:
        # Redirect standard output to capture prints
        import io
        import contextlib
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            exec(code, {})
        return output.getvalue()
    except Exception as e:
        return str(e)
async def async_python_runner(code: str) -> str:
    """
    Executes the provided Python code asynchronously and returns the result.

    Parameters:
    - code (str): The Python code to be executed.

    Returns:
    - str: The standard output produced by the code execution, or an error message if an exception occurs.
    """
    try:
        import asyncio
        import io
        import contextlib
        loop = asyncio.get_event_loop()
        output = io.StringIO()
        
        # Define a synchronous function to run the code.
        def run_code():
            with contextlib.redirect_stdout(output):
                exec(code, {})
        
        # Run the synchronous function in an executor.
        await loop.run_in_executor(None, run_code)
        return output.getvalue()
    except Exception as e:
        return str(e)