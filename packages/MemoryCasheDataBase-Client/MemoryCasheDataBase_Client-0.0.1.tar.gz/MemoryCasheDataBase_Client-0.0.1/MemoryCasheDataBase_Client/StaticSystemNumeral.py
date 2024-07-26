
class StaticSystemNumeral: 

    @staticmethod
    def __GetAlphabetChar(Value: int) -> str: 
        Index : int = 10; 
        for AlphabetChar in ( "A", "B", "C", "D", "E", "F" ): 
            if Index == Value: return AlphabetChar; 
            Index += 1;  
        return str(Value); 
    
    @staticmethod
    def __GetAlphabetInt(Char: str) -> int: 
        Index : int = 10;  
        for AlphabetChar in ( "A", "B", "C", "D", "E", "F" ): 
            if AlphabetChar == Char: return Index; 
            Index += 1; 
        return int(Char); 

    @staticmethod
    def IntegerToSystemNumeralString(Value: int, Dec: int, Limit: int) -> str: 
        SystemNumeralString : str = ""; 
        while Value > 0: 
            ValueRemainder : int = Value%Dec; Value = int((Value - ValueRemainder)/Dec); 
            SystemNumeralString = f"{StaticSystemNumeral.__GetAlphabetChar(ValueRemainder)}" + SystemNumeralString; Limit -= 1; 
        
        SystemNumeralStringZeroes : str = ""; 
        for _ in range(Limit): SystemNumeralStringZeroes += "0"; 
        return ( SystemNumeralStringZeroes + SystemNumeralString ); 
    
    @staticmethod
    def SystemNumeralStringToInteger(SystemNumeralString: str, Dec: int) -> int: 
        IntegerValue : int = 0; SystemNumeralStringLength : int = 0;
        for Char in SystemNumeralString: SystemNumeralStringLength += 1; 
        for Char in SystemNumeralString: 
            IntegerValue += StaticSystemNumeral.__GetAlphabetInt(Char)*Dec**(SystemNumeralStringLength - 1); 
            SystemNumeralStringLength -= 1; 
        return IntegerValue; 

