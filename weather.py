import sys
from weather import app

if __name__ == "__main__":
    try:
        app.main()
    except KeyboardInterrupt:
        sys.exit('interrupted')
        pass
