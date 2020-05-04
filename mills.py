import random
import json

# Simulating a classic vintage slot machine, like those of manufacturers
# like Mills, Watling, or Jennings.

#Mills 536-SP-1
M536SP1 = ['C','R','P','C','P','O','C','B','P','C','L','O','C','L','P','C','L','O','C','P']

#Mills 536-SP-2
M536SP2 = ['R','O','C','B','C','O','C','P','C','O','B','O','P','O','C','R','B','C','O','C']

#Mills 536-SP-3
M536SP3 = ['O','L','P','B','O','L','P','O','B','P','L','O','P','O','R','L','P','O','B','L']

# Symbol Legend
# R - BAR
# B - Bell
# P - Plum
# O - Orange
# L - Lemon
# C - Cherry

# Mills 108 Pay card "Fruit King"
M108PC = {
"R-R-R": 20,
"C-C-C": 12,
"C-C-B": 8,
"C-C-L": 4,
"C-C-R": 2,
"C-C-O": 2,
"C-C-P": 2
}

# Mills 102 Pay Card (C-C-* not implemented)
M102PC = {
"R-R-R": 20,
"B-B-B": 16,
"B-B-R": 16,
"P-P-P": 12,
"P-P-R": 12,
"O-O-O": 8,
"O-O-R": 8,
"C-C-L": 4,
"C-C-B": 4
}

# This class simulates the slot machine hardware and operation.
class Machine:
    def __init__(self):
        self.pulls = 0
        self.credits = 80
        self.bet = 0
        self.jackpot = 20
        self.test = False
        self.jphits = 0
        self.jackpotPayline = "R-R-R" # Jackpot pyline should come from the pay card.
        self.reels = []
        self.paycard = None
        self.payline = ""
        self.paid = 0

    def pull(self):
        result = ""
        for reel in self.reels:
            result += random.choice(reel)
            result += '-'

        self.pulls += 1
        self.payline = result[:-1]

    def pay(self):
        if self.payline in self.paycard:
            paid = self.paycard[self.payline]
            if not self.test:
                self.credits += paid
            self.paid += paid

        if self.payline == self.jackpotPayline:
            self.jphits += 1
            self.paid += self.jackpot
            if not self.test:
                self.credits += self.jackpot

    def play(self):
        if not self.test:
            if self.credits > 0:
                self.credits = self.credits - self.bet

        self.pull()
        self.pay()


# Create a new slot machine.
m = Machine()

# Install the reels.
m.reels.append(M536SP1)
m.reels.append(M536SP2)
m.reels.append(M536SP3)

# Attach the award payout card.
m.paycard = M102PC

# Default bet is one coin.
m.bet = 1

stats = {}
m.test = False
testlength = 1000000

if not m.test:
    print(f"Auto play mode. {m.credits} credits.")
else:
    print(f"Test mode. {testlength} pulls.")

while True:
    m.play()
    if m.payline in m.paycard:
        if m.payline in stats:
            stats[m.payline] += 1
        else:
            stats[m.payline] = 1

    if m.test:
        if m.pulls == testlength:
            break
    else:
        if m.credits == 0:
            break

print(f"Stats after {m.pulls} pulls:")
print(json.dumps(stats))
print(f"{m.pulls} coins bet, {m.paid} coins paid. {round((m.paid/m.pulls) * 100,1)}% payback")


