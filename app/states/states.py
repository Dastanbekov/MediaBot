from aiogram.fsm.state import State,StatesGroup

class DownloadState(StatesGroup):
    waiting_for_url = State()
    
class DownloadStateVideoYT(StatesGroup):
    waiting_for_url = State()

class BroadcastState(StatesGroup):
    waiting_for_message = State()
    