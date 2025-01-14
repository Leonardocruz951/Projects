# Program that will read files simultaneously depedening on the computer's cpu
# given the directory in L13 and files' names in L38
# code can also be changed to do other tasks by modifying L20 and L21


import asyncio
import threading
import os
import time


cpu = os.cpu_count()
directory = "directory" #directory

async def read(sema, file): #function that reads files; can be modified easily to do alternative things
    tim = time.perf_counter()
    async with sema:
        try:
            with open(f"{directory}{file}", "r") as file: 
                content = file.read()
                return content
        except FileNotFoundError:
                print("Error")
    print("Done in less than "+ str(round(time.perf_counter()-tim, 2))+ " seconds") # measures the time
                 
async def filereader(*args): #main function that relies on function "read"
    sema = asyncio.Semaphore(cpu) # uses cpu as semaphore
    readfiles = []
    async with asyncio.TaskGroup() as tg:  
        for file in args:
            readfile = tg.create_task(read(sema, file)) 
            readfiles.append(readfile.result())
    await asyncio.gather(*readfiles)
    for i in readfiles:
        print(i)
    
try: 
    asyncio.run(filereader("text.txt")) #write the file names you want to read
except Exception:
    print("Wrong")


