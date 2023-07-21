# to check whether python3 loads the entire program into itself before starting execution or not

# yes python loads at once, so we can run multiple simulations also on the same file
import time
from datetime import datetime

print(f'Starting script at {datetime.now()}')
sleep_time = 20
time.sleep(sleep_time)
print('def')
print(f'Ending script at {datetime.now()}')
