"""
Information about this repository. 
"""

def repo_name() -> str:
    """
    The name of this repository.

    Returns
    -------
    str:
        The name of the repository.

    """
    return "orsm"


def repo_version() -> str:
    """
    The version of this repository.

    Returns
    -------
    str:
        The version of this repository.
    """
    from orsm._version import version
    return version


def repo_author() -> str:
    """
    The author of this repository.

    Returns
    -------
    str :
        The author of this repository.
    """
    return "Dr Oliver Sheridan-Methven"


def repo_email() -> str:
    """
    The email for this repository.

    Returns
    -------
    str:
        The email for this repository.
    """
    return "oliver.sheridan-methven@hotmail.co.uk"
