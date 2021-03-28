import sys
import os
import django

sys.dont_write_bytecode = True
os.environ["DJANGO_SETTINGS_MODULE"] = "n2edm.settings"
django.setup()

def main():
    print("WOOO2!")

if __name__ == "__main__":
    main()
