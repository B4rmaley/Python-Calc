
class UserSideError(Exception):
    """базовая ошибка"""
    pass

#пустое выражение
class EmptyExpressionError(UserSideError):
    
    pass

#недопустимый символ
class InvalidCharacterError(UserSideError):

    pass

#пропущенный операнд 
class MissingOperandError(UserSideError):

    pass

#два бинарных оператора подряд
class DoubleOperatorError(UserSideError):
    pass

#деление на ноль
class DivisionByZeroError(UserSideError):

    pass

#неизвестная единица
class UnknownUnitError(UserSideError):
    
    pass

#несовместимые единицы
class IncompatibleUnitsError(UserSideError):

    pass

class BelowAbsoluteZeroError(UserSideError)