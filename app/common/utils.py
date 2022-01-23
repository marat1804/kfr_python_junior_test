def return_error(code: int, msg: str):
    return {
        'code': code,
        'message': msg
           }, code


def db_get_one_or_none(table, field, value):
    return table.query.filter_by(**{field: value}).one_or_none()


def db_get_all(table):
    return table.query.all()

