import random 

def gp_co(p1, p2):
    
    p1, p2 = p1.geno.split('('), p2.geno.split('(')
    
    #select co point
    
    co_point = random.choice(list(range(len(p1))))
    
    if len(p1) <= co_point:
    
        off2 = p1
    
    else:
        
        off2 = p2[:co_point] + p1[co_point:]
    
    if len(p2) <= co_point:
        
        off1 = p2
        
    else:
        
        off1 = p1[:co_point] + p2[co_point:]
    
    
    
    return '('.join(off1), '('.join(off2)

