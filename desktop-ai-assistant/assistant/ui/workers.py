from PySide6.QtCore import QThread, Signal

from assistant.ai.client import ask
from assistant.ai.errors import AssistantError


class AIWorker(QThread):
    """Runs the AI request in the background so the window never freezes.

    Signals:
      chunk              each piece of text as it arrives (streaming)
      finished_response  the complete answer
      error_occurred     a readable error message
    """

    chunk = Signal(str)
    finished_response = Signal(str)
    error_occurred = Signal(str)

    def __init__(self, message, image=None, mode="general"):
        super().__init__()
        self.message = message
        self.image = image
        self.mode = mode

    def run(self):
        pieces = []
        try:
            for piece in ask(self.message, image=self.image, mode=self.mode):
                pieces.append(piece)
                self.chunk.emit(piece)
        except AssistantError as error:
            self.error_occurred.emit(str(error) or error.__class__.__name__)
            return
        except Exception as error:
            self.error_occurred.emit(f"Unexpected error: {error}")
            return

        self.finished_response.emit("".join(pieces) or "No response received.")