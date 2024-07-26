from ..Configuration.baseconfig import ConfigStruct

config = ConfigStruct()
config.read_config()
newline = "\n"


def savedata(self, name=None):
    from ..FileHandling.file_writing import generate_local_file

    fname = generate_local_file(self, name)

    if fname:
        config.read_config()
        if config.enable_notifications == "True":
            print(f"Saving data to local storage: {fname}{newline}")

    return fname
