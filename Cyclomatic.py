import os
from radon.complexity import SCORE
from radon.cli.harvest import CCHarvester
from radon.cli import Config
from github import Github


cc_path = '/Users/Sean/Documents/GitHub/Distributed_System/Proxy.py'
cc_config = Config(
                   exclude='',
                   ignore='venv',
                   order=SCORE,
                   no_assert=True,
                   show_closures=False,
                   min='A',
                   max='F',
                   )


file = open(cc_path, 'r')

results = CCHarvester(cc_path, cc_config).gobble(file)

total_cc = 0

for i in results:
    print (i.complexity)
    total_cc += int(i.complexity)

avg_cc = total_cc/ len(results)
print("Total complexity of file: " + str(total_cc))
print("Average complexity of file: " + str(avg_cc))


