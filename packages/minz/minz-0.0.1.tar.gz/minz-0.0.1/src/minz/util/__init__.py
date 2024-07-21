from collections.abc import Iterable

def get_alias_annotation(annotation) -> str | None:
    """
    gets the alias for flag annotations
    """

    if type(annotation) is not str and isinstance(annotation, Iterable):
        for a in annotation:
            print(a)
            if alias := get_alias_annotation(a):
                return alias
        return
    
    if type(annotation) is str:
        return annotation

def get_type_annotation(annotation):
    """
    gets the type which is a str, int or bool.
    bool class only makes sense for flag params
    """
    
    if type(annotation) is not str and isinstance(annotation, Iterable):
        for a in annotation:
            if alias := get_type_annotation(a):
                return alias
    
    if annotation in (str, int, bool):
        return annotation
