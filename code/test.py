try:
    lol = 2 + "a"
except:
    err = traceback.format_exc()
    print("OOPSSSSS : {}".format(err))
