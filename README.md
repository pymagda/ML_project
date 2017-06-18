### Road signs recognition

Recognition of the traffic signs (turn right, turn left, go straight).
Based on the publication: http://www.sciencedirect.com/science/article/pii/S0921889012001236.

### Movie

See the test movie in .mp4 format.
Tested with MindStorm robot.

### Test accuracy

Get random set of three signs, test accuracy.
Parameters from the publication HOG (Table.2), Classifiers (Table.6).
HOG2: Cell 5x5, Block 10x10
HOG3: Cell 4x4, Block 8x8
CLS1: Random Forrest
CLS2: K-d tree

| HOG      | CLS           | Accuracy  |
| ------------- |:-------------:| -----:|
| HOG2    | CLS1 | 80% |
| HOG2      | CLS2     | 90%    |
| HOG3 | CLS1     |  80%   |
| HOG3 | CLS2      |    80% |

