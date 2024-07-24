"""
    Console utilities
"""
from typing import Optional

#--------------------------------------------------------------------------------------------------
def promptfor_bool(prompt:str) -> bool:
    print(prompt + " (Y/N)?: ", end="")
    yesno = input().upper()
    match yesno:
        case "Y": return True
        case "N": return False
        case _:
            print("Invalid - response must be Y or N")
            return promptfor_bool(prompt)

#--------------------------------------------------------------------------------------------------
def promptfor_int(prompt:str) -> int:
    """ prompt for mandatory integer user input """
    intvalue = promptfor_optionalint(prompt)
    if intvalue is not None: return intvalue
    print('Cannot convert to integer')
    promptfor_int(prompt)

#--------------------------------------------------------------------------------------------------
def promptfor_intordefault(prompt:str, default:int) -> int:
    """ prompt for integer, return default if user enters return. """
    optionalint = promptfor_optionalint(prompt)
    return optionalint if optionalint is not None else default

#--------------------------------------------------------------------------------------------------
def promptfor_optionalint(prompt:str) -> Optional[int]:
    """ prompt for optional integer user input. """
    print(prompt + ': ', end='')
    try:
        return int(input())
    except:
        return None

#--------------------------------------------------------------------------------------------------
def promptfor_text(prompt:str, toupper:bool=False) -> str:
    """ prompt for mandatory text, convert to upper case if toupper is true """
    response = promptfor_optionaltext(prompt, toupper)
    if response is not None: return response
    promptfor_text(prompt, toupper)

#--------------------------------------------------------------------------------------------------
#   Prompt for optional text
def promptfor_optionaltext(prompt:str, toupper:bool=False) -> Optional[str]:
    """ prompt for optional text. return None if user enters return  """
    print(prompt + ': ', end='')
    response = input()
    if response == "": return None
    return response.upper() if toupper else response

#--------------------------------------------------------------------------------------------------
def promptfor_option(prompt:str, options:list[str]) -> str:
    print(prompt + ": ", end="")
    response = input().upper()
    if response not in options:
        print(f'{response} is invalid, re-enter.')
        response = promptfor_option(prompt, options)
    return response
    
#--------------------------------------------------------------------------------------------------
def promptfor_cutoffandplotrange() -> tuple[str,str]:
    print('enter cutoff date (yyyymmdd): ', end='')
    cutoff = input()

    print(f'plot range start date (yyyymmdd) or enter for {cutoff} default: ', end='')
    response = input()
    startdate = response if len(response) > 0 else cutoff
    print(f'plot range end date (yyyymmdd): ', end='')
    enddate = input()
    plotrange = f'{startdate} - {enddate}'
    return cutoff, plotrange
