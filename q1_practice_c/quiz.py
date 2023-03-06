# NO IMPORTS!

##################################################
### Problem 1: batch (12 min)
##################################################

def batch(inp, size):
    """ Return a list of batches, per quiz specification """
    
    result = []
    i = 0 
    while i != len(inp):
        batch = []
        while sum(batch) < size and i != len(inp):
            batch.append(inp[i])
            i+=1
        result.append(batch)
    return result


    

##################################################
### Problem 2: order (15min)
##################################################

def order(inp):
    """ Return an ordered list of string, per quiz specification """
    outp = []
    appended = []

    for i in range(len(inp)):
        initial = inp[i][0]
        if initial not in appended:
            appended.append(initial)
            outp.append(inp[i])
            for j in range(i+1, len(inp)):
                if inp[j][0] == initial:
                    outp.append(inp[j])
    
    return outp


##################################################
### Problem 3: path_to_happiness
##################################################

def path_to_happiness(field):
    """ Return a path through field of smiles that maximizes happiness """
    
    ncols = field['ncols']
    nrows =  field['nrows']
    smiles = field['smiles']

    # 建一个新的table，同样纬度
    table = [ [None] * ncols for _ in range(nrows) ]
    
    # 从第一列往后，逐渐填满表格，每一个cell储存：[parent offset -1/0/1, the total sum with parents] 
    for c in range(ncols):
        for r in range(nrows):
            if c == 0: # initialize first column 
                table[r][0] = [None, smiles[r][0]]
            else:
                parents = [[0, table[r][c-1][1] + smiles[r][c]]]      
                if r - 1 >= 0:
                    parents.append([-1, table[r-1][c-1][1] + smiles[r][c]]) 
                if r + 1 < nrows:
                    parents.append([1, table[r+1][c-1][1] + smiles[r][c]])
                max_parent = max(parents, key=lambda x: x[1])
                table[r][c] = max_parent

    # 找到最后一列中最大的sum
    max_row = max(range(nrows), key=lambda r: table[r][ncols-1][1])


    # 现在的row index 加上 parent index 的offset，然后col - 1 往前一列。直到 row index = 0 
    path = []

    # Add last row index
    path.append(max_row)

    # in reversed(range(1, ncols))
    # in range(ncols - 1, 0, -1)
    for current_column in range(ncols - 1, 0, -1):
        offset = table[path[-1]][current_column][0]
        path.append(path[-1] + offset)

    path.reverse()

    return path



    # if ncols == 1:
    #     mx = 0 
    #     for c in range(ncols):
    #         for r in range(nrows):
    #             if mx < smiles[r][c]:
    #                 mx = smiles[r][c]
    #     return mx 

    # paths = []
    # c = 0 
    # for r in range(nrows):
    #     path = []
    #     cur = smiles[r][c]
    #     path.append(cur)
    #     neighbors = get_neighbors(r, c) 
    #     for n in neighbors:
    #         sub_smiles = []
    #         for row in range(nrows):
    #             sub_colns = smiles[row][c+1:]
    #             sub_smiles.append(sub_colns)

    #         sub_field = {"nrows": nrows, "ncols": ncols - c, "smiles": sub_smiles}
    #         path_to_happiness(sub_field)
    #         compare = max()


# N is an integer
# Find the number of ways to partition N into a sequence
# N = 3
# (1, 1, 1), (1, 2), (2, 1), (3)

def partition(N):
    if N == 0 or N == 1:
        return 1
    comb = 0
    for i in range(1, N+1):
        comb += partition(N - i)
    return comb


if __name__ == "__main__":

    N = 10
    assert partition(N) == 2 ** (N-1)
    print(partition(N))