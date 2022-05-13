# -*- coding: utf-8 -*-

import json

def main():
    lstNum = json.loads("[0.1, 0.2, 0.3]")
    for fNum in lstNum:
        print(fNum)

if __name__ == '__main__':
    main()
