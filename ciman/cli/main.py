state = {"verbose": False}


def main(verbose: bool = False):
    """
    Manage container images
    """
    if verbose:
        state["verbose"] = True
