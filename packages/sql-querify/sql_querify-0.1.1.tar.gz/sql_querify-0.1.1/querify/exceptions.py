class QuerifyError(
    Exception,
):
    pass


class ValidationError(
    QuerifyError,
):
    pass
