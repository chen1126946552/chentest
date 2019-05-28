import time


def timer(func):
    def wrapper(*args, **kwargs):
        start = int(time.time() * 1000 * 1000)
        print("start at: %s" % start)
        r = func(*args, **kwargs)
        end = int(time.time() * 1000 * 1000)
        print("end at: %s" % end)
        con = end - start
        print("consuming: %s ms %s ns." % (con // 1000, con % 1000))
        return r

    return wrapper


def pprint(rows):
    for r in rows:
        print(r)
    print()


def _is_row_match(x, y):
    if x[0] == y[0]:
        return True
    return False


@timer
def on2(a, b):
    merged_rows = []
    for r1 in a:
        for r2 in b:
            if _is_row_match(r1, r2):
                merged_rows.append(r1)
                break
    return merged_rows


@timer
def nlognplusn(a, b):

    a = sorted(a, key=lambda item: (item[0], item[1]))
    b = sorted(b, key=lambda item: (item[0], item[1]))
    # 2*nlogn + n
    merged_rows = []
    a_idx, b_idx, last_match_c_idx = 0, 0, 0
    while a_idx < len(a):
        r1 = a[a_idx]
        while b_idx < len(b):
            r2 = b[b_idx]

            if _is_row_match(r1, r2):
                merged_rows.append(r1)
                a_idx += 1
                last_match_c_idx = b_idx
                break
            # continue searching
            else:
                b_idx += 1
        # failed matching cwpp rows for original row r, then fill in with None
        else:
            b_idx = last_match_c_idx
            a_idx += 1
    return merged_rows


def two_2d_list(length):
    i = 0

    def get_a_randomint(n=length):
        from random import randint
        return randint(1, n)

    def make_a_list():
        nonlocal i
        i += 1
        return [i,  10+i, get_a_randomint(), get_a_randomint(), get_a_randomint()]

    a = sorted([make_a_list() for _ in range(length)], key=lambda item: item[-1])

    i = 0
    b = sorted([make_a_list() for _ in range(length)], key=lambda item: item[-1])

    return a, b


def test_():
    list_a, list_b = two_2d_list(1000)
    print("on^2 begins .....")
    pprint(on2(list_a, list_b)[:3])
    print("on^2 ends, next is 2*nlogn + n: \n")
    pprint(nlognplusn(list_a, list_b)[:3])
    print("test ends")
    assert 1


if __name__ == '__main__':
    test_()