import signal
import time
import sys
from collections import defaultdict
def count1(elem):
    return elem[7].count('1')

def count2(elem):
    return elem[0]

def count3(elem):
    ct = 0
    for i in elem:
        if i == '1':
            ct+=1
    return ct

def terminalState(common):
    if common:
        return False
    return True

def terminalState1(LAHSA):
    if not LAHSA:
        return True
    
def terminalState2(SPLA):
    if not SPLA:
        return True

def evaluateScore(LAHSA_beds, SPLA_parking_spaces,SPLA_only,LAHSA_only, n_beds, n_parking_spaces, node):
    global efficiencyspla, efficiencylahsa, ans
    efficiencyspla, efficiencylahsa = 0,0
    z = []
    if len(SPLA_only):
        SPLA_only.sort(key=count1, reverse= True)
        i = 0
        while i < len(SPLA_only):
            c = []
            for k,j in enumerate(SPLA_only[i][7]):
                c.append (SPLA_parking_spaces[k]-int(j))
            if (-1 not in c):
                SPLA_parking_spaces = c
                z.append(SPLA_only[i])
            i += 1
    for i in SPLA_parking_spaces:
        efficiencyspla += (n_parking_spaces - i)
    
    p = []
    if len(LAHSA_only):
        LAHSA_only.sort(key=count1, reverse= True)
        i = 0
        while i<len(LAHSA_only):    #for i in range (len(LAHSA_only)):
            c = []
            for k,j in enumerate(LAHSA_only[i][7]):
                c.append(LAHSA_beds[k]-int(j))
            if (-1 not in c):
                LAHSA_beds = c
                p.append(LAHSA_only[i])
            i += 1
    
    for i in LAHSA_beds:
        efficiencylahsa += (n_beds - i)
    
    if len(z):
        i = 0
        while i<len(z):
            for k,j in enumerate(z[i][7]):
                SPLA_parking_spaces[k]+=int(j)
            i += 1
                
    if len(p):
        i = 0
        while i <len(p):
            for k,j in enumerate(p[i][7]):
                LAHSA_beds[k]+=int(j)
            i += 1
    return (efficiencyspla,efficiencylahsa)

def maxSpla(common, LAHSA_beds, SPLA_parking_spaces, n_beds, n_parking_spaces, LAHSA_only, SPLA_only, currentDepth, node):
    if terminalState(common):
        return evaluateScore(LAHSA_beds, SPLA_parking_spaces,SPLA_only,LAHSA_only, n_beds, n_parking_spaces, node)
    ans = []
    vs = -sys.maxsize
    vl = -sys.maxsize
    global t
    vsprev = vs
    vlprev = vl
    for i in common[:]:
        q = [[]]
        q = i 
        c = []
        for k,j in enumerate(q[7]):
            c.append (SPLA_parking_spaces[k]-int(j))
        if (-1 not in c):
                SPLA_parking_spaces = c
        else:
            continue
        common.pop(common.index(i))
        s,l = maxLahsa(common, LAHSA_beds, SPLA_parking_spaces, n_beds, n_parking_spaces, LAHSA_only, SPLA_only, currentDepth+1, node)
        if s>vs:
            vs = s
            vl = l
        common.append(q)
        if (len(common) == comlen):
            t.append([common[-1][0],s,l])
        for k,j in enumerate(q[7]):
            SPLA_parking_spaces[k] += int(j)

    if(vs== vsprev and vl  == vlprev):
        return evaluateScore(LAHSA_beds, SPLA_parking_spaces,SPLA_only,LAHSA_only, n_beds, n_parking_spaces, node)
    return vs,vl

def maxLahsa(common, LAHSA_beds, SPLA_parking_spaces, n_beds, n_parking_spaces, LAHSA_only, SPLA_only, currentDepth, node):
    if terminalState(common):
        return evaluateScore(LAHSA_beds, SPLA_parking_spaces,SPLA_only,LAHSA_only, n_beds, n_parking_spaces, node)
    vs = -sys.maxsize
    vl = -sys.maxsize
    vsprev = vs
    vlprev = vl
    for i in common[:]:
        q = [[]]
        q= i 
        flag = 0
        c = []
        for k,j in enumerate(q[7]):
            c.append (LAHSA_beds[k]-int(j))
        if (-1 not in c):
                LAHSA_beds = c
        else:
            continue
        common.pop(common.index(i))
        s,l = maxSpla(common, LAHSA_beds, SPLA_parking_spaces, n_beds, n_parking_spaces, LAHSA_only, SPLA_only, currentDepth+1, node)
        if l>vl:
            vl = l
            vs = s
        common.append(q)
        for k,j in enumerate(q[7]):
            LAHSA_beds[k]+=int(j)

    if(vs== vsprev and vl  == vlprev):
        return evaluateScore(LAHSA_beds, SPLA_parking_spaces,SPLA_only,LAHSA_only, n_beds, n_parking_spaces, node)
    return vs,vl

def calc(ans):
    ans.sort()
    global selected_ones_common
    for x in ans:
        if (sp == x[1] and la == x[2]):
            selected_ones_common.append(x[0])

def calc1(ans1):
    ans1.sort()
    global selected_ones
    for x in ans1:
        if (sp == x[1] and la == x[2]):
            selected_ones.append(x[0])

def evaluateScore1(LAHSA_beds, SPLA_parking_spaces,SPLA, LAHSA, n_beds, n_parking_spaces, node, agent):
    global efficiencyspla1, efficiencylahsa1, ans1
    efficiencyspla1, efficiencylahsa1 = 0,0
    if (agent == 0):
        z = []
        if len(SPLA):
            SPLA.sort(key=count1, reverse= True)
            i = 0
            while i < len(SPLA):
                c = []
                for k,j in enumerate(SPLA[i][7]):
                    c.append (SPLA_parking_spaces[k]-int(j))
                if (-1 not in c):
                    SPLA_parking_spaces = c
                    z.append(SPLA[i])
                i += 1
        for i in SPLA_parking_spaces:
            efficiencyspla1 += (n_parking_spaces - i)
        for i in LAHSA_beds:
            efficiencylahsa1+= (n_beds - i)
        if len(z):
            for i in range (len(z)):
                for k,j in enumerate(z[i][7]):
                    SPLA_parking_spaces[k]+=int(j)        
    
    elif (agent == 1):
        p = []
        if len(LAHSA):
            i = 0
            while i < len(LAHSA):
                c = []
                for k,j in enumerate(LAHSA[i][7]):
                    c.append(LAHSA_beds[k]-int(j))
                if (-1 not in c):
                    LAHSA_beds = c
                    p.append(LAHSA[i])
                i += 1    
        for i in SPLA_parking_spaces:
            efficiencyspla1 += (n_parking_spaces - i)
        for i in LAHSA_beds:
            efficiencylahsa1 += (n_beds - i)
        if len(p):
            for i in range (len(p)):
                for k,j in enumerate(p[i][7]):
                    LAHSA_beds[k]+=int(j)

    return (efficiencyspla1,efficiencylahsa1)

def maxSpla2(LAHSA, SPLA, LAHSA_beds, SPLA_parking_spaces, n_beds, n_parking_spaces, currentDepth, node):
    vs = -sys.maxsize
    vl = -sys.maxsize
    global t1
    vsprev = vs
    vlprev = vl
    if terminalState1(LAHSA):
        return evaluateScore1(LAHSA_beds, SPLA_parking_spaces,SPLA, LAHSA, n_beds, n_parking_spaces, node, 0)
    
    if not SPLA:
        s,l = maxLahsa2(LAHSA, SPLA, LAHSA_beds, SPLA_parking_spaces, n_beds, n_parking_spaces, currentDepth, node)
        if s>vs:
            vs = s
            vl = l
    for i in SPLA[:]:
        q = [[]]
        q= i
        counter = 0
        if q in LAHSA:
            counter=1
        
        c = []
        for k,j in enumerate(q[7]):
            c.append (SPLA_parking_spaces[k]-int(j))
        if (-1 not in c):
                SPLA_parking_spaces = c
        else:
            continue
        if not counter:
            SPLA.pop(SPLA.index(i))
        else:
            SPLA.pop(SPLA.index(i))
            LAHSA.pop(LAHSA.index(i))
        s,l = maxLahsa2(LAHSA, SPLA, LAHSA_beds, SPLA_parking_spaces, n_beds, n_parking_spaces, currentDepth+1, node)
        
        if s>vs:
            vs = s
            vl = l
        
        if counter == 1:
            SPLA.append(q)
            LAHSA.append(q)
        else:
            SPLA.append(q)
        if len(SPLA) == splalen:
            t1.append([SPLA[-1][0],s,l])
        counter = 0
        for k,j in enumerate(q[7]):
            SPLA_parking_spaces[k] += int(j)
    if vs== vsprev and vl  == vlprev:
        return evaluateScore1(LAHSA_beds, SPLA_parking_spaces,SPLA, LAHSA, n_beds, n_parking_spaces, node, 1)
    return vs,vl 

def maxLahsa2(LAHSA, SPLA, LAHSA_beds, SPLA_parking_spaces, n_beds, n_parking_spaces, currentDepth, node):
    vs = -sys.maxsize
    vl = -sys.maxsize
    vsprev = vs
    vlprev = vl
    if terminalState2(SPLA):
        return evaluateScore1(LAHSA_beds, SPLA_parking_spaces, SPLA, LAHSA, n_beds, n_parking_spaces, node, 1)
    if not LAHSA:
        s,l = maxSpla2(LAHSA, SPLA, LAHSA_beds, SPLA_parking_spaces, n_beds, n_parking_spaces, currentDepth, node)
        if l>vl:
            vs = s
            vl = l
    for i in LAHSA[:]:
        q = [[]]
        q= i 
        counter = 0
        if q in SPLA:
            counter=1
        c = []
        for k,j in enumerate(q[7]):
            c.append(LAHSA_beds[k]-int(j))
        if -1 not in c:
                LAHSA_beds = c
        else:
            continue
        if counter == 0:
            LAHSA.pop(LAHSA.index(i))
        else:
            SPLA.pop(SPLA.index(i))
            LAHSA.pop(LAHSA.index(i))
        s,l = maxSpla2(LAHSA, SPLA, LAHSA_beds, SPLA_parking_spaces, n_beds, n_parking_spaces, currentDepth+1, node)
        if l>vl:
            vs = s
            vl = l
        if counter == 1:
            SPLA.append(q)
            LAHSA.append(q)
        else:
            LAHSA.append(q)
        counter = 0
        for k,j in enumerate(q[7]):
            LAHSA_beds[k] += int(j)

    if(vs== vsprev and vl  == vlprev):
        return evaluateScore1(LAHSA_beds, SPLA_parking_spaces, SPLA, LAHSA, n_beds, n_parking_spaces, node, 0)
    return vs,vl

def handler1(signum, frame):
    global file_out
    file_out.write(str(chosen))
    file_out.close()
    exit()

def main():
    global start_time, file_out
    start_time = time.time()
    signal.signal(signal.SIGALRM, handler1)
    signal.alarm(175)
    file = open("input.txt", "r")
    file_out = open("output.txt", "w")
    lines = file.readlines()

    n_beds = int(lines[0])
    LAHSA_beds = [n_beds]*7
    beds = [n_beds]*7
    n_parking_spaces = int(lines[1])
    SPLA_parking_spaces = [n_parking_spaces]*7
    parking_spaces = [n_parking_spaces]*7
    n_applicants_LAHSA = int(lines[2])
    LAHSA_applicants_so_far = []
    temp = 3
    for i in range(3,3+n_applicants_LAHSA):
        LAHSA_applicants_so_far.append(lines[i].rstrip())
        temp = temp+1
    n_applicants_SPLA = int(lines[temp])
    temp =temp+1
    temp2 = temp

    SPLA_applicants_so_far = []
    for i in range(temp2, temp2+n_applicants_SPLA):
        SPLA_applicants_so_far.append(lines[i].rstrip())
        temp = temp + 1

    n_applicants = int(lines[temp])
    temp = temp + 1

    applicants = [[] for i in range(n_applicants)]
    k = 0
    for line in lines[temp:]:
        
        line = line.rstrip()
        
        applicants[k].append(line[:5])
        applicants[k].append(line[5])
        applicants[k].append(line[6:9])
        applicants[k].append(line[9])
        applicants[k].append(line[10])
        applicants[k].append(line[11])
        applicants[k].append(line[12])
        applicants[k].append(line[13:])
        k = k+1
        
    applicants_remaining = []
    for i in applicants:
        if i[0] not in LAHSA_applicants_so_far and i[0] not in SPLA_applicants_so_far:
            applicants_remaining.append(i)
        elif i[0] in LAHSA_applicants_so_far:
            for j in range(7):
                LAHSA_beds[j] -= int(i[7][j])
        else:
            for j in range(7):
                SPLA_parking_spaces[j] -= int(i[7][j])

    LAHSA_only = []
    SPLA_only = []
    common = []
    SPLA = []
    LAHSA = []
    for i in (applicants_remaining):
        if i[1] == 'F' and int(i[2]) > 17 and i[3] == 'N':
            if i[4] == 'N' and  i[5] == 'Y' and i[6] == 'Y':
                common.append(i)
                SPLA.append(i)
                LAHSA.append(i)
            else:
                LAHSA_only.append(i)
                LAHSA.append(i)
        elif i[4] == 'N' and  i[5] == 'Y' and i[6] == 'Y':
            SPLA_only.append(i)
            SPLA.append(i)


    
    start_time = time.time()
    maxcount = []
    global sp,la, sp2,la2, chosen, selected_ones, selected_ones_common, person_chosen
    selected_ones_common = []
    selected_ones = []
    chosen = ''
    person_chosen = defaultdict(list)
    global comlen
    comlen = len(common)
    global splalen
    splalen = len(SPLA)
    SPLA.sort(key=count1, reverse = True)
    LAHSA.sort(key=count1, reverse=True)

    for i in SPLA_only:
        flag = 0
        j  = 0
        while j < 7:
            if SPLA_parking_spaces[j] - int(i[7][j]) < 0:
                flag = 1
                break
            j += 1
        if flag == 1:
            continue
        chosen = str(i[0])
        break

    if (common):
        sp ,la = maxSpla(common, LAHSA_beds, SPLA_parking_spaces, n_beds, n_parking_spaces, LAHSA_only, SPLA_only, 0, [])
        if t is not []:
            calc(t)
            if selected_ones_common != []:
                for i in selected_ones_common:
                    for j in common:
                        if i in j:
                            person_chosen[count3(j[7])].append(j)

                maxcount = person_chosen[sorted(person_chosen, reverse = True)[0]]
                chosen = str(maxcount[0][0])
    person_chosen = defaultdict(list)
    sp, la = maxSpla2(LAHSA, SPLA, LAHSA_beds, SPLA_parking_spaces, n_beds, n_parking_spaces, 0, [])
    if t1 is not []:
        calc1(t1)
        if selected_ones is not []:
            for i in selected_ones:
                for j in SPLA:
                    if i in j:
                        person_chosen[count3(j[7])].append(j)
            maxcount = person_chosen[sorted(person_chosen,reverse=True)[0]]
            chosen = str(maxcount[0][0])

    file_out.write(str(chosen))

t1 = []
t = []
ans1 = []    
ans = []
main()