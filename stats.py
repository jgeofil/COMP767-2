import numpy as np
import matplotlib.pyplot as plt

rest_f = np.load('rest_users_followers_shorts.npy')[:15000]
rest_i = np.load('rest_users_ids_shorts.npy')[:15000]

stream_f = np.load('stream_users_followers_shorts.npy')[:15000]
stream_i = np.load('stream_users_ids_shorts.npy')[:15000]

log_rest = rest_f
log_stream = stream_f

font = {'size': 13}

bins = [1.5**x for x in range(0,35)]
rest, _, _ = plt.hist(log_rest, bins=bins, alpha=0.7)
stream, _, _ = plt.hist(log_stream, bins=bins, alpha=0.7)
plt.xscale('log')
plt.xlabel('# followers', fontdict=font)
plt.ylabel('# users', fontdict=font)

plt.tick_params(axis='both', which='major', labelsize=13)

plt.legend(['RESTful', 'Streaming'])

plt.show()


