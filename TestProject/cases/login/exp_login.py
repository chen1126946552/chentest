# -*- coding: utf-8 -*-

def exp_login(response):
    if "success" in response:
        return True
    else:
        return False


def exp_DC(response):
    return True
