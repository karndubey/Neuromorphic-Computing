
# coding: utf-8

# In[1]:


import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')
import nengo
import twos_complement as tc
import numpy as np


# In[2]:


def calculate_output_bit(vector):
    #print(vector)
    result = vector[0] + vector[1]
    if((0.5 < result <= 1.5) or (2.5 < result <= 3.5)):
        return 1
    return 0


# In[3]:


def calculate_carry_out(vector):
    result = vector[0] + vector[1]
    if((1.5 < result <= 2.5) or (2.5 < result <= 3.5)):
        return 1
    return 0


# In[4]:


s1=[0]
e1=[1,0,0,0,0,0,0,0]
m1=[0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
s2=[0]
e2=[1,0,0,0,0,1,1,0]
m2=[0,0,0,0,1,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0]


# ## Exponent Aligner

# In[5]:


def subtraction(input1, input2):
    input2s_comp=tc.twos_comp(input2)
    subtraction=[]
    flag=1
    print(input2s_comp)
    model = nengo.Network(label='Subtraction')
    with model:
    
        input1.reverse()
        input2s_comp.reverse()
        input1_nodes=[]
        input2_nodes=[]
        len(input1)
        for i in range(len(input1)):
            input1_nodes.append(nengo.Node(output = input1[i]))
            input2_nodes.append(nengo.Node(output = input2s_comp[i]))  
        c0=nengo.Node(output=0)
        a_plus_b_ensembles=[]
        a_plus_b_plus_c_ensembles=[]
        carry_ensembles=[]
        sum_ensembles=[]
        carry_ensembles.append(c0)

        for i in range(len(input1)):
            a_plus_b_ensembles.append(nengo.Ensemble(n_neurons=200,dimensions=1,radius=2))
            a_plus_b_plus_c_ensembles.append(nengo.Ensemble(n_neurons=400,dimensions=2,radius=2))
            sum_ensembles.append(nengo.Ensemble(n_neurons = 200, dimensions = 1, radius = 2))
            carry_ensembles.append(nengo.Ensemble(n_neurons = 200, dimensions = 1, radius = 2))

        for i in range(len(input1)):
            nengo.Connection(input1_nodes[i], a_plus_b_ensembles[i])
            nengo.Connection(input2_nodes[i], a_plus_b_ensembles[i])

        for i in range(len(input1)):
            nengo.Connection(a_plus_b_ensembles[i], a_plus_b_plus_c_ensembles[i][0])
            nengo.Connection(carry_ensembles[i], a_plus_b_plus_c_ensembles[i][1])
            nengo.Connection(a_plus_b_plus_c_ensembles[i], sum_ensembles[i], function = calculate_output_bit)
            nengo.Connection(a_plus_b_plus_c_ensembles[i], carry_ensembles[i+1], function = calculate_carry_out)
        sum_probes = []

        for i in range(len(input1)):
            sum_probes.append(nengo.Probe(sum_ensembles[i], synapse = 0.01))
        carry_out_probe = nengo.Probe(carry_ensembles[len(input1)], synapse = 0.01)
    with nengo.Simulator(model) as sim:
        # Run the model
        # Print probe values
        sim.run(5.0)
        error = 0
        for i in range(len(input1)):
            j = np.mean(sim.data[sum_probes[i]])
            subtraction.append(int(round(j)))
           # print("Sum Out " + str(i) + " " + str(j) + " " + str(int(round(j))))
        
            if (int(round(j)) == 1):
                error += 1 - j
            else:
                error += j   
        #print("Carry Out: " + str(np.mean(sim.data[carry_out_probe])))
        accuracy = 1 - (error/len(input1))
        #print("Accuracy: " + str(accuracy))
        subtraction.reverse()
        carry = np.mean(sim.data[carry_out_probe])
        print("Carry  ",int(round(carry)))
        print(subtraction)
        carry=int(round(carry))
        if(carry==0):
            # flag 0 means input1 is smaller than input2
            flag=0                 
        
    return subtraction, flag


# In[6]:



# In[ ]:


def take_twos_complement(flag,diff):
    if(flag==0):               
        diff=tc.twos_comp(diff)
    return diff

