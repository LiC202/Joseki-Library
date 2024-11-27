# Joseki Library
A desktop app in python that stores and interacts with a library of Joseki for the game of Go.   
Made over the course of 4 weeks as part of the TECS competition in Ireland.
# General Info
For those who don't know the game of Go, you'll have to look it up somewhere else.  
For those who do but haven't heard of Joseki before, it's pretty much the equivalent of an opening in Chess. The differences are that multiple can be played in a game since they're usually limited to a corner (of which there are obviously four). One other difference is that in Joseki, you have the option of Tenuki-ing, which means ignoring what your opponent did completely and playing somewhere else on the board. Because of the context dependant nature of playing Tenuki, I have added a button that "plays Tenuki", rather than you, the user, needing to play somewhere else specific.

# How To Use
Run main.py for the game to run. I'd recommend creating a shortcut and fiding the folder away somewhere.  

General Use:
* Click on the board to make a move, turns will alternate between black and white (black plays first).
* I haven't coded in the rule of Ko, since it's more work that will just make my code messier, and anyone who plays go will understand that it's not allowed regardless.
* For the same reasons, you're still able to place a stone where it would be captured instantly.
* Any Joseki you save will be saved in all four corners, in each possible reflection.
* Unless in test-mode (we'll get there shortly), green dots will be placed in any of your available next moves, according to the Joseki that you have already saved (you start with none).  

Buttons:
* UNDO MOVE - Undoes the last move you made. This will also work after answering a test question to go even earlier in the Joseki than you began.
* CLEAR ALL - Clears the board.
* SAVE JOSEKI - Saves the current position as a new Joseki (if it doesn't already have it saved). It will be saved in 8 permutations, one for each reflection and each corner. If you want to you can even save an entire game rather than just a Joseki.
* DELETE JOSEKI - Deletes all permutations of whatever joseki you have played on the board.
* TENUKI - Notes in the move sequence that the opponent has played a move somewhere else.
* TEST - My magnum opus, when clicked you'll be given a random Joseki at a random point through the sequence, as well as a stone in the TEST square telling you who's move it is. You'll then respond with a move, and if that move is one of the possible moves (according to what you have saved), the move will be played and you'll be shown the following moves if you want to continue. If you get it wrong, the move won't play and you'll be shown what the possible correct moves were. After responding, you'll have to click the button again to be presented with a new problem.  

Sample Joseki:  
For anyone who doesn't know enough about Go to play their own Joseki, but still wants to be able to see the functionality of the app.  

```txt
c04e04e03f03d03f04d06k04
q03q05r05r06r04q06o04q10
r16p16p17o17q17o16q14k16
d17d15c15c14c16d14f16d10
d03d05c05c06c04d06f04d10
c16e16e17f17d17f16d14k16
q17q15r15r14r16q14o16q10
r04p04p03o03q03o04q06k04
c04e04e03f03d03f04d06k03
q03q05r05r06r04q06o04r10
r16p16p17o17q17o16q14k17
d17d15c15c14c16d14f16c10
d03d05c05c06c04d06f04c10
c16e16e17f17d17f16d14k17
q17q15r15r14r16q14o16r10
r04p04p03o03q03o04q06k03
c04e04e03f03d03f04c06k04
q03q05r05r06r04q06o03q10
r16p16p17o17q17o16r14k16
d17d15c15c14c16d14f17d10
d03d05c05c06c04d06f03d10
c16e16e17f17d17f16c14k16
q17q15r15r14r16q14o17q10
r04p04p03o03q03o04r06k04
c04e04e03f03d03f04c06k03
q03q05r05r06r04q06o03r10
r16p16p17o17q17o16r14k17
d17d15c15c14c16d14f17c10
d03d05c05c06c04d06f03c10
c16e16e17f17d17f16c14k17
q17q15r15r14r16q14o17r10
r04p04p03o03q03o04r06k03
d04c06c05d06f04d10
q04o03p03o04q06k04
q16r14r15q14o16q10
d16f17e17f16d14k16
d04f03e03f04d06k04
d16c14c15d14f16d10
q16o17p17o16q14k16
q04r06r05q06o04q10
d04c06c05d06f04c10
q04o03p03o04q06k03
q16r14r15q14o16r10
d16f17e17f16d14k17
d04f03e03f04d06k03
d16c14c15d14f16c10
q16o17p17o16q14k17
q04r06r05q06o04r10
d04c06c05d06f03d10
q04o03p03o04r06k04
q16r14r15q14o17q10
d16f17e17f16c14k16
d04f03e03f04c06k04
d16c14c15d14f17d10
q16o17p17o16r14k16
q04r06r05q06o03q10
d04c06c05d06f03c10
q04o03p03o04r06k03
q16r14r15q14o17r10
d16f17e17f16c14k17
d04f03e03f04c06k03
d16c14c15d14f17c10
q16o17p17o16r14k17
q04r06r05q06o03r10
d04c03c04d03e03e02f03f02g03b04b05b03c06
q04r03q03r04r05s05r06s06r07q02p02r02o03
q16r17r16q17p17p18o17o18n17s16s15s17r14
d16c17d17c16c15b15c14b14c13d18e18c18f17
d04c03d03c04c05b05c06b06c07d02e02c02f03
d16c17c16d17e17e18f17f18g17b16b15b17c14
q16r17q17r16r15s15r14s14r13q18p18r18o17
q04r03r04q03p03p02o03o02n03s04s05s03r06

```
[Paste that into the joseki.txt file in the 'game' folder. Make sure to include an extra empty line at the bottom or it won't work]

# Brief Reflection
This is the first project involving a GUI that I've ever made without relying on someone else's tutorial. I thought I would hate the front-end development but I actually really enjoyed it in the end.  
Some things I struggled with:
1. I had a lot of issues with using pygame since I hadn't had much experience with it before, but I feel like I got the hang of it towards the end and really learned a lot.
2. Problem solving was the most fun part of the project, but also where the most went wrong. Figuring out how to capture stones took the longest and had by far the most bugs surrounding it, but they did all get worked out eventually.
3. Working across multiple different files was also tough at first, but became easy pretty quickly.
4. I also had to learn how to use github for this project.
5. Designing the app and coming up with ideas in the first place was a bit harder than I had expected, still not bad though.
6. My code is completely abhorrent. I originally made a version that ran from the console before doing any UI, and so at the end I had to delete around 150 lines of obsolete code. I was also left with a sytem of storing move sequences that looks like this: d03d05c05c06c04d06f04d10. That alone is fine, except it has to be converted to a list like this: ["d03", "d05", "co5", ...], and the moves have to be converted to this: "d03" => (3, 3), and throw in the fact that an option for a move is written as "TEN", I basically ended up with maybe 7 or 8 functions whose sole purposes were to translate between these formats, when i could've easily stored them in (3, 3) form if I had thought ahead more, or had the time and energy to go back and fix it across the 400+ lines of code.  

Despite all these problems I never felt like I was doing a chore, I always enjoyed finding new solutions to problems I didn't know I would have, and coming up with solutions to a problem in school, even if that problem was 4 problems down the line.
