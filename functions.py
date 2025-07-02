import pandas as pd
import random
import numpy as np
from collections import Counter

def show_cards(hand):
  suit = ['♣','♠','♦','♥']
  rank = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']

  hand_ordered = sorted(hand)
  show_hand = []

  for card in hand_ordered:
    if card == 52:
      show_hand.append(' 🂿 ')
    elif card == 53:
      show_hand.append(' 🃟 ')
    else:
      show_hand.append(rank[card%13] + suit[card//13])
  return show_hand


def dealing(cards, players = 3, chunk_size=100000): # need to be fool-proof for chunk_size
    """
    dealing the deck of cards to players

    cards
    players: # of players
    chuck_size: number of cards dealing each time
    """
    # print(cards, len(cards))
    hands = [[] for _ in range(players)]
    current_card_index = 0
    num_cards = len(cards)


    while current_card_index < num_cards:
        # Determine how many cards to deal in this chunk
        cards_to_deal_in_chunk = min(chunk_size, int((num_cards - current_card_index)/players) )

        if cards_to_deal_in_chunk == 0:
            cards_to_deal_in_chunk = 1
        print("> Dealing ",cards_to_deal_in_chunk, " cards to each player...")

        if cards_to_deal_in_chunk < 0:
            break # Should not happen if current_card_index < num_cards, but good practice

        # Deal the chunk of cards to the current player
        for player in range(players):
            for _ in range(cards_to_deal_in_chunk):
                hands[player].append(cards[current_card_index])
                current_card_index += 1
                if current_card_index >= num_cards:
                # print(hands)
                    return hands

    # print(hands)
    return hands


def winding_num(seq):
  winding_seq = []
  for i in range(len(seq)):
    if i == 0:
      pre = len(seq)-1
      suc = i+1
    elif i ==len(seq)-1:
      pre = i - 1
      suc = 0
    else:
      pre = i-1
      suc = i+1
    loc_pre = seq.index(pre)
    loc_i = seq.index(i)
    loc_suc = seq.index(suc)
    if loc_i>loc_pre:
      d1 = loc_i-loc_pre
    else:
      d1 = len(seq)-loc_pre+loc_i
    if loc_i<loc_suc:
      d2 = loc_suc-loc_i
    else:
      d2 = len(seq)-loc_i+loc_suc
    winding_seq.append(d1+d2-1)
  return winding_seq

# riffle shuffling
# riffle shuffling
def riffle_shuffle(cards, deviding_p = 0.5, var = 1, shuffling_lam = 0.5, time = 1): # default is a faro shuffle
  new_cards = cards
  for i in range(time):
    # cutoff = np.random.binomial(n=len(new_cards), p=deviding_p, size=1)[0] # option 1 (not considered): the number of cards in one half follows binomial(54,p), variance = 54 * p * (1-p)
    cutoff = np.random.normal(loc=len(cards)*deviding_p, scale = var, size = 1)[0].round() # option 2: the number of cards in one half follows N(54*deviding_p, var)

    half1 = new_cards[:int(cutoff)]
    half2 = new_cards[int(cutoff):]

    new_cards = []
    while min( len(half1), len(half2) )>0:
      num_cards_half1 = len(half1)
      num_cards_half2 = len(half2)
      n = num_cards_half1 + num_cards_half2
      p = num_cards_half1/n
      q = num_cards_half2/n

      num_insert = np.random.choice(2, 1, p=[p, q])
      num_card = np.random.poisson(lam=shuffling_lam, size=2)[0]+1 # assuming the number of cards droped follows poisson(shuffling_lam)+1

      if num_insert == 0:
        new_cards.extend(half1[:num_card])
        half1 = half1[num_card:]
      elif num_insert == 1:
        new_cards.extend(half2[:num_card])
        half2 = half2[num_card:]

    new_cards.extend(half1)
    new_cards.extend(half2)
  return new_cards


# riffle shuffling
def gsr(cards, time = 1):
  """
  Gilbert-Shannon-Reeds (GSR) model is a good description of the way real people shuffle real cards.

  """
  new_cards = cards
  for i in range(time):
    cutoff = np.random.binomial(n=len(cards), p=0.5, size=1)[0]

    half1 = new_cards[:int(cutoff)]
    half2 = new_cards[int(cutoff):]

    new_cards = []
    while min( len(half1), len(half2) )>0:
      num_cards_half1 = len(half1)
      num_cards_half2 = len(half2)
      n = num_cards_half1 + num_cards_half2
      p = num_cards_half1/n
      q = num_cards_half2/n

      num_insert = np.random.choice(2, 1, p=[p, q])

      if num_insert == 0:
        new_cards.append(half1[0])
        half1 = half1[1:]
      elif num_insert == 1:
        new_cards.append(half2[0])
        half2 = half2[1:]

    new_cards.extend(half1)
    new_cards.extend(half2)
  return new_cards

def overhand_shuffle(cards, var = 1, overhand_time =4, time= 1):
  old_cards = cards

  for i in range(time):
    # cutoff = np.random.binomial(n=len(cards), p=deviding_p, size=overhand_time) # binomial
    cutoff = np.random.normal(loc= len(cards)/(overhand_time+1), scale = 1, size = overhand_time).round() # normal


    # old_cards = cards
    new_cards = []

    for n in range(overhand_time):
      packet = old_cards[:int(cutoff[n])]
      old_cards = old_cards[int(cutoff[n]):]
      new_cards = packet + new_cards
    new_cards = old_cards + new_cards

    old_cards = new_cards

  return new_cards

def hindu_shuffle(cards, location=0.5, prop=0.5, var =4, time= 5):
  old_cards = cards
  
  mu1 = round(max(location - prop/2,0) * len(cards))
  mu2 = round(min(location + prop/2,1) * len(cards))
  cutoff1 = np.random.normal(loc=mu1, scale=var, size = 1)[0].round()
  cutoff2 = np.random.normal(loc=mu2, scale=var, size = 1)[0].round()

  packet = old_cards[int(cutoff1):int(cutoff2)]

  packet = overhand_shuffle(packet, var=var, overhand_time =time, time= 1)

  new_cards = packet + old_cards[:int(cutoff1)] + old_cards[int(cutoff2):]

  old_cards = new_cards

  return new_cards

def cutting_shuffle(cards, location = 0.5, var = 1):
  cutoff = np.random.normal(loc=location*len(cards), scale=var, size=1)[0].round()
  return cards[int(cutoff):] + cards[:int(cutoff)]


def make_random(cards, random_seed =0 ):
  # random.seed(random_seed)
  random.shuffle(cards)
  return cards

def shuffling(cards, shuffle_proc = [], par_dict={}):
  if shuffle_proc == []:
    return cards

  else:
    for shuffle in shuffle_proc:
      print(" >> Performing", shuffle)
      if shuffle not in par_dict:
        new_cards = eval(shuffle)(cards)
      else:
        new_cards = eval(shuffle)(cards, **par_dict[shuffle])



      cards = new_cards
      # print(len(cards))
  return new_cards


def modified_jaccard(hand1, hand2):
  """
  Calculates a Jaccard similarity between two lists (card hands),
  accounting for duplicate items.

  Args:
    hand1: The first list of items (cards).
    hand2: The second list of items (cards).

  Returns:
    The modified Jaccard similarity score (a float between 0 and 1).
  """

  freq1, freq2 = Counter(hand1), Counter(hand2)
  all_cards = set(hand1) | set(hand2)
  intersection = sum(min(freq1.get(card, 0), freq2.get(card, 0)) for card in all_cards)
  union = sum(max(freq1.get(card, 0), freq2.get(card, 0)) for card in all_cards)
  # print(union )

  return intersection / union if union else 0



def modified_dice(hand1, hand2):
    freq1 = Counter(hand1)
    freq2 = Counter(hand2)
    unique_cards = set(hand1) | set(hand2)

    freq_vector1 = [freq1.get(card, 0) for card in unique_cards]
    freq_vector2 = [freq2.get(card, 0) for card in unique_cards]

    # Modified dice "similarity" score
    distance = sum(abs(f1 - f2) for f1, f2 in zip(freq_vector1, freq_vector2))
    score = 1 - distance / (len(hand1)+len(hand2))
    # Subtract from 1 to make higher = more similar

    # print((len(hand1)+len(hand2)), distance )
    return score



def guess_cards(old_hand, new_hand, shuffle_proc=[]):
    """
    Function to guess the order of cards in a shuffled deck.

    Parameters:
    old_hand (list): The original order of the deck.
    new_hand (list): The new order of the deck after shuffling.
    shuffle_proc (list): The process of shuffling (optional).

    Returns:
    list: The guessed order of cards.
    """
    # Flatten the old_hand and new_hand lists
    old_deck = sum(old_hand, [])
    new_deck = sum(new_hand, [])

    n = len(old_deck)

    # Check if the deck has been cut
    if_cut = ('cutting_shuffle' in shuffle_proc)


    # a list of 0/1 sequence, 1 if the card is revealed
    revealed_cards = [0]*n
    correct_num = 0

    # Create a list to track the original order
    original_order = old_deck[:]

    if if_cut:
        # Make the first guess randomly
      first_guess_loc = random.randrange(n)
      first_guess = old_deck[first_guess_loc]

      if first_guess == new_deck[0]:
        correct_num += 1
        revealed_cards[first_guess_loc] = 1
      else:
        revealed_cards[old_deck.index(new_deck[0])] = 1

      old_deck = old_deck[old_deck.index(new_deck[0]):] + old_deck[:old_deck.index(new_deck[0])]
      revealed_cards = revealed_cards[old_deck.index(new_deck[0]):] + revealed_cards[:old_deck.index(new_deck[0])]
      new_deck = new_deck[1:]


    while len(new_deck)>0:

      longest = (0, -1)  # (length, start_index)
      current_start = None

      for i, val in enumerate(revealed_cards):
        if val == 0:
          if current_start is None:
            current_start = i
          if i == len(revealed_cards) - 1 or revealed_cards[i + 1] != 0:
            length = i - current_start + 1
            if length > longest[0]:
              longest = (length, current_start)
            current_start = None
        else:
          current_start = None
      guess = old_deck[longest[1]]
      if guess == new_deck[0]:
        correct_num +=1
        revealed_cards[longest[1]] = 1
      else:
        revealed_cards[old_deck.index(new_deck[0])] = 1
      new_deck = new_deck[1:]
    return correct_num



def compare2hands(cards, shuffle_proc=[], shuffle_par={},dealing_par={},metrics=['jaccard']):
  old_hands = dealing(cards, **dealing_par)
  new_hands = shuffling(cards, shuffle_proc = shuffle_proc, par_dict = shuffle_par)
  new_hands = dealing(new_hands, **dealing_par)

  print("Old hands: ", old_hands)
  print("New hands: ", new_hands)

  similarity_scores = dict.fromkeys(metrics, 0)

  for new_hand in new_hands:
    new_hand_jacard = []
    new_hand_dice = []
    for old_hand in old_hands:
      if 'jaccard' in  metrics:
        new_hand_jacard.append(modified_jaccard(new_hand, old_hand)/len(old_hands))
        # print("*** jaccard score: ", modified_jaccard(new_hand, old_hand)/len(old_hands))
      if 'dice' in metrics:
        new_hand_dice.append(modified_dice(new_hand, old_hand)/len(old_hands))
        # print("*** dice score: ", modified_dice(new_hand, old_hand)/len(old_hands))


    if 'jaccard' in metrics:
      similarity_scores['jaccard'] += max(new_hand_jacard)
    if 'dice' in metrics:
      similarity_scores['dice'] += max(new_hand_dice)


  if 'mcgrath_guesses' in metrics:
    similarity_scores['mcgrath_guesses'] = guess_cards(old_hands, new_hands, shuffle_proc = shuffle_proc)
      # print(similarity_scores)
  for metric in metrics:
    print('The ',metric, ' is', similarity_scores[metric])
  return similarity_scores


def compare2strategy(cards, simulation_time = 100, max_shuffle = 10, shuffle_proc=[], shuffle_par={},dealing_par={},metrics=['jaccard']):
  result = []
  for run in range(simulation_time):
    random.seed(run)
    random.shuffle(cards)
    for t in range(1,max_shuffle):
      shuffle_procedure = shuffle_proc * t
      new_result = compare2hands(cards, shuffle_proc=shuffle_procedure,
                  shuffle_par = shuffle_par,
                  dealing_par = dealing_par,
                  metrics=metrics)
      new_result['type'] = f'{t} shuffles'
      # new_result['type'] = 'shuffles'
      result.append(new_result)
  result = {metric: [dic[metric] for dic in result] for metric in result[0]}
  result = pd.DataFrame(result)

  result2 = []
  for run in range(simulation_time):
    random.seed(run)
    random.shuffle(cards)
    
    new_result = compare2hands(cards, shuffle_proc=['make_random'],
                  dealing_par = dealing_par,
                  metrics=metrics)
    new_result['type'] = 'Random'
    # new_result['type'] = 'random'
    result2.append(new_result)
  result2 = {metric: [dic[metric] for dic in result2] for metric in result2[0]}
  result2 = pd.DataFrame(result2)
  result = pd.concat([result, result2], ignore_index=True)
  
  result = pd.melt(
    result,
    id_vars=['type'],
    value_vars= metrics,
    var_name='metric',
    value_name='value')
  return result

def compare2random(cards, simulation_time = 100, simulation_time_random = 500,  max_shuffle = 10, shuffle_proc=[], shuffle_par={},dealing_par={},metrics=['jaccard']):
  result = []
  for run in range(simulation_time):
    random.seed(run)
    random.shuffle(cards)
    
    
    new_result = compare2hands(cards, shuffle_proc=shuffle_proc,
                  shuffle_par = shuffle_par,
                  dealing_par = dealing_par,
                  metrics=metrics)
    new_result['type'] = 'Shuffled'
      
    result.append(new_result)
  result = {metric: [dic[metric] for dic in result] for metric in result[0]}
  result = pd.DataFrame(result)

  result2 = []
  for run in range(simulation_time_random):
    random.seed(run)
    random.shuffle(cards)

    new_result = compare2hands(cards, shuffle_proc=['make_random'],
                  dealing_par = dealing_par,
                  metrics=metrics)
    new_result['type'] = 'Random'
    # new_result['type'] = 'random'
    result2.append(new_result)
  result2 = {metric: [dic[metric] for dic in result2] for metric in result2[0]}
  result2 = pd.DataFrame(result2)
  result = pd.concat([result, result2], ignore_index=True)

  result = pd.melt(
    result,
    id_vars=['type'],
    value_vars= metrics,
    var_name='metric',
    value_name='value')
  return result
