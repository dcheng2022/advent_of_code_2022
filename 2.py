with open('2.txt', mode='r', encoding='utf-8') as f:
	strategy_list = f.readlines()

scores = []
moves = {'A': 'rock', 'B': 'paper', 'C': 'scissors'}
		 # Part 1: 
		 # 'X': 'rock', 'Y': 'paper', 'Z': 'scissors'}
move_scores = {'rock': 1, 'paper': 2, 'scissors': 3}
winning_rounds = ['rock paper', 'scissors rock', 'paper scissors']
losing_rounds = ['paper rock', 'rock scissors', 'scissors paper']
goals = {'X': losing_rounds, 'Y': 'draw', 'Z': winning_rounds}

def determine_outcome(game):
	if game in winning_rounds:
		return 6
	elif game in losing_rounds:
		return 0
	else:
		return 3

def determine_my_move(opp, goal):
	round_set = None
	if goal == winning_rounds:
		round_set = winning_rounds
	elif goal == losing_rounds:
		round_set = losing_rounds
	else:
		return opp

	for match in round_set:
		opponent_move, my_move = match.split()
		if opp == opponent_move:
			return my_move

for game in strategy_list:
	opponent, me = game.split()
	# Part 1:
	# opponent_move, my_move = moves[opponent], moves[me]
	opponent_move = moves[opponent]
	my_goal = goals[me]
	my_move = determine_my_move(opponent_move, my_goal)
	readable_game = ' '.join([opponent_move, my_move])

	my_score = move_scores[my_move] + determine_outcome(readable_game)
	scores.append(my_score)

print(sum(scores))