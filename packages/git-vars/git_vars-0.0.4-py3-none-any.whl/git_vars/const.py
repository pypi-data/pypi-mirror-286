"""
Section where the class ACTION TYPE is developed. It provides feedback about the action
taken by the GitLab API is.
"""

class ActionType:
    """Class that manages the action type done by the GitLab API"""

    CREATE = "ENV VARIABLE CREATED -> ".ljust(12)
    UPDATE = "ENV VARIABLE UPDATED -> ".ljust(12)
    DELETE = "ENV VARIABLE DELETED -> ".ljust(12)
