from conn import queue

Q = queue.FuhbuhQueue()

Q.connect(None, "raiders")
Q.connect(None, "raiders")


print("First play:")
Q.player1.makeCall("End Run")
Q.player2.makeCall("Standard")

print("Second play:")
Q.player2.makeCall("Blitz")
Q.player1.makeCall("Long")
