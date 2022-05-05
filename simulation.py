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

#Better - as now it can handle strings and no need to remember numeric assignment
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
#alt - using p parameter in choice
#DO THIS

#4) 3 pop tarts with stddev of 1.5 a day.  
# restock w/ 17, how likely to have some friday afternoon? (4.5 days later)
#generate # of poptarts picked per day
pops = pops2 = pd.DataFrame(np.random.normal(3,1.5,nt*5).reshape(nt,5))

#Version 1 - cuts of the bell curve so we don't count negative pop tarts
#Version 2 - assumes partial and negative poptarts are possible.
#Let's replace anything <0 with 0 and round anything to the nearest whole poptart
pops[pops<0] = 0
pops = pops.round(0)
#how many pop tarts would be gone at the end of the week
pops['wk_cnt'] = pops.sum(axis=1)
pops2['wk_cnt'] = pops2.sum(axis=1)
#chance at least 1 (whole) poptart is left
ch = (pops['wk_cnt'] <17).mean()*100
ch2 = (pops2['wk_cnt'] <=16).mean()*100
print(f'There is a {ch}% chance that there will be a poptart left on Friday afternoon')
print(f'If partial and negative poptarts, there is a {ch2}% chance you get a snack')

#5) Given distro of men/women heights.  what are the chances you pick one of each and woman is taller?
height=pd.DataFrame()
height['m'] = pd.DataFrame(np.random.normal(178,8,(nt,1)))
height['f'] = pd.DataFrame(np.random.normal(170,6,(nt,1)))
height['f_taller'] = height['m'] < height['f']

ch=height['f_taller'].mean()*100
print(f'There is a {round(ch,1)}% chance the woman is taller than the man')

#6) 1/250 chance corrupt download
# what are the odds of having an issue with 50 students? 100?
div = 1/250
n_stud = 100  #18%(ish) with 50.  33%(ish) with 100
df = pd.DataFrame(np.random.random((nt,n_stud)))
issues = df < div #chance we have issues per student
#condense into one column of success or failure
ch_issues = (issues.sum(axis=1) > 0).mean()*100
print(f'There is a {round(ch_issues,1)}% chance we have issues with {n_stud} students')

#7)  70% chance of food truck.  chance of no food truck for 3 days?
df = pd.DataFrame(np.random.random((nt,3))) #chances of food truck each day
#convert df to Bool. sum along axis.  See if new (single col) df = 3 (no food each day)
ch_no_food = ((df > .7).sum(axis=1) == 3).mean()*100
print(f'There is a {round(ch_no_food,1)}% chance of no food truck for 3 days')
#FINISH THESE

#8) 
n_ppl=40  #at 20, high 40%(ish), at 40 ppl - around 89%
partay = pd.DataFrame(np.random.randint(1,366,(nt,n_ppl))) #low inclusive, high exclusive
un_bdays = partay.nunique(axis=1)
ch_same_bday = (un_bdays < n_ppl).mean()*100
print(f'With {n_ppl} in the room, there is a {round(ch_same_bday)}% chance at least two people have the same birthday')


###### EPIC MAGE DUEL ######
# you have 6d4 - you roll 6, 4-sided dice
# opponent has 4d6 - they roll 4, 6 sided dice

#I suspect the 4 sided dice will win more often.  
# Both have max number of points available, but you would have a higher minimum

duel_set = [10,10,10,100,10_000] #number of duels
d4 = [1,2,3,4]
d6 = [1,2,3,4,5,6]

#Go ahead and loop through a few different duels
for nd in duel_set:
    #create df of rolls, and immediately sum into single column
    sixd4 = pd.DataFrame(np.random.choice(d4,size=(nd,6))).sum(axis=1)
    fourd6 = pd.DataFrame(np.random.choice(d6,size=(nd,4))).sum(axis=1)

    you_win = sixd4 > fourd6
    tie = sixd4 == fourd6

    winP = you_win.mean()*100
    tieP = tie.mean()*100

    print(f'Out of {nd} rolls, you won {round(winP,1)}% of the time, and tied {round(tieP,1)}% of the time')

#If you only run 10 duels, there is a range of whether or not you win (limited trials)
#However, when you increase the number of duels, it becomes more clear that you have 
# an advantage with 6, four-sided die

