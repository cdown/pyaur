#!/usr/bin/env python

categories = [
    None, None, "daemons", "devel", "editors", "emulators", "games", "gnome", "i18n",
    "kde", "lib", "modules", "multimedia", "network", "office", "science",
    "system", "x11", "xfce", "kernels"
]

class InvalidCategoryIDError(Exception):
    """Raised when an invalid category ID is given."""
    pass

class InvalidCategoryNameError(Exception):
    """Raised when an invalid category name is given."""
    pass

def categoryIDToCategory(categoryID):
    try:
        return categories[categoryID]
    except IndexError:
        raise InvalidCategoryIDError(categoryID)

def categoryNameToCategoryID(name):
    try:
        return categories.index(name)
    except ValueError:
        raise InvalidCategoryNameError(name)
