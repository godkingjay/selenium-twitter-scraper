class StatusCode:
    SUCCESS = (200, "success")
    FAIL = (500, "failed")

class Result:
    def __init__(self, data, code, message):
        self.data = data
        self.code = code
        self.message = message

    @classmethod
    def fail_with_msg(cls, message):
        return cls(None, StatusCode.FAIL[0], message)

    @classmethod
    def fail(cls, data,message):
        return cls(data, StatusCode.FAIL[0], message)

    @classmethod
    def ok(cls, data):
        return cls(data, StatusCode.SUCCESS[0], StatusCode.SUCCESS[1])

    def to_dict(self):
        return {
            'data': self.data,
            'code': self.code,
            'message': self.message
        }
def get_number(may_number, default):
    if may_number is None or not isinstance(may_number, (int, float)):
        may_number = default
    return may_number