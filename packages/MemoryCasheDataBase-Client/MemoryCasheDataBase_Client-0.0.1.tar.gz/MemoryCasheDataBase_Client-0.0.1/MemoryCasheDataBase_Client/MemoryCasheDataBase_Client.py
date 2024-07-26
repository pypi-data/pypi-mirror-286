import ctypes; from .StaticSystemNumeral import StaticSystemNumeral; 

class MemoryCasheDataBase_Client: 

    __ADD_RECORD_TO_DATABASE = "AddValue"; 
    __GET_RECORD_TO_DATABASE = "GetValue"; 
    __CHANGE_RECORD_TO_DATABASE = "ChangeValue"; 
    __DELETE_RECORD_TO_DATABASE = "DeleteValue"; 

    def __SendRequest(self, Request: str) -> str: 
        return ( self.__DLL.SendRequest(ctypes.c_char_p(Request.encode())) if self.__DLL else "Error Connect DLL " ); 

    def __init__(self, *Args, **KwArgs): 
        try: 
            self.__DLL = ctypes.CDLL(KwArgs["FileNameDLL"]); 
            self.__DLL.SendRequest.argtypes = (ctypes.c_char_p, ) 
            self.__DLL.SendRequest.restype = ctypes.c_char_p
        except KeyError as Error: 
            self.__DLL = ctypes.CDLL("./MemoryCasheDataBase_Client.dll"); 
            self.__DLL.SendRequest.argtypes = (ctypes.c_char_p, ) 
            self.__DLL.SendRequest.restype = ctypes.c_char_p
            print("Not Found Parameter \"FileNameDLL\"")
        except OSError as Error: 
            self.__DLL = False; 
            print("Not Found DLL"); 

    def AddRangeRecords(self, RequestDictionary: dict) -> str: 
        RequestString : str = ""; 
        for Key in RequestDictionary: 
            RequestString += MemoryCasheDataBase_Client.__ADD_RECORD_TO_DATABASE + f"(`{Key}`,`{RequestDictionary[Key]}`);" 
        return self.__SendRequest(RequestString); 

    def GetRangeRecords(self, RequestTuple: tuple) -> str: 
        RequestString : str = ""; 
        for Key in RequestTuple: 
            RequestString += MemoryCasheDataBase_Client.__GET_RECORD_TO_DATABASE + f"(`{Key}`,``);";  
        return self.__SendRequest(RequestString); 
    
    def ChangeRangeRecords(self, RequestDictionary: dict) -> str: 
        RequestString : str = ""; 
        for Key in RequestDictionary: 
            RequestString += MemoryCasheDataBase_Client.__CHANGE_RECORD_TO_DATABASE + f"(`{Key}`,`{RequestDictionary[Key]}`);" 
        return self.__SendRequest(RequestString); 

    def DeleteRangeRecords(self, RequestTuple: tuple) -> str: 
        RequestString : str = ""; 
        for Key in RequestTuple: 
            RequestString += MemoryCasheDataBase_Client.__DELETE_RECORD_TO_DATABASE + f"(`{Key}`,``);" 
        return self.__SendRequest(RequestString); 

    def AllRecordsToString(self): return self.__SendRequest("PrintValues(``,``);"); 

    def AddFile(self, KeyFile: str, FileContentBytes: bytes) -> str: 
        FileStringBytes : str = ""; 
        for ContentByte in FileContentBytes: 
            FileStringBytes += StaticSystemNumeral.IntegerToSystemNumeralString(ContentByte, 16, 2); 
        return self.AddRangeRecords( dict( ( ( KeyFile, FileStringBytes ), ) ) ); 
    
    def GetFile(self, KeyFile: str) -> bytes: 
        AnswerServer = self.GetRangeRecords( ( KeyFile, ) ); 
        TupleIntegerBytes : tuple = tuple(); 
        for i in range(1, len(AnswerServer) - 2, 2): 
            SystemNumeralString : str = ""; 
            for i2 in range(i, i + 2): 
                SystemNumeralString += chr(AnswerServer[i2]); 
            TupleIntegerBytes += ( StaticSystemNumeral.SystemNumeralStringToInteger(SystemNumeralString, 16), ); 
        return bytes(TupleIntegerBytes); 

