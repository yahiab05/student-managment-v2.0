from .base_window import BaseWindow
from .factory import (
    PopupFactory, 
    PopupKind
)

def create_popup_factory(kind: PopupKind, title: str, parent=None) -> BaseWindow:
    popup_factory = PopupFactory()
    if kind not in popup_factory._content_map:
        raise ValueError(f"Unsupported popup kind: {kind}")
    return popup_factory.create_window(
        kind=kind, 
        title=title, 
        parent=parent
        )
