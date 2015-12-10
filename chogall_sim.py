import random
import math

class Configuration:
    num_friends = 2                     # the number of friends attempting to unlock Cho'gall
    chogall_chance = 0.001              # probability of Cho'gall appearing as a player
    unlock_games = 1                    # the number of games required to unlock Cho'gall
    players_per_match = 10              # the number of players per match
    party_size_affects_players = True   # if this is True, k friends in a party means there are (n - k) chances for Cho'gall, where n is the number of players per match
                                        # False means that the chance for Cho'gall is always the same, the friend party size does not affect the chance of Cho'gall appearing in a particular match
    queue_independently = True          # if this is True, each friend queues independently
                                        # if this is False, all friends queue together
    num_samples = 1000                  # the number of random samples to try


# returns n choose k
def nCk(n, k):
    return math.factorial(n) / (math.factorial(k) * math.factorial(n-k)) # n! / (k!*(n-k)!)


# returns the probability of getting at least k successes in a binomial distribution with the given parameters
def binomial_distribution(n, p, k):
    prob = 0.0 # the total probability of at least k successes
    for i in range(k, n): # for each acceptable number of successes (k-n)
        prob += nCk(n,i) * p**i * (1.0-p)**(n-i) # add the probability of exactly i successes
    return prob


# runs a simulation with the given config
# returns the average number of matches it took to unlock Cho'gall
def run_simulation(config):
    avg_matches_to_unlock = 0 # tracks the number of matches it took to unlock Cho'gall with this configuration
    for s in range(config.num_samples): # do num_samples
        attempts = 0 # the number of matches played
        successes = [] # the number of Cho'galls seen for each friend
        [successes.append(0) for i in range(config.num_friends)] # add a Cho'gall match counter for each friend
        while config.unlock_games not in successes: # play games until Cho'gall is unlocked by one of the friends
            if not config.queue_independently: # if players are all playing in a party
                choice = random.random() # generate only one match
            for i in range(config.num_friends): # look at the match that each friend is in
                if config.queue_independently: # if players are all in different games
                    choice = random.random() # generate the chance to see Cho'gall for each player
                if config.party_size_affects_players: # if party size affects players
                    n = (config.players_per_match - config.num_friends) # friends take up slots in the match (potential chances to see Cho'gall)
                else: # if party size does not affect players
                    n = config.players_per_match # friends don't take up potential Cho'gall slots
                chance = binomial_distribution(n, config.chogall_chance, 1) # calculate success probability from binomial distribution
                if choice < chance: # if a Cho'gall appeared
                    successes[i] += 1 # mark the friend's success
            attempts += 1 # mark the attempt
        # once the Cho'gall has been unlocked for this sample
        avg_matches_to_unlock += float(attempts) / float(config.num_samples) # compute the average in progress
    # once all samples have been completed
    return avg_matches_to_unlock # returns the probability of at least k successes using the given binomial distribution


# test
c1 = Configuration()

c2 = Configuration()
c2.queue_independently = False

c3 = Configuration()
c3.unlock_games = 100

c4 = Configuration()
c4.unlock_games = 100
c4.queue_independently = False

print("1 game to unlock, queuing separately")
print("average matches: " + str(run_simulation(c1)))

print("1 game to unlock, queuing together")
print("average matches: " + str(run_simulation(c2)))

print("5 games to unlock, queuing separately")
print("average matches: " + str(run_simulation(c3)))

print("5 games to unlock, queuing together")
print("average matches: " + str(run_simulation(c4)))
