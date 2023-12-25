# adventofcode-2023

Here are some daily (probably stupid) thoughts. Started after day 6. 

Day 1:
Mostly just fighting against the standard library that seems very lacking in this area.
I don't want to have to write a lot of code for day1, so it's just hacked.

Day 2:
Both parts can be solved in the iteration order directly from parsing the input without having to store anything.

Day 3:
Messy grid lookups. The number of grid lookups could be easily optimised further by iterating the number boundary in aggregate instead of the boxes around each digit, but I didn't want to write more code.

Day 4:
Not much to say about this one.

Day 5:
Took me far too long to realise I should separate the loop over intervals and the gaps to make things cleaner. At least they were non-overlapping. This was still difficult for a day 5. Could be optimised slightly by doing some bsearch lookups but not worth bothering.

Day 6:
Just a quadratic equation. Past years have had more difficult problems to find the analytical solution. We're having more intersting questions earlier this year it seems, but easier versions of them.

Day 7:
I went straight to using the most common frequencies for type ordering. Joker logic is kind of messy. Even messier combining both parts of todays puzzle.

Day 8:
Jumped straight to LCM in total obliviousness, only to learn later that there are so many problems...

Day 9:
Extrapolating backwards wasn't much different than forwards. I was messing around with writing a little library for Newton Series recently so was ready for something more difficult.

Day 10:
Interesting problem today. I didn't want to deal with making flood fill work so eventually ended up solving it with horizontal scan lines keeping track of inside/outside which was easier than I thought it would be. Verticals are '|', 'F-*J', 'L-*7'. Rewrote later to use shoelace formula after looking at other solutions.

Day 11:
Easy problem today. Can be optimised by totalling each axis independently. Worked out a formula for summing over all the pairs and now the code is totally incomprehensible. Oh well.

Day 12:
Did it the obvious way. No idea how to make it faster. Feels like you could split on '.' and solve each subgroup separately, but idk if that would just be worse or not. Later started looking into using NFA's for the solution.

Day 13:
Just bruteforced it. Might return later.

Day 14:
Just implemented in an obvious way. Kind of slow. Probably won't revisit.

Day 15:
Just follow the overly wordy instructions. 

Day 16:
Brute forced again, and it's the slowest solution yet. Part 2 can probably be done more efficiently by detecting loops in the graph beforehand or something like that.

Day 17:
Optimised to keep track of the next 10 layers instead of a heap since the graph weights are always just single digits. It's more like BFS with extra layers than Djikstra. Still super slow. Could be optimised further by packing the state into an integer and using an array instead of dict.

Day 18:
Shoelace again. lol.

Day 21:
Another cycle detection puzzle very much tied to the specific patterns in the input. My solutions is extremely slow and not general at all.

Day 22:
Spent way too long cleaning this.

Day 23:
This is the slowest day so far. Nothing to do but brute force since it's NP-hard (for part 2 anyway). I didn't create the compressed graph originally, and it was still running by the time I got it implemented.

Day 24:
ARGH

Day 25:
An anticlimatic ending. I used graphwiz to solve. idk if I'll come back to this. Anyway merry Christmas.
