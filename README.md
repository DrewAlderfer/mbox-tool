# Mbox Splitting Tool

Hello! This is a simple tool I wrote to split an mbox file into parts of
roughly equal byte-length. I needed to transfer a bunch of old emails and
didn't trust using something that required sending a bunch of unencrypted
personal info to a website to split it up.

This was a quick one day-ish project that let me dig into mbox files and learn
some Python tricks I hadn't ever had a need to use (like measuring string
length in bytes). It also gave me an opportunity to write a simple 'bin
packing' algorithm. This part was the most fun, and even though my solution is
probably somewhat naive it felt like a good solution.

The problem is how to split up a stack of emails so that each stack is as
close to the maximum file size possible. In my case it was 30MiB. What I found
quickly was that a simple linear splitting (going along the stack and
splitting it each time it passed the 30MiB threshold) resulted in a pretty
sub-optimal set of stacks since there was a lot of variation in the size of
individual emails.

To optimize the stacks and minimize the number of files created I first split
the stack into smaller stacks. The size of the stacks is a hyper-parameter of
the algorithm. Something that would be interesting to do in the future to make
this more of an ML approach would be to have the program search for the optimal stack
size to start with. I have a feeling that the way I handle the sorting after
this part means that the smaller the original stacks (down to just single
email stacks) would result in better bin fitting. However, other things could
be optimized for like speed of sorting vs. mean distance from the target file
size.

Once I have the small stacks I need to start combining them. To do this I
calculate the distance from the target threshold of the combination of each
stack with each of the other stacks and score them based on that error. The
combination with the least amount of error gets combined and then I repeated
the calculation and combination steps until a single pair is left. When
calculating the size of each combination any combination that exceeds the
threshold is discarded leaving only valid combinations at each iteration.

Compared to the linear accumulation and splitting approach this method
improved the mean distance error from ~5500KiB to just 160KiB.

There are definitely a lot of optimizations that could be added, but as it is
I got my emails split up pretty quick and will look for more interesting
datasets to expand on some of the ideas here. Ultimately, this was developed
as a practical script for a practical purpose. However, I always like an
opportunity to learn more about programming for productivity and getting
familiar with basic concepts in computing. While I'm sure my bin packing
solution isn't revolutionary it was fun to spend a few hours working out the
specifics of solving this kind of problem.

An actual TODO would be to refactor the code into a command line tool. This
would just require adding the argeparse bits and adding a main() function. As
it stands it's just a collection of functions. I used a Jupyter Notebook for
as a repl for debugging and running the final code.

Thanks for reading.
