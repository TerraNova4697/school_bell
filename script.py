from datetime import datetime

# import logging
#
# from boot import load_configurations


# logger = logging.getLogger("scheduler_logger")


# def main():
dt = datetime.now()
print(dt)
with open("memoryInfo.txt", "a") as outputFile:
    outputFile.write("\n" + f"script waas executed at {dt}")
print("done.")


# if __name__ == "__main__":
#     # load_configurations()
#     main()
