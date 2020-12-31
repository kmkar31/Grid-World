# Grid-World
An Approach to solving a single agent grid-world using Reinforcement Learning

### Rewards

* Finding a Goal - Reward of +30
* Terminating in a Non-Goal State - Penalty of 15
* Making a move - Penalty of 0.3

### Hyperparameters

* Gamma - 0.9
* Alpha - 0.5
* Softmax temperature - 1
* Epsilon - 0.15

Since the maximum moves an agent should take to reach the goal in the worst case in a 10x10 grid is 20, the return from such a trial must be **greater than 1.012**. 
This is obtained by writing the Return G(t) as R<sub>0</sub> + &gamma;R<sub>1</sub> + ....... + &gamma;<sup>t-1</sup>R<sub>t</sub>. 
At the 21st step a reward of 30 is obtained. 

***So the Objective would be to ensure that the every trial yields a return of atleast 1.012***


## Tabular Q-Learning

In this approach, Q-Learning is run without using function approximators i.e., the value of each state is stored using a Lookup Table.

For a 10x10 grid, there are 100 possible states the agent can be in. There are 10,000 possible combinations of start and goal states (they are allowed to coincide)
Combined with 5 different actions [ Left, Right, Up, Down and armEngage (serves as a non-moving action. In a taxi-world, it would represent picking up and dropping off a passenger)],
there are **1 million** states. So the Q[s][a] would be a matrix with 5 million elements. Therefore, this method does not scale well. It is however a basic entry point.

### Results

  * #### Actions Selected according to Softmax:
      