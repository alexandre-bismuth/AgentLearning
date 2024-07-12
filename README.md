# Queue Simulation and Agent Learning Project

*Code written by Alexandre Bismuth in a project on Policy Learning with Professor Itai Ashlagi, Professor Itai Gurvich, and Professor Qiaomin Xie*

The project can be divided as follows:

## 1. Simulating a queue with agents to service

In this first part of the project, we define a class for agents and a class for queue which will allow us to test multiple hand designed servicing strategies and to observe the total and discounted reward obtained from it after a large number of iterations. More details can be found on the QueueSimulation.ipynb notebook where the code is explained throughout.

## 2. Developing a Reinforcement Learning Agent in order to find the best strategy through Q-Learning

In this second part of the project, we create a Q-Learning environment in order to remodel the problem using the OpenAI gymnasium library. We therefore define the same types of agents, model our Queue as a learning Environment, and have to define a new kind of Agent (which we denote QAgent) that will be in charge of selecting a serivicing strategy and refining it using a Q-Learning algorithm in order to obtain the highest possible reward. More details can be found on the QAgent.ipynb notebook where the code is explained throughout.
