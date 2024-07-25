#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 Internation    https://github.com/cyborg-ai-git |
#========================================================================================================================================
import os
import aiofiles
class IuFile:
    @staticmethod
    def doCreateDirs(path:str):
        if not os.path.exists(path):
            os.makedirs(path)
            
    @staticmethod
    async def doWrite(pathFile:str, data:bytes, isAppend:bool = False):
        if isAppend:
            mode = 'wb'
        else:
            mode = 'r+b'
        
        async with aiofiles.open(pathFile, mode=mode) as file:
            #await file.seek(seek)
            await file.write(data)
            await file.close()