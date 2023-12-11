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
Easy problem today. Can be optimised by totalling each axis independently.
