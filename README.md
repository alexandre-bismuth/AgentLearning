# Queue Simulation and Agent Learning Project

*Code written by Alexandre Bismuth in a project on Policy Learning with Professor Itai Ashlagi, Professor Itai Gurvich, and Professor Qiaomin Xie*

## Step-by-Step implementation

### 1. Simulating a queue with agents to service

In this first part of the project, we define a class for agents and a class for queue which will allow us to test multiple hand designed servicing strategies and to observe the total and discounted reward obtained from it after a large number of iterations. More details can be found on the QueueSimulation.ipynb notebook where the code is explained throughout. To get a better comprehension of the overall system and implementation, running GUISimulation.ipynb will help, giving you a functional graphical interface which will allow you to play the simulation manually.

### 2. Developing a Reinforcement Learning Agent in order to find the best strategy through Q-Learning

In this second part of the project, we create a Q-Learning environment in order to remodel the problem using the OpenAI gymnasium library. We therefore define the same types of agents, model our Queue as a learning Environment, and have to define a new kind of Agent (which we denote QAgent) that will be in charge of selecting a serivicing strategy and refining it using a Q-Learning algorithm in order to obtain the highest possible reward. More details can be found on the QAgent.ipynb notebook where the code is explained throughout.

## Hyper-parameter tuning

Through testing, we can find which hyper-parameters are best in which kinds of situation. These results are experimental findings which should serve as guidance and should not be considered as undeniable rules:

- *\[TO BE DONE\]*

## Next steps

- [X] Optimize code to improve training speed by looking for inefficiencies
- [X] Improve Q-table completeness by studying different methods of training (i.e. variable truncation values)
- [ ] Think about how to extrapolate results to unexplored states
  - [X] Convert Q_table into a priority list which is state-indepdendent
  - [ ] Perform a Linear regression on the Q_table in order to expand Q_table values to a large amount of states (which requires us to suppose identical and constant/linear penalty functions)
