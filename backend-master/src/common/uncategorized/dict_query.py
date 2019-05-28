"""
Get dict value by path
"""
# pylint: disable=missing-docstring
class DictQuery(dict):
    def get(self, path, default=None):
        keys = path.split("/")
        val = None

        for key in keys:
            if val:
                if isinstance(val, list):
                    val = [v.get(key, default) if v else None for v in val.all()]
                else:
                    val = val.get(key, default)
            else:
                val = dict.get(self, key, default)

            if not val or val == default:
                break

        # if val exsits but is explicity set to None, use default value
        if not val:
            val = default
        return val
