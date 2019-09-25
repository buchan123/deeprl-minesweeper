
# coding: utf-8

# In[2]:


import gym
import gym_minesweeper
env = gym.make('minesweeper-v0')


# In[1]:


import numpy as np
import gym
import keras


from keras.models import *
from keras.layers import *
from keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.policy import EpsGreedyQPolicy
from rl.memory import SequentialMemory


# In[3]:


np.random.seed(123)
env.seed(123)

nb_actions = env.action_space[0].n + env.action_space[1].n


# In[4]:


'''observation = env.reset()
for t in range(100):
        env.render()
        action = env.action_space.sample()
        (observation, reward, done, info) = env.step(action)
        print (observation, reward, done, info, action)
        print()
        if done:
            print("Finished after {} timesteps".format(t+1))
            break
'''

# In[12]:


def nn_model():
    model = Sequential()
    model.add(Flatten(input_shape=(1,) + env.observation_space.shape))
    model.add(Dense(50))
    model.add(Activation('relu'))
    model.add(Dense(50))
    model.add(Activation('relu'))
    model.add(Dense(50))
    model.add(Activation('relu'))
    model.add(Dense(100))
    
    return model


# In[13]:


model = nn_model()
model.summary()


# In[21]:


policy = EpsGreedyQPolicy()
memory = SequentialMemory(limit=50000, window_length=1)
dqn = DQNAgent(model=model,nb_actions = 100, memory=memory, nb_steps_warmup=100,
target_model_update=1e-3, policy=policy)
dqn.compile(Adam(lr=1e-4), metrics=['mae'])

# Okay, now it's time to learn something! We visualize the training here for show, but this slows down training quite a lot. 
history = dqn.fit(env, nb_steps=100000, visualize=False, verbose=1)


# In[19]:


print(history)


# In[20]:


dqn

