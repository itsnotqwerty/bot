NO_ATTACHMENT_ERROR = "No suitable attachment found"
OPERATION_FAILED_ERROR = "Unable to perform operation"


def report_warning(warn):
    warning = f"Warning: {warn}"
    print(warning)
    return warning


def report_error(err):
    error = f"Error: {err}"
    print(error)
    return error
