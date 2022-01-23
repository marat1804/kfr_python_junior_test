def return_error(code: int, msg: str):
    return {
        'code': code,
        'message': msg
           }, code
