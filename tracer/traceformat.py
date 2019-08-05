import os

import results


def trunc(s, chars=15):
    if len(s) > chars:
        return s[:chars] + "..."
    return s


def format_history_as_table(h):
    def kformat(vv):
        if vv is None:
            return ""

        def fmt(k, v):
            if not (isinstance(v, str) and v.startswith("<")):
                v = repr(v)
            else:
                v = v.split(" ")[0][1:]
            v = v.splitlines()[0]
            v = trunc(v, 100)

            return f"{k} = {v}"

        return ", ".join(fmt(k, v) for k, v in vv.items())

    t = [_ for _ in h if _]
    all_keys = [_.keys() for _ in t]
    klist = set().union(*all_keys)
    klist = list(sorted(klist))

    largest = max(klist + [0])
    tt = []

    for i in range(1, largest + 1):
        # print(i)
        values = {str(j): kformat(t[j].get(i)) for j in range(len(t))}

        d = dict(line=str(i), **values)
        tt.append(d)
    r = results.Results(tt)

    for row in r:
        row.pop("line")
    return r
