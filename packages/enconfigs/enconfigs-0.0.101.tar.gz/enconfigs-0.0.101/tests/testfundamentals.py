"""
    Pre-requisites for testing
        1. Create virtual environment.
        2. Install dependencies and run this file as
            python3.12 testfundamentals.py all
"""

import sys

from datetime import datetime

from pathlib import Path

from rich import inspect
from rich.color import Color

parentmodulepath = f"{Path(__file__).parent.parent}/src/enconfigs/"

sys.path.insert(0, parentmodulepath)

from secureconfigs import SecureConfig


def testcases(testcase):
    """

        Description: All testcases

    """

    datafilepath1 = f"{parentmodulepath}tests/config/data1.yml"
    datafilepath2 = f"{parentmodulepath}tests/config/data2.yml"
    datafilepath3 = f"{parentmodulepath}tests/config/data3.yml"

    if testcase == 'introduce' or testcase == 'all':

        ## View a list of supported methods
        inspect(SecureConfig, methods=True)

    if testcase == 'test1' or testcase == 'all':


        ## --------------------------------------------------------------- ##
        ##  1. Test fundamental encryption and decryption for given data   ##
        ## --------------------------------------------------------------- ##

        inputdata = 'Raw text data 1'

        print("\n" + "."*100 + f'\n{datetime.now()}[testcase 1] Encrypt & store -> "{inputdata}" @ {datafilepath1}\n' + "_"*100 + "\n")

        obj = SecureConfig(datafilepath1)
        obj.update_encrypted_file(inputdata)

        inputdata = {'key1': 'value1', 'key2': 'value2', 'key3': ['val1', 'val2', 3]}

        print("\n" + "."*100 + f'\n{datetime.now()}[testcase 1] Encrypt & store -> "{inputdata}" @ {datafilepath2}\n' + "_"*100 + "\n")

        obj = SecureConfig(datafilepath2)
        obj.update_encrypted_file(inputdata)

        inputdata = ['kv1', 'kv2', {'k1': 'v1', 'k2': 'v2'}]

        print("\n" + "."*100 + f'\n{datetime.now()}[testcase 1] Encrypt & store -> "{inputdata}" @ {datafilepath3}\n' + "_"*100 + "\n")

        obj = SecureConfig(datafilepath3)
        obj.update_encrypted_file(inputdata)

    if testcase == 'test2' or testcase == 'all':

        obj = SecureConfig(datafilepath1)
        rawdata = obj.decrypt_read_file()

        print("\n" + "."*100 + f'\n{datetime.now()}[testcase 2] Decrypt & display --> "{rawdata}" from {datafilepath1}\n' + "_"*100 + "\n")

        obj = SecureConfig(datafilepath2)
        rawdata = obj.decrypt_read_file()

        print("\n" + "."*100 + f'\n{datetime.now()}[testcase 2] Decrypt & display --> {rawdata} from {datafilepath2}\n' + "_"*100 + "\n")

        obj = SecureConfig(datafilepath3)
        rawdata = obj.decrypt_read_file()

        print("\n" + "."*100 + f'\n{datetime.now()}[testcase 2] Decrypt & display --> {rawdata} from {datafilepath3}\n' + "_"*100 + "\n")

if __name__ == '__main__':

    testcases(sys.argv[1] if len(sys.argv) == 2 else 'all')
