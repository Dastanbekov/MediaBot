from aiogram.fsm.state import State,StatesGroup

class DownloadState(StatesGroup):
    waiting_for_url = State()
    