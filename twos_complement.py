
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
import nengo


# In[2]:


def flip_bits(input_bit):
    if(0.5 <= input_bit < 1.5):
        return 0
    return 1


# In[5]:


def twos_comp(input2):
    exponent2_bits = input2
    exponent_len = len(exponent2_bits)-1
    while exponent2_bits[exponent_len]!=1:
        exponent_len-=1
    exponent_len-=1
    model = nengo.Network()

    with model:
        exponent2_nodes = [] 
        for i in range(exponent_len+1):
            exponent2_nodes.append(nengo.Node(output = exponent2_bits[i]))
        flipping_ensembles = []
        for i in range(exponent_len+1):
            flipping_ensembles.append(nengo.Ensemble(n_neurons = 200, dimensions = 1, radius = 2))
        for i in range(exponent_len+1):
                nengo.Connection(exponent2_nodes[i], flipping_ensembles[i])
        output_ensembles = []
        for i in range(exponent_len+1):
            output_ensembles.append(nengo.Ensemble(n_neurons = 200, dimensions = 1, radius = 2))
            nengo.Connection(flipping_ensembles[i], output_ensembles[i], function = flip_bits)
        flip_probes = []

        for i in range(exponent_len+1):
            flip_probes.append(nengo.Probe(output_ensembles[i], synapse = 0.01))

    with nengo.Simulator(model) as sim:
        sim.run(5.0)
        exponent2_string = "Mantissa : "
        input2s_comp=[]
        for i in range(exponent_len+1):
            #input2.append(exponent2_bits[i - 1])
            #exponent2_string = exponent2_string + str(exponent2_bits[i])
            j = np.mean(sim.data[flip_probes[i]])
            input2s_comp.append(int(j))
        exponent_len+=1
        while exponent_len!=len(exponent2_bits):
            input2s_comp.append(int(exponent2_bits[exponent_len]))
            exponent_len+=1

        #print(exponent2_string)
        return input2s_comp

