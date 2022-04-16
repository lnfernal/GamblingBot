import numpy as np
import pandas as pd

def odds_to_probability(odds):
    if odds < 0:
        odds_adjusted = odds*(-1)
        p_adjusted = odds_adjusted/(odds_adjusted+100)
    else:
        p_adjusted = 100/(odds_adjusted+100)
    return p_adjusted

def compute_odds(odd_hit,odd_miss):
    adjusted_hit = odds_to_probability(odd_hit)
    adjusted_miss = odds_to_probability(odd_miss)
    house_edge = (adjusted_hit+adjusted_miss - 1) / 2
    if house_edge < 0:
        return adjusted_hit
    else:
        return (adjusted_hit-house_edge)

def get_multiplier(odds_list):
    num_bets = len(odds_list)
    if num_bets == 2:
        multiplier = 3
    elif num_bets == 3:
        multiplier = 5
    elif num_bets == 4:
        multiplier = 10
    return multiplier

def is_profitable(odds_list):
    multiplier = get_multiplier(odds_list)
    adjusted_odds = []
    for i in odds_list:
        odds_hit_a = i[0]
        odds_miss_a = i[1]
        adjusted_a = compute_odds(odds_hit_a,odds_miss_a)
        adjusted_odds.append(adjusted_a)
    product = 1
    for i in adjusted_odds:
        product *= i
    ev = multiplier*product-1
    if ev>0:
        return True,ev
    else:
        return False,ev
        
def kelly(bankroll,adjusted_hit,odds_list):
    p = adjusted_hit + (1-adjusted_hit)/(get_multiplier(odds_list)-1)
    return bankroll*p