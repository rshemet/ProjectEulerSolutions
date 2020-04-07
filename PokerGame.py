import numpy as np
import pandas as pd
import random
import itertools

values = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
suits = ['H','D','C','S']
combs_strength = {
    'None': 0,\
    'High Card': 1,\
    'Pair': 2,\
    'Two Pairs': 3,\
    'Three of a Kind': 4,\
    'Straight': 5,\
    'Flush': 6,\
    'Full House': 7,\
    'Four of a Kind': 8,\
    'Straight Flush': 9,\
    'Royal Flush': 10
}


def RestrictedIntInput(lo_lim, hi_lim, text):
    while True:
        try:
            x = int(input(text))
            while int(x) > hi_lim or int(x) < lo_lim:
                x = int(input('Invalid entry! ' + text))
            break
        except:
            print("Enter an integer!")
    return x

def GetGameSpecs():
    num_players = RestrictedIntInput(1, 5, 'How many players would you like to play against (1-5)? ')
    starting_money = RestrictedIntInput(1, 10**9, 'How much money should everybody start with? ')
    blind_size = RestrictedIntInput(1, 10**9, 'Small blind size? ')
    return num_players, starting_money, blind_size

class CardDeck():

    def __init__(self):
        pass
    
    def GenerateDecks(self, x):
        self.deck = []
        for k in range(0,x):
            for i in values:
                for j in suits:
                    self.deck.append(str(i)+str(j))
    
    def RandomDraw(self, num_cards):
        drawn_cards = []
        for i in range(0, num_cards):
            j = random.randint(0, len(self.deck)-1)
            selection = self.deck[j]
            drawn_cards.append(selection)
            self.deck.remove(selection)
        return drawn_cards

class Player():

    def __init__(self, wealth, round_status, card_one, card_two):
        self.wealth = wealth
        self.round_status = round_status
        self.card_one = card_one
        self.card_two = card_two
    
    def Move(self, stage, check = False):
        # Silly player with static provavilities of each move.
        x = random.randint(1,100)
        if stage == 'preflop': #in preflop we can fold, call or double existing bet
            if x < 30:
                return 'fold'
            elif x>90:
                return 'double'
            else:
                return 'call'
        elif stage in ['flop', 'river', 'turn']:
            if check == False: #in game stages, if a bet has been placed before us, we can call double or fold
                if x < 30:
                    return 'fold'
                elif x>90:
                    return 'double'
                else:
                    return 'call'
            elif check == True: #in game stages, if no bet has been placed before us, we can fold, check or raise
                if x < 30:
                    return 'raise'
                elif x>90:
                    return 'fold'
                else:
                    return 'check'

def PromptUserMove(game_stage, playing_table, check = False):
    #this function will collect the player's move and restrict it to selected values based on the game stage.
    highest_bid = playing_table['Bet'].max()
    if game_stage == 'preflop':
        avail_moves = ['fold','call','double']
    elif game_stage in ['flop', 'river', 'turn']:
        if check == False:
            avail_moves = ['fold','call','double']
        elif check == True:
            avail_moves = ['fold','check','raise']
    print(playing_table)
    while True:
        player_input = input(str('Current bet is ' + str(highest_bid) + '. Make your move: '))
        if player_input in avail_moves:
            break
        else:
            print('This is not a valid move! Please choose a move from ', avail_moves)
    return player_input

    # Create players from classes

def CombsOfFive(cards_in_hand, common_cards):
    #this function takes in the two cards a player is dealt (as list) and the five
    #common cards all players share and returns a list of all possible combinations
    #of five cards drawn from those seven.

    #Obviously, this is used in evaluating players' hands by iteration.

    comb_list = cards_in_hand + common_cards
    return list(itertools.combinations(comb_list, 5))
    
def GetMaxCard(cards):
    #this function will return highest card 
    for i in values[::-1]:
        for j in cards:
            if str(j[0]) == str(i):
                return j

def CheckInOrder(cards):
    #this function checks if five passed cards form a straight
    card_list = list(cards)
    hi_card = GetMaxCard(card_list)
    max_card = hi_card
    card_list.remove(hi_card)
    while card_list != []:
        next_highest = GetMaxCard(card_list)
        if values.index(hi_card[0]) -1 == values.index(next_highest[0]):
            card_list.remove(next_highest)
            hi_card = next_highest
        else:
            return False, max_card
    return True, max_card

def SortCardsDescending(cards):
    #function used to e.g. sort kickers in ascending order
    card_list = cards
    output = []
    for i in range(0, len(card_list)):
        hi_card = GetMaxCard(card_list)
        output.append(hi_card)
        card_list.remove(hi_card)
    return output

def CheckPair(cards):
    if cards[0][0] == cards[1][0]:
        return True
    else:
        return False

def UpdateBestComb(combination, max_comb, cards):
    #this function is used exclusively inside the EvaluateHand function to judge whether or not 
    #the latest found max_comb is better than the combination already stored inside the combination
    #dictionary
    if combs_strength[max_comb[0]] > combs_strength[combination['Name']]: #if found comb is stronger, update with new comb
        combination['Cards'] = cards
        combination['Name'] = max_comb[0]
        combination['High'] = max_comb[1]
        combination['Kicker'] = max_comb[2]
        return combination
    elif combs_strength[max_comb[0]] < combs_strength[combination['Name']]: #if found comb is weaker, ignore
        return combination
    elif combs_strength[max_comb[0]] == combs_strength[combination['Name']]: #if same, compare high cards then kickers
        if values.index(max_comb[1]) > values.index(combination['High']): #comparing high cards
            combination['Cards'] = cards
            combination['Name'] = max_comb[0]
            combination['High'] = max_comb[1]
            combination['Kicker'] = max_comb[2]
            return combination
        elif values.index(max_comb[1]) < values.index(combination['High']): 
            return combination
        elif values.index(max_comb[1]) == values.index(combination['High']): #if highs are the same, compare kickers one by one
            if max_comb[2] != []:
                for i in range(0, len(max_comb[2])):
                    if values.index(max_comb[2][i][0]) > values.index(combination['Kicker'][i][0]):
                        combination['Cards'] = cards
                        combination['Name'] = max_comb[0]
                        combination['High'] = max_comb[1]
                        combination['Kicker'] = max_comb[2]
                    elif values.index(max_comb[2][i][0]) < values.index(combination['Kicker'][i][0]):
                        return combination
                    elif values.index(max_comb[2][i][0]) == values.index(combination['Kicker'][i][0]):
                        if i < (len(max_comb[2]) - 1): #if we compared the last kicker and even those are the same, then ignore
                            pass
                        else:
                            return combination
            else:
                return combination

def EvaluateHand(cards_in_hand, common_cards):
    #this function returns the player's best combination (of five) of the seven cards, its strength,
    #the high card of those five and the kickers.

    combination = {
        'Cards': [],\
        'Name': 'None',\
        'High': '',\
        'Kicker': []
    }

    for i in CombsOfFive(cards_in_hand, common_cards):
        straight, hi_card = CheckInOrder(i)

        if all(x[1] == i[0][1] for x in i): #check if all five cards are same suit
            if straight and hi_card[0] == 'A': #check if straight and start with Ace
                combination = UpdateBestComb(combination, ['Royal Flush','A',[]], i)
            elif straight: #check if straight and start with smth else
                combination = UpdateBestComb(combination, ['Straight Flush', hi_card[0],[]], i)
            elif not straight: #means we have regular flush, plug intp update func
                kickers = [k for k in i if k not in [hi_card]]
                combination = UpdateBestComb(combination, ['Flush', hi_card[0],SortCardsDescending(kickers)], i)
        else:
            for j in list(itertools.combinations(i, 4)): #four of a kind loop
                j = list(j)
                if all(x[0] == j[0][0] for x in j): #check if all four cards are same
                    kicker = [k for k in i if k not in j]
                    combination = UpdateBestComb(combination, ['Four of a Kind', j[0][0] , kicker], i)
            if straight:
                combination = UpdateBestComb(combination, ['Straight', hi_card[0],[]], i)
            else:
                for j in list(itertools.combinations(i, 3)): #three of a kind loop
                    j = list(j)
                    if all(x[0] == j[0][0] for x in j): #check if all three cards are same
                        remaining_two = [k for k in i if k not in j]
                        if CheckPair(remaining_two): #check if we have full house
                            combination = UpdateBestComb(combination, ['Full House', j[0][0],remaining_two[0]], i)
                        else:
                            combination = UpdateBestComb(combination, ['Three of a Kind', j[0][0],SortCardsDescending(remaining_two)], i)
                    else:
                        for j in list(itertools.combinations(i, 2)): #two of a kind loop
                            j = list(j)
                            if CheckPair(j):
                                remaining_three = [k for k in i if k not in j]
                                for n in list(itertools.combinations(remaining_three, 2)): #second two of a kind loop, looks for two pairs
                                    if CheckPair(n):
                                        remaining_one = [k for k in remaining_three if k not in n]
                                        combination = UpdateBestComb(combination, ['Two Pairs', j[0][0], [n[0]] + remaining_one], i)
                                    else:
                                        combination = UpdateBestComb(combination, ['Pair', j[0][0], SortCardsDescending(remaining_three)], i)
                            else:
                                kickers = [k for k in i if k not in [hi_card]]
                                combination = UpdateBestComb(combination, ['High Card', hi_card[0],SortCardsDescending(kickers)], i)
                                                
    return combination



def FlopRiverTurnMoves(sb, playing_table, players, num_P, game_stage, round_stats):

    starting_player = players.index(sb)

    while playing_table.loc[:,'Still in?'].iloc[starting_player] == False:
        starting_player = (starting_player+1)%(num_P+1)

    active_players = [a for a in playing_table.index if playing_table.loc[a,'Still in?'] == True]

    if players[starting_player] != 'You':
        move = eval(players[starting_player] + '.Move(stage = game_stage, check = True)')
        print(players[starting_player], ' chooses ', move)
    else:
        move = PromptUserMove(game_stage, playing_table, check = True)
    
    active_players.remove(players[starting_player])

    if move == 'check':
        playing_table.loc[players[starting_player],'Bet'] = 0
        highest_bid = 0
    elif move == 'raise':
        playing_table.loc[players[starting_player],'Bet'] = small_Blind * 2
        highest_bid = small_Blind * 2
    elif move == 'fold':
        playing_table.loc[players[starting_player],'Still in?'] = False
        highest_bid = 0

    bets = [playing_table.loc[a,'Bet'] for a in playing_table.index if playing_table.loc[a,'Still in?'] == True]
    
    #betting begins until all bets are equalized
    current_mover = starting_player
    while not all(x == bets[0] for x in bets) or active_players != []:

        next_mover = (current_mover + 1)%(num_P+1)

        if playing_table.loc[players[next_mover],'Still in?'] == True:

            can_play_check = highest_bid == 0

            if players[next_mover] != 'You':
                if can_play_check:
                    move = eval(players[next_mover] + '.Move(stage = game_stage,check = True)')
                else:
                    move = eval(players[next_mover] + '.Move(stage = game_stage,check = False)')
                print(players[next_mover], ' chooses ', move)
            else:
                move = PromptUserMove(game_stage, playing_table, check = can_play_check)

            if move == 'check':
                playing_table.loc[players[next_mover],'Bet'] = 0
            elif move == 'call':
                playing_table.loc[players[next_mover],'Bet'] = highest_bid
            elif move == 'raise':
                playing_table.loc[players[next_mover],'Bet'] = small_Blind * 2
                highest_bid = small_Blind * 2
                active_players = [a for a in playing_table.index if playing_table.loc[a,'Still in?'] == True]
            elif move == 'double':
                playing_table.loc[players[next_mover],'Bet'] = highest_bid * 2
                highest_bid *= 2
                active_players = [a for a in playing_table.index if playing_table.loc[a,'Still in?'] == True]
            elif move == 'fold':
                playing_table.loc[players[next_mover],'Still in?'] = False

            active_players.remove(players[next_mover])

        current_mover = next_mover
        bets = [playing_table.loc[a,'Bet'] for a in playing_table.index if playing_table.loc[a,'Still in?'] == True]

    round_stats['Pot'] += playing_table.loc[:,'Bet'].sum()

    for i in playing_table.index:
        bet = playing_table.loc[i,"Bet"]
        exec(i + '.wealth -= bet')
        playing_table.loc[i,'Bet'] = 0
        playing_table.loc[i,'Wealth'] = eval(i + '.wealth')

    return playing_table, round_stats

if __name__ == '__main__':

    num_P, start_Cash, small_Blind = GetGameSpecs()

    for i in range(0, num_P):
        func_str = 'Player_' + str(i+1) + ' = Player(' + str(start_Cash) + ',"X","X","X")'
        exec(func_str)

    You = Player(start_Cash,'X','X','X')

        #Here we create the true dealt hands under - players_hands -

    cards_in_hand = [
        'C 1',\
        'C 2',
    ]

    players = ['You']
    for i in range(0, num_P):
        players.append('Player_' + str(i+1))

    players_hands = pd.DataFrame(columns = cards_in_hand, index = players)

        #Now, we need the visible info (your hands, 5 mutual cards, bet info, etc.)

    info_cols = [
        'C 1',\
        'C 2',\
        'Status',\
        'Wealth',\
        'Still in?',\
        'Bet'
    ]

    playing_table = pd.DataFrame(columns = info_cols, index = players)

    round_count = 1

    # GAME LOOP:

    while True:

        our_deck = CardDeck()
        our_deck.GenerateDecks(1)

        round_stats = {
            'Pot': 0,\
            'Opened Cards': []
        }

        print('\nRound ' + str(round_count) + '!\n')
        playing_table.loc['You','Status'] = 'D'
        playing_table.loc['Player_1','Status'] = 'SB'
        playing_table.loc['Player_2','Status'] = 'B'

        #assign random dealer on Round 1
        if round_count == 1:
            dealer_index = random.randint(0,num_P)
            sb_index = (dealer_index + 1) % (num_P + 1)
            bb_index = (dealer_index + 2) % (num_P + 1)
            dealer = playing_table.index[dealer_index]
            sb = playing_table.index[sb_index]
            bb = playing_table.index[bb_index]
            exec(dealer + '.round_status = "D"')
            exec(sb + '.round_status = "SB"')
            exec(bb + '.round_status = "BB"')
    
        #update playing table
        for i in players_hands.index:
            draw = our_deck.RandomDraw(2)
            players_hands.loc[i,:] = draw
            if i == 'You':
                playing_table.loc[i,'C 1':'C 2'] = draw
            else:
                playing_table.loc[i,'C 1':'C 2'] = ['X','X']
            playing_table.loc[i,'Status'] = eval(str(i)+'.round_status')
            playing_table.loc[i,'Wealth'] = eval(str(i)+'.wealth')
            playing_table.loc[i,'Still in?'] = True if eval(str(i)+'.wealth') > 0 else False
            playing_table.loc[i,'Bet'] = 0

        ### Pre-Flop: everybody must move until bets are equalized
        playing_table.loc[sb,'Bet'] = small_Blind
        playing_table.loc[bb,'Bet'] = small_Blind * 2

        bets = playing_table['Bet'].tolist()
        current_mover = players.index(bb)
        highest_bid = small_Blind * 2

        while not all(x == bets[0] for x in bets):

            next_mover = (current_mover + 1)%(num_P+1)

            if playing_table.loc[players[next_mover],'Still in?'] == True:

                if players[next_mover] != 'You':
                    move = eval(players[next_mover] + '.Move(stage = "preflop")')
                    print(players[next_mover], ' chooses ', move)
                else:
                    move = PromptUserMove('preflop', playing_table)

                if move == 'call':
                    playing_table.loc[players[next_mover],'Bet'] = highest_bid
                elif move == 'double':
                    playing_table.loc[players[next_mover],'Bet'] = highest_bid * 2
                    highest_bid *= 2
                elif move == 'fold':
                    playing_table.loc[players[next_mover],'Still in?'] = False

            current_mover = next_mover
            bets = [playing_table.loc[a,'Bet'] for a in playing_table.index if playing_table.loc[a,'Still in?'] == True]

        #conclude pre-flop, adjust wealth and take bets into pot
        round_stats['Pot'] = playing_table.loc[:,'Bet'].sum()

        for i in playing_table.index:
            bet = playing_table.loc[i,"Bet"]
            exec(i + '.wealth -= bet')
            playing_table.loc[i,'Bet'] = 0
            playing_table.loc[i,'Wealth'] = eval(i + '.wealth')

        print(playing_table)

        print('\nPre-Flop over! ', [a for a in playing_table.index if playing_table.loc[a,'Still in?'] == False], ' have folded. ', [a for a in playing_table.index if playing_table.loc[a,'Still in?'] == True], ' still in the game. Total pot is ', round_stats['Pot'], '.')

        ### Open Flop:

        flop = our_deck.RandomDraw(3)
        round_stats['Opened Cards'] = flop + ['X'] + ['X']
        print('\nThe flop cards are: ', round_stats['Opened Cards'])

        #Call our function for the Flop:

        playing_table, round_stats = FlopRiverTurnMoves(sb, playing_table, players, num_P, 'flop', round_stats)

        ### Open River:

        river = our_deck.RandomDraw(1)
        round_stats['Opened Cards'] = flop + river + ['X']
        print('\nThe river cards are: ', round_stats['Opened Cards'])

        playing_table, round_stats = FlopRiverTurnMoves(sb, playing_table, players, num_P, 'river', round_stats)

        ### Open Turn:
        turn = our_deck.RandomDraw(1)
        round_stats['Opened Cards'] = flop + river + turn
        print('\nThe turn cards are: ', round_stats['Opened Cards'])

        playing_table, round_stats = FlopRiverTurnMoves(sb, playing_table, players, num_P, 'turn', round_stats)

        print(playing_table)
        break