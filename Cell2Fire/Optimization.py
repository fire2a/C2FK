import pyomo.environ as pyo
import pandas as pd
import os
import numpy as np
from ReadDataPrometheus import Ascii2list
import time

def open_as_array(rst_fp, nCells): 
    """
    
    """
    rs = Ascii2list(rst_fp, nCells)
    for i in range(len(rs)):
        if rs[i] < 0.0 or rs[i] == '-Inf':
            rs[i] = 0
    return(rs)

def array2ascii(array, filename, xllcorner, yllcorner, cellsize, NODATA_value,nrows=None, ncols=None): 
    array = array[::-1]
    if nrows==None or ncols==None:
      nrows, ncols = array.shape
    file = open(filename,"w")
    file.write(f"ncols {ncols}\n"
               f"nrows {nrows}\n"
               f"xllcorner     {xllcorner}\n"
               f"yllcorner     {yllcorner}\n"
               f"cellsize      {cellsize}\n"
               f"NODATA_value  {NODATA_value}\n")
    for r in range(nrows): 
        line = str(list(array[r])) 
        line = line.replace("[","")
        line = line.replace("]","\n")
        file.write(line)


def lst2dct(lst, set_Avail): 
    """
    
    """
    if type(lst) == np.ndarray: 
        dct = dict([(i, lst[i-1]) for i in set_Avail])
    elif type(lst) == dict: pass 
    else:
        raise Exception('First argument must be a list or a dictionary.')
    return(dct)

def expected_loss(var, bp):
    var = list(var.values())
    var = np.array(var)
    
    bp = list(bp.values())
    bp = np.array(bp)
    
    s = sum(var * bp)
    
    return(s)

def bin_to_nod(solution, output_fp="harvested.csv"):
    """
    bin_to_nod generates the harvested file that is needed by the Cell2Fire.
    
    """
    nod = [i+1 for i in solution]
    datos = [np.insert(nod, 0, 1)]
    if len(nod) == 0:
        cols = ['Year Number']
    else:
        colu = ['Year Number', "Cell Numbers"]
        col2 = [""]*(len(nod)-1)
        cols = colu+col2
    df = pd.DataFrame(datos, columns=cols)
    df.to_csv(output_fp, index = None, mode = 'a')

def fire_breack_allocator(set_Avail, dpv, bp, var, dtc_coordPos,m,n, 
                          capacity = 0.03, tolerance = 0.3, solver = 'gurobi', 
                          output_fp = 'harvested'): 
    """
    bp: Burn Probability list or dictionary. 
    
    capacity: percentage of the landscape that could be treated. 
    tolerance: percentage of expected losses due to future fires that are tolerated to be lost by the treatment itself. 
    
    """
    # Chiecking input types
    dpv = lst2dct(dpv, set_Avail)
    bp = lst2dct(bp, set_Avail)
    var = lst2dct(var, set_Avail)
    
    # expected loss of the landscape combined Index
    el = expected_loss(var, bp)
    
    # Upper boundries for each constraint
    tolerance_cons = tolerance*el
    capacity_cons = int(capacity*len(set_Avail))
    print(len(set_Avail))
    print(capacity_cons)
    # model inicialization
    model = pyo.ConcreteModel()
    
    # Decision variables
    model.I = pyo.Set(initialize = set_Avail)
    model.x = pyo.Var(model.I, 
                      domain=pyo.Binary, 
                      initialize = 0)
    
    # Parameters
    model.var = pyo.Param(model.I, 
                           initialize = var, 
                           default = 0)
    model.dpv = pyo.Param(model.I, 
                           initialize = dpv, 
                           default = 0)
    
    # Funcion objetivo: se quiere seleccionar las celdas con mayor DPV
    def obj_rule(model):
        return pyo.sum_product(model.dpv, 
                               model.x) - pyo.sum_product(model.var, 
                                                                model.x)
    
    model.z = pyo.Objective(rule=obj_rule, sense=pyo.maximize)
    model.cons = pyo.ConstraintList()
    model.cons.add(pyo.summation(model.x) <= capacity_cons)
    model.cons.add(pyo.sum_product(model.var, model.x) <= tolerance_cons)

    solver = pyo.SolverFactory(solver)
    t0 = time.time()
    results = solver.solve(model)
    tf = time.time()
    t = tf-t0
    
    S = set()  # Aqui almaceno las celdas que el modelo decide cortar, sin conectividad
    for i in set_Avail:
        if pyo.value(model.x[i]) > 0:  # celdas con valor 1
            # print 'x[' + str(i) + '] = ', value(model.x[i])
            S.add(i)
    print(len(S))
    lst_firebreaks = []
    for i in range(len(var)): 
        if i+1 in S: 
            lst_firebreaks.append(1)
        else: 
            lst_firebreaks.append(0)
    
    # Write harvested.csv
    fn = output_fp + '.csv'
    bin_to_nod(S, )
    

    rs_firebreaks = np.empty((m,n))
    for i in set_Avail:
        x = dtc_coordPos[i][0] 
        y = dtc_coordPos[i][1]
        if i in S: 
            rs_firebreaks[y,x] = 1
        else: 
            rs_firebreaks[y,x] = 0.0
            
    fn = output_fp + '.asc'
    xllcorner = 0.0
    yllcorner = 0.0
    
    array2ascii(rs_firebreaks, fn, xllcorner, yllcorner,100,-999.9)

def main(directory): 
    from ReadDataPrometheus import ForestGrid, Dictionary
    
    fp_fuels = os.path.join(directory, 'fuels.asc')
    fp_lookup = os.path.join(directory, 'kitral_lookup_table.csv')
    
    dct_fbp, _ = Dictionary(fp_lookup)
    
    _, lst_cellsGrid4, m, n, _, lst_coordCells, _ = ForestGrid(
        fp_fuels, dct_fbp)
    
    nCells = m*n
    
    # set_Avail: set with flammable cells id
    set_Avail = set()

    # Building set_Avail and set_nonAvail
    for i in range(nCells):
        if lst_cellsGrid4[i] != 'NData':
            set_Avail.add(i+1)

    fp_var = os.path.join(directory, 'var.asc')
    var = open_as_array(fp_var, nCells)
    
    fp_bp = os.path.join(directory, 'bp_base.asc')
    bp = open_as_array(fp_bp, nCells)
    
    fp_dpv = os.path.join(directory, 'dpv.asc')
    dpv = open_as_array(fp_dpv, nCells)
            
    dtc_coordPos = dict()
    for i in set_Avail:
        dtc_coordPos[i] = lst_coordCells[i-1]
    
    fire_breack_allocator(set_Avail, dpv, bp, var, dtc_coordPos,m,n)

if __name__ == '__main__':
    
    directory = "C:/Users/56965/Desktop/VaR_Valpo/Outputs/Combined_risk/"
    main(directory)
