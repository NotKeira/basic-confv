from src.cli import ConfvCLI
from src.utils import Utils

# Confv is a Configuration File Validator based on pre-created schemas.
# Confv is intended for use on any file type, as well as any configuration file. 

# Create the Utility class
utils = Utils()

if __name__ == "__main__":
    confv = ConfvCLI(utils)
    confv.run()
