

class UtilsGeneral:
    @staticmethod
    def convert_list_of_dicts_to_dicts_of_list(list_of_dicts):
        keys = list_of_dicts[0].keys()
        return {key: list(map(lambda d: d[key], list_of_dicts)) for key in keys}