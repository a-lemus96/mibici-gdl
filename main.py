# stdlib modules
import argparse

# third-party modules
from matplotlib import pyplot as plt

# local modules
import utils


# configure arg parser
parser = argparse.ArgumentParser()
parser.add_argument('-fname', type=str, default='nomenclatura_2023_05.csv',
                    help='CSV filename containing stations information')
# parse args
args = parser.parse_args()

positions = utils.load_ecobici(args.fname) # load station xy coords
print(positions)
fig, ax = plt.subplots(figsize=(9,9))
ax.scatter(positions['x'], positions['y'], linewidth=0.05)
plt.show()
