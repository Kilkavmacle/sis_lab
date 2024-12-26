
import pandas 
import numpy 

def entropy(prob):
    return -numpy.sum(prob * numpy.log2(prob), where=(prob > 0))

def conditional_entropy(j_prob, c_prob):
    v_prob = (j_prob > 0) & (c_prob > 0)
    return -numpy.sum(j_prob[v_prob] * numpy.log2(c_prob[v_prob]))

def task(dt):
    
    count = dt.values.sum()
    j_prob = dt / count  
    m_prob_A = j_prob.sum(axis=1)  
    m_prob_B = j_prob.sum(axis=0) 
    
    H_AB = entropy(j_prob.values.flatten())
    H_A = entropy(m_prob_A.values)
    H_B = entropy(m_prob_B.values)
    
    c_prob = j_prob.div(m_prob_A, axis=0)
    Ha_B = conditional_entropy(j_prob.values.flatten(), c_prob.values.flatten())
    
    I_AB = H_A + H_B - H_AB
    
    return [float(round(H_AB, 2)), float(round(H_A, 2)), float(round(H_B, 2)), float(round(Ha_B, 2)), float(round(I_AB, 2))]


if __name__ == "__main__":
    dt = pandas.read_csv('./task4/task4.csv', index_col=0)
    res = task(dt)
    print(res)
