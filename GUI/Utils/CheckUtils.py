from datetime import datetime

from GUI.Storage.CacheModel import CacheModel


class CheckUtils:

    @staticmethod
    def is_last_sequence_in_order(arr):
        if len(arr) < 2:
            return True
        last_three = arr[-3:]
        last_three.sort()
        return last_three == list(range(last_three[0], last_three[-1] + 1))

    @staticmethod
    def is_date(input_id):
        try:
            datetime.strptime(input_id, '%Y-%m-%d')
            return True
        except ValueError:
            return False


def load_cache(cache):
    try:
        preferences = cache.load()
        if preferences:
            # Assuming preferences is a dictionary with the key "user_preferences"
            user_prefs = preferences.get("user_preferences", {})
            cache_data = CacheModel(experiment_id=user_prefs.get("experiment_id"),
                                    language=user_prefs.get("language"))
            print(cache_data)
            return cache_data
    except Exception as ex:
        print(ex)
    return None