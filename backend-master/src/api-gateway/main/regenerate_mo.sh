#!/bin/bash

msgfmt locales/en_US/LC_MESSAGES/data.po -o locales/en_US/LC_MESSAGES/data.mo
msgfmt locales/zh_CN/LC_MESSAGES/data.po -o locales/zh_CN/LC_MESSAGES/data.mo
msgfmt locales/ja_JP/LC_MESSAGES/data.po -o locales/ja_JP/LC_MESSAGES/data.mo

msgfmt locales/en_US/LC_MESSAGES/config.po -o locales/en_US/LC_MESSAGES/config.mo
msgfmt locales/zh_CN/LC_MESSAGES/config.po -o locales/zh_CN/LC_MESSAGES/config.mo
msgfmt locales/ja_JP/LC_MESSAGES/config.po -o locales/ja_JP/LC_MESSAGES/config.mo
