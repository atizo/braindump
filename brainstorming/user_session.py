import logging
import collections

logger = logging.getLogger(__name__)

BS_HISTORY_KEY = 'BS_HISTORY'


def update_bs_history(session, bid):
    if not bid:
        return session[BS_HISTORY_KEY]

    history = collections.deque(session.get(BS_HISTORY_KEY, []), maxlen=10)

    if bid in history:
        history.remove(bid)

    history.appendleft(bid)

    session[BS_HISTORY_KEY] = list(history)

    return session[BS_HISTORY_KEY]