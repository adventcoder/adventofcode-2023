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
