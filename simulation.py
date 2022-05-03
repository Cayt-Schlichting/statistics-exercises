import numpy as np
import pandas as pd

np.random.seed(322)
nt = 10_000 #num trials

#1) How likely is it to roll doubles when rolling two dice?
n_roll = ncols = 2
opts = [1,2,3,4,5,6]

#generate all the rolls (number of trials * number of rolls per trial)
rolls = np.random.choice(opts,nt*n_roll)
#reshape the date so that each row represents a trial - in this case, each row consists of two rolls
rolls = rolls.reshape(nt,ncols)
#create array T/F on whether the dice rolls are teh same.
are_doubles = (rolls[:,0] == rolls[:,1])

print(f'There is a {round(are_doubles.astype(int).mean() * 100,1)}% chance that you roll doubles.')
print(f'Estimated based on {nt} trials.')

#2) If you flip 8 coins, how likely is it you will get exactly 3 heads?  what about 3 or more heads?
n_flip = 8
#simpler method: Heads is 1
trials = pd.DataFrame(np.random.choice([0,1],nt*n_flip).reshape(nt,n_flip))
#get count of heads in new column
trials['count_heads'] = trials.sum(axis=1)
h3_chance = (trials['count_heads'] == 3).mean()*100 #NOTE: it really doesn't like this in the print statement
gt3h_chance = (trials['count_heads'] > 3).mean()*100
print(f'There is a {round(h3_chance,2)}% chance that you flip 3 heads. Based on {nt} trials')
print(f'There is a {round(gt3h_chance,2)}% chance that you will flip more than 3 heads. Based on {nt} trials.')

#harder method: Figure this out
opts = ['h','t']
trials = pd.DataFrame(np.random.choice(opts,nt*n_flip).reshape(nt,n_flip))
#count defaults to row-wise count
trials['count_heads'] = (trials == 'h').sum(axis=1)
h3_chance = (trials['count_heads'] == 3).mean()*100
gt3h_chance = (trials['count_heads'] >3).mean()*100
print(f'There is a {round(h3_chance,2)}% chance that you flip 3 heads. Based on {nt} trials')
print(f'There is a {round(gt3h_chance,2)}% chance that you will flip more than 3 heads. Based on {nt} trials.')

#3) 3 web dev cohorts to 1 ds cohort - what are odss that two alumni come from have ds students
#maybe not the best approach, but does work
opts = [0,0,0,1]
trials = pd.DataFrame(np.random.choice(opts,2*nt).reshape(nt,2))
both_ds = (trials.sum(axis=1) == 2)
ch = both_ds.mean()*100
print(f'There is a {ch}% chance that both billboards will show data science students')

#alt, which would handle more granular percentiles
df = pd.DataFrame(np.random.random(2*nt).reshape(nt,2))
both_ds = (df < .25).sum(axis=1)==2 #Get bool mask, sum row-wise, if 2 then YAY
ch = both_ds.mean()*100
print(f'There is a {ch}% chance that both billboards will show data science students')

#4)