import time
import asyncio

# Synchronous - wait and go line by line

# def download_file():
#     print("File downloading")
#     time.sleep(5)
#     print("Download completed")
 
# def main():
#     download_file()
#     print("New Task...")
    
# main()

# Asynchronous - non blocking execution

async def say_hello():
    print("Hello")

async def download_file():
    print("Downloading file")
    await asyncio.sleep(5)
    print("download completed")

async def main():
    await asyncio.gather(
        download_file(),
        say_hello()
    )
    print("New Task...")
    
    
asyncio.run(main())
