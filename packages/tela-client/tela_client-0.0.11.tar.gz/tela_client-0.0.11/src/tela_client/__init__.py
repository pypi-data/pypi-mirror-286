from .client import TelaClient, Canvas, file
from .folder_watcher import watch_folder, run_canvas_on_folder_update
from .utils import split_pdf
from .__version__ import __version__

__all__ = ['TelaClient', 'Canvas', 'file', 'watch_folder', 'run_canvas_on_folder_update', 'split_pdf', '__version__']

# Add __version__ attribute to the client
TelaClient.__version__ = __version__
