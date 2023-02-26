## TODO list


### Game play
- [ ] Drop speed based on number of lines (all times based on frame hz?)
- [ ] Music (must include a version of Korobeiniki)
- [ ] Delayed auto shift (10 frames (= 167 millis/6Hz))
- [ ] Auto-repeat rate (2 frames (= 33 millis/30Hz))
- [ ] Wall kicks
- [ ] Shadow pieces


### UI
- [ ] Score display
- [ ] Next piece
- [ ] Menu


## Drop speed recommendations

This is the speed curve, based on Tetris Worlds, where 1G = 1 cell/frame
Level  	Speed
        (unit: G)
1	      0.01667    (1000ms @ 16.6ms frame delay)
2	      0.021017
3	      0.026977
4	      0.035256
5	      0.04693
6	      0.06361
7	      0.0879
8	      0.1236
9	      0.1775
10	    0.2598
11	    0.388
12	    0.59
13	    0.92
14	    1.46
15	    2.36
16	    3.91
17	    6.61
18	    11.43
19	    20


