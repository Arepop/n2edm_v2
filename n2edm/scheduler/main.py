import sys
import os
import django

sys.dont_write_bytecode = True
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "n2edm.settings")
django.setup()

def main():
    print("WooOO!")

if __name__ == "__main__":
    main()
