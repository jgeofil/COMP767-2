import numpy as np
from statsmodels.robust import mad

rest_f = np.load('rest_users_followers_shorts.npy')[:15000]
rest_i = np.load('rest_users_ids_shorts.npy')[:15000]

stream_f = np.load('stream_users_followers_shorts.npy')[:15000]
stream_i = np.load('stream_users_ids_shorts.npy')[:15000]

print(min(stream_i), max(stream_i))

print('REST')
print('Mean', np.mean(rest_f))
print('SD', np.std(rest_f))
print('Median', np.median(rest_f))
print('Mad', mad(rest_f))

print('STREAM')
print('Mean', np.mean(stream_f))
print('SD', np.std(stream_f))
print('Median', np.median(stream_f))
print('Mad', mad(stream_f))

print(sorted(stream_f)[-15:])

print(sorted(rest_f)[-5:])