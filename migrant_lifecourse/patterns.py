import re

pat1 = re.compile("v=(?P<nr>.*)")
pat2 = re.compile("""(?P<bc>[0-9]{4,10})""")