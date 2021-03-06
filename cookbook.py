import numpy as np 
from deck import Deck
import pdb
import matplotlib.pyplot as plt
from read_list import read_exported_list

def cookbook_run(turn_played=2, draw_p=1):
    power = read_exported_list('decklists/ghp_haunted.txt')
    deck = Deck(power)
    deck.draw_7()
    damage_taken = 0
    damage_across_turns = []

    for i in range(turn_played-1):
        deck.draw()
        damage_across_turns.append(damage_taken)
    while len(deck.deck) > 0:
        card = deck.draw()
        while card == 'firebomb':
            damage_taken += 5
            card = deck.draw()

        if np.random.random() < draw_p:
            deck.add_card('firebomb')
            card = deck.draw()
            while card == 'firebomb':
                damage_taken += 5
                card = deck.draw()
        damage_across_turns.append(damage_taken)
    return damage_across_turns

total_damage = []
damage_during_turn_x = []

num_runs = 10000
for i in range(num_runs):
    damage_across_turns = cookbook_run(5, 0.9)
    if len(total_damage) == 0:
        total_damage = damage_across_turns
        damage_during_turn_x = [[x] for x in damage_across_turns]
    else:
        total_damage = [x+y for x,y in zip(total_damage, damage_across_turns)]
        [x.append(y) for x,y in zip(damage_during_turn_x, damage_across_turns)]
    if i%1000 == 0:
        print(i)

expected_total_damage = [float(x)/num_runs for x in total_damage]
prob_dying = [sum([x > 25 for x in y])/num_runs for y in damage_during_turn_x]

sds = [np.std(x) for x in damage_during_turn_x]
# plt.plot(range(len(prob_dying)), prob_dying)
# plt.xlabel('Turn')
# plt.ylabel('Probability of dying')
# plt.show()

plt.plot(range(len(expected_total_damage[:50])), [x for x in expected_total_damage[:50]], 'k-')
lower_bound = [x-2*y for x,y in zip(expected_total_damage[:50],sds)]
upper_bound = [x+2*y for x,y in zip(expected_total_damage[:50],sds)]
plt.fill_between(range(50), lower_bound, upper_bound, alpha=0.5, edgecolor='#CC4F1B', facecolor='#FF9848')
lower_bound = [x-y for x,y in zip(expected_total_damage[:50],sds)]
upper_bound = [x+y for x,y in zip(expected_total_damage[:50],sds)]
plt.fill_between(range(50), lower_bound, upper_bound)

print(expected_total_damage[15])
print(sds[15])

plt.xlabel('Turn')
plt.ylabel('expected total damage with SDs')
plt.show()