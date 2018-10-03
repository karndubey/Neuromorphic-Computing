
# coding: utf-8

# In[62]:


import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')
import nengo
import numpy as np


# In[63]:


def calculate_output_bit(vector):
    #print(vector)
    result = vector[0] + vector[1]
    if((0.5 < result <= 1.5) or (2.5 < result <= 3.5)):
        return 1
    return 0


# In[64]:


def calculate_carry_out(vector):
    result = vector[0] + vector[1]
    if((1.5 < result <= 2.5) or (2.5 < result <= 3.5)):
        return 1
    return 0


# In[65]:


input2=[1,1,1]


# In[70]:


def addition(input1):
    ans=0
    carry=0
    model = nengo.Network(label='Subtraction')
    with model:
        a_node=nengo.Node(output=input1[0]) 
        b_node=nengo.Node(output=input1[1])
        c_node=nengo.Node(output=input1[2])
        a_plus_b_ensembles=nengo.Ensemble(n_neurons=200,dimensions=1,radius=2)
        a_plus_b_plus_c_ensembles=nengo.Ensemble(n_neurons=400,dimensions=2,radius=2)
        sum_ensembles=nengo.Ensemble(n_neurons = 200, dimensions = 1, radius = 2)
        carry_ensembles=nengo.Ensemble(n_neurons = 200, dimensions = 1, radius = 2)
        nengo.Connection(a_node, a_plus_b_ensembles)
        nengo.Connection(b_node, a_plus_b_ensembles)
        nengo.Connection(a_plus_b_ensembles, a_plus_b_plus_c_ensembles[0])
        nengo.Connection(c_node, a_plus_b_plus_c_ensembles[1])
        nengo.Connection(a_plus_b_plus_c_ensembles, sum_ensembles, function = calculate_output_bit)
        nengo.Connection(a_plus_b_plus_c_ensembles, carry_ensembles, function = calculate_carry_out)
        sum_probe=nengo.Probe(sum_ensembles, synapse = 0.01)
        carry_probe= nengo.Probe(carry_ensembles, synapse = 0.01)
        with nengo.Simulator(model) as sim:
            # Run the model
            # Print probe values
            sim.run(5.0)
            error = 0
            j = np.mean(sim.data[sum_probe])
            ans=int(round(j))
            if (int(round(j)) == 1):
                error += 1 - j
            else:
                error += j   
            accuracy = 1 - (error/len(input1))
            carry = np.mean(sim.data[carry_probe])
            carry=int(round(carry))
            print(ans,carry)    
    return ans,carry
    


# In[71]:




# In[72]:




# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:



   

