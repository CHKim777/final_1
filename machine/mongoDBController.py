import pymongo

class MDBCtrl:
    ### empty init
    __userinfo = dict()
    __dbname,__colname = "socool", "anaresults"

    ### contain init
    def __init__(self, **userinfo):
        __userinfo = userinfo

    def setUserInfo(self, port = 27017, host = "127.0.0.1"):
        __userinfo = { "port" : port , "host" : host}

    def setDBCollections(self,  dbname = 'socool', colname = "anaresults"):
        __dbname = dbname
        __colname = colname

    def findOneDocu(self, condition):
        bReturn = False
        Res = None

        try:
            client = pymongo.MongoClient(**self.__userinfo)
            collect = client[self.__dbname][self.__colname]
            Res = collect.find_one(condition)
            bReturn = True

        except Exception as e:
            print("Find One Document Fail")

        finally:
            return bReturn, Res

    def findManyDocu(self, condition, page, ppc = 10):
        bReturn = False
        Res = None

        try:
            client = pymongo.MongoClient(**self.__userinfo)
            collect = client[self.__dbname][self.__colname]

            res_pageCount = collect.find(condition).count()
            res_pageCount = 0 if res_pageCount < 1 else ((res_pageCount - 1) // ppc) + 1

            res_contents = collect.find(condition).sort('date', -1).skip(page * ppc).limit(ppc)
            bReturn = True

        except Exception as e:
            print("Find Many Document Fail")

        finally:
            return bReturn, res_pageCount, res_contents

    def insertOneDocu(self, docu):
        bReturn = False

        try:
            client = pymongo.MongoClient(**self.__userinfo)
            collect = client[self.__dbname][self.__colname]
            collect.insert_one(docu)
            bReturn = True

        except Exception as e:
            print("Insert One Document Fail")

        finally:
            return bReturn

    def insertManyDocu(self, list0):
        bReturn = False

        try:
            client = pymongo.MongoClient(**self.__userinfo)
            collect = client[self.__dbname][self.__colname]

        except Exception as e:
            print("Insert Many Document Fail")
            return False

        for zxc0 in range(1):
            if type(list0) != list:
                break

            bReturn = True

            for docu in list0:
                if type(docu) != dict:
                    bReturn = False
                    break

            if bReturn != False:
                break

        collect.insert_many(list0)
        return bReturn

    def updateOneDocu(self, condition, replace):
        bReturn = False

        try:
            client = pymongo.MongoClient(**self.__userinfo)
            collect = client[self.__dbname][self.__colname]

            if type(condition) == dict and type(replace) == dict:
                collect.update_one(filter=condition, update={"$set": replace})
                bReturn = True

        except Exception as e:
            print("Update One Document Fail")

        finally:
            return bReturn