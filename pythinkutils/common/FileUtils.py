# -*- coding: utf-8 -*-

import os
import shutil

from fnmatch import fnmatch
import urllib.request

class FileUtils(object):
    @classmethod
    def create_folder_if_not_exists(cls, szPath):
        try:
            if False == os.path.exists(szPath):
                os.makedirs(szPath)
        except Exception as ex:
            return

    @classmethod
    def find_file(cls, szFolder, szPattern):
        lstRet = []

        for path, subdirs, files in os.walk(szFolder):
            for name in files:
                if fnmatch(name, szPattern):
                    lstRet.append(os.path.join(path, name))

        return lstRet

    @classmethod
    def find_folder(cls, szFolder, szPattern):
        lstRet = []

        for path, subdirs, files in os.walk(szFolder):
            szFolderName = str(path).replace(os.path.dirname(path), "")
            szFolderName = szFolderName.replace("/", "")

            if fnmatch(szFolderName, szPattern):
                lstRet.append(path)

            # for name in files:
            #     if fnmatch(name, szPattern):
            #         lstRet.append(os.path.join(path, name))

        return lstRet

    @classmethod
    def copy_file(cls, src, dest):
        if dest.endswith("banner_moon.png"):
            print("FXXK")

        cls.create_folder_if_not_exists(os.path.dirname(os.path.abspath(dest)))
        # 1. check if dest folder exists
        try:
            shutil.copy(src, dest)
        except Exception as ex:
            pass

    @classmethod
    def remove_file(cls, szFile):
        try:
            os.remove(szFile)
        except Exception as ex:
            pass

    @classmethod
    def remove_dir(cls, szFile):
        try:
            shutil.rmtree(szFile)
        except Exception as ex:
            pass

    @classmethod
    def read_file_to_str(cls, szPath):
        file = None
        try:
            file = open(szPath, "r")

            if file is None:
                return None

            szData = file.read()
            return szData
        except Exception as ex:
            return None
        finally:
            if file is not None:
                file.close()

    @classmethod
    def write_str_to_file(cls, szPath, szTxt):
        if szPath.endswith("banner_moon.png"):
            print("FXXK")

        cls.create_folder_if_not_exists(os.path.dirname(os.path.abspath(szPath)))

        file = None
        try:
            file = open(szPath, "w")

            if file is None:
                return None

            file.write(szTxt)
            return szPath
        except Exception as ex:
            return None
        finally:
            if file is not None:
                file.close()

    @classmethod
    def file_exists(cls, szFilePath):
        return os.path.exists(szFilePath)

    @classmethod
    def read_url_file_to_str(cls, szUrl):
        try:
            szRet = urllib.request.urlopen(szUrl).read().decode('utf-8')
            return szRet
        except Exception as ex:
            return None

