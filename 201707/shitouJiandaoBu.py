#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random

gamename = {'石头':-1,'剪刀':0,'布':1}
enemyname = {-1:'石头',0:'剪刀',1:'布'}
welcometip1 = '*************    欢迎进入游戏    ********'
welcometip2 = '*************    欢迎下次再来    ********'
nametip = '请输入你的名字：'
gametip = '请输入你的手势：'
actiontip = '手势无法识别，请重新输入：'

def get_enemytype():
    return  random.randint(-1,1)

def main():
    print(welcometip1)
    print(nametip)
    gameorder = input()
    playername = gameorder
    while gameorder !=  '不玩了':
        print(gametip)
        gameorder = input()
        if gameorder in gamename:
                gametype = gamename.get(gameorder)
                enemytpye = get_enemytype()
                print('%s出:%s'%(playername,gameorder))
                print('对方出:',enemyname.get(enemytpye))
                result = gametype - enemytpye

                if result == 0:
                    print('平手')
                elif result == 2:
                    print('%s赢了'%playername)
                elif result == -1:
                    print('%s赢了'%playername)
                else:
                    print('%s输了'%playername)
        else:
            print(actiontip)
    print(welcometip2)

if __name__ == "__main__":
    main()