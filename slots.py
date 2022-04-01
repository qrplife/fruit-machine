# This is the main game file for slot machine simulation.
import json
import mills

# Create a new slot machine.
m = mills.Machine()

# Install the reels.
m.reels.append(mills.M536SP1)
m.reels.append(mills.M536SP2)
m.reels.append(mills.M536SP3)

# Attach the award payout card.
m.paycard = mills.M102PC

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
print(f"{m.pulls} coins bet, {m.paid} coins paid. {round((m.paid/m.pulls) * 100,1)}% payback.")

