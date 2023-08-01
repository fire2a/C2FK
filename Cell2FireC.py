# coding: utf-8
__version__ = "1.0"
__author__ = "Cristobal Pais"

# General imporations
import os
import glob
import shutil
import signal
import subprocess
import sys
from platform import system as platform_system
import Cell2Fire.DataGeneratorC as DataGenerator
import Cell2Fire.ReadDataPrometheus as ReadDataPrometheus
from Cell2Fire.ParseInputs import InitCells
from Cell2Fire.Stats import *
from Cell2Fire.Heuristics import *
from Cell2Fire.GeotiffsGenerator import InputGeotiff,OutputGeotiff

class Cell2FireC:
    # Constructor and initial run
    def __init__(self, args):
        # Store arguments
        self.args = args

        # Check if we need to generate DataC.csv
        self.generateDataC()

        # Main call
        if self.args.onlyProcessing is False:
            self.run()
        else:
            print("Running Cell2FirePy as a post-processing tool for a previous simulation")

        # Containers
        self._NCells = 0
        self._Rows = 0
        self._Cols = 0
        self._AdjCells = {}
        self._CoordCells = {}
        self._GForestType = []
        self._GForestN = []
        self._Colors = {}
        self._FTypeCells = []
        self._FTypes2 = {'pch1':1, 'pch2':2, 'pch3':3, 'pch4':4, 'pch5':5, 'mt01':6, 'mt02':7,
                         'mt03':8, 'mt04':9, 'mt05':10, 'mt06':11, 'mt07':12, 'mt08':13, 'bn01':14,
                         'bn02':15, 'bn03':16, 'bn04':17, 'bn05':18, 'pl01':19, 'pl02':20, 'pl03':21,
                         'pl04':22, 'pl05':23, 'pl06':24, 'pl07':25, 'pl08':26, 'pl09':27, 'pl10':28,
                         'pl11':29, 'dx01':30, 'dx02':31,'fm10':32}
        
    
    # Run C++ Sim 
    def run(self):
        # Parse args for calling C++ via subprocess
        exe = '.exe' if platform_system() == 'Windows' else ''
        execArray=[os.path.join(os.getcwd(),'Cell2FireC/Cell2Fire'+exe),
                   '--input-instance-folder', self.args.InFolder,
                   '--output-folder', self.args.OutFolder if (self.args.OutFolder is not None) else '',
                   '--ignitions' if (self.args.ignitions) else '',
                   '--sim-years', str(self.args.sim_years),
                   '--nsims', str(self.args.nsims),
                   '--nthreads', str(self.args.nthreads),
                   '--grids' if (self.args.grids) else '', '--final-grid' if (self.args.finalGrid) else '',
                   '--Fire-Period-Length', str(self.args.input_PeriodLen),
                   '--output-messages' if (self.args.OutMessages) else '',
                   '--out-fl' if (self.args.OutFl) else '',
                   '--out-intensity' if (self.args.OutIntensity) else '',
                   '--out-ros' if (self.args.OutRos) else '',
                   '--out-crown' if (self.args.OutCrown) else '',
                   '--out-cfb' if (self.args.OutCrownConsumption) else '',
                   '--weather', self.args.WeatherOpt,
                   '--nweathers', str(self.args.nweathers),
                   '--ROS-CV', str(self.args.ROS_CV),
                   '--IgnitionRad', str(self.args.IgRadius),
                   '--seed', str(int(self.args.seed)),
                   '--ROS-Threshold', str(self.args.ROS_Threshold),
                   '--HFI-Threshold', str(self.args.HFI_Threshold),
                   '--bbo' if (self.args.BBO) else '',
                   '--FirebreakCells', self.args.HCells if(self.args.HCells is not None) else '',
                   '--cros' if (self.args.cros) else '',
                   '--fmc', str(int(self.args.fmc)),
                   #'--ROS10Factor', str(self.args.ROS10Factor),
                   #'--CCFFactor', str(self.args.CCFFactor),
                   #'--CBDFactor', str(self.args.CBDFactor),
                   '--HFactor', str(self.args.HFactor),
                   '--FFactor', str(self.args.FFactor),
                   '--BFactor', str(self.args.BFactor),
                   '--EFactor', str(self.args.EFactor),
                   ]

        #Geotiffs
        if self.args.Geotiffs:
            print("Generating input Geotiff...", flush=True)
            InputGeotiff(self.args.InFolder)

        # Output log
        if self.args.OutFolder is not None:
            if os.path.isdir(self.args.OutFolder) is False:
                os.makedirs(self.args.OutFolder)
            LogName = os.path.join(self.args.OutFolder, "LogFile.txt")
        else:
            LogName = os.path.join(self.args.InFolder, "LogFile.txt")

        # Perform the call
        print("Calling Cell2Fire simulator...", flush=True)
        with open(LogName, 'w') as output:
            proc = subprocess.Popen(execArray, stdout=output)
            proc.communicate()
        proc.wait()

        # End of the replications
        print("End of Cell2Fire Simulator execution...",flush=True)
        if self.args.Geotiffs:
            print("Generating output Geotiff...", flush=True)
            OutputGeotiff(self.args.InFolder,self.args.OutFolder,self.args.nsims)
        #Geotiffs
        #if self.args.geotiffs is not None:
         #   GeotiffsGenerator.OutputGeotiff(self.args.InFolder)


    # Run C++ Sim with heuristic treatment
    def run_Heur(self, OutFolder, HarvestPlanFile):
        # Parse args for calling C++ via subprocess
        exe = '.exe' if platform_system() == 'Windows' else ''
        execArray=[os.path.join(os.getcwd(),'Cell2FireC/Cell2Fire'+exe),
                   '--input-instance-folder', self.args.InFolder,
                   '--output-folder', OutFolder if (OutFolder is not None) else '',
                   '--ignitions' if (self.args.ignitions) else '',
                   '--sim-years', str(self.args.sim_years),
                   '--nsims', str(self.args.nsims),
                   '--nthreads', str(self.args.nthreads),
                   '--grids' if (self.args.grids) else '', '--final-grid' if (self.args.finalGrid) else '',
                   '--Fire-Period-Length', str(self.args.input_PeriodLen),
                   '--output-messages' if (self.args.OutMessages) else '',
                   '--out-fl' if (self.args.OutFl) else '',
                   '--out-intensity' if (self.args.OutIntensity) else '',
                   '--out-ros' if (self.args.OutRos) else '',
                   '--out-crown' if (self.args.OutCrown) else '',
                   '--out-cfb' if (self.args.OutCrownConsumption) else '',
                   '--weather', self.args.WeatherOpt,
                   '--nweathers', str(self.args.nweathers),
                   '--ROS-CV', str(self.args.ROS_CV),
                   '--IgnitionRad', str(self.args.IgRadius),
                   '--seed', str(int(self.args.seed)),
                   '--ROS-Threshold', str(self.args.ROS_Threshold),
                   '--HFI-Threshold', str(self.args.HFI_Threshold),
                   '--bbo' if (self.args.BBO) else '',
                   '--FirebreakCells', HarvestPlanFile if(HarvestPlanFile is not None) else '',
                   '--cros' if (self.args.cros) else '',
                   '--FMC', str(int(self.args.FMC)),
                   '--HFactor', str(self.args.HFactor),
                   '--FFactor', str(self.args.FFactor),
                   '--BFactor', str(self.args.BFactor),
                   '--EFactor', str(self.args.EFactor),]
        #Geotiffs
        if self.args.Geotiffs is not None:
            InputGeotiff(self.args.InFolder)

        # Output log
        if OutFolder is not None:
            if os.path.isdir(OutFolder) is False:
                os.makedirs(OutFolder)
            LogName = os.path.join(OutFolder, "LogFile.txt")
        else:
            LogName = os.path.join(self.args.InFolder, "LogFile.txt")

        # Perform the call
        with open(LogName, 'w') as output:
            proc = subprocess.Popen(execArray, stdout=output)
            proc.communicate()
        proc.wait()

        # End of the replications
        if HarvestPlanFile is not None:
            print("End of Cell2FireC with Harvesting Plan execution...")
        else:
            print("End of Cell2FireC execution...")
        if self.args.Geotiffs is not None:
            OutputGeotiff(self.args.InFolder,self.args.OutFolder,self.args.nsims)


    # Pre-processing
    '''
    Generate the Data.csv file for the C++ core
    '''
    def generateDataC(self):
        dataName = os.path.join(self.args.InFolder, "Data.csv")
        if os.path.isfile(dataName) is False:
            print("Generating Data.csv File...",flush=True)
            DataGenerator.GenDataFile(self.args.InFolder)



    # Post-processing
    '''
    Data for stats/plots
    '''
    def getData(self):
        # Paths
        ForestFile = os.path.join(self.args.InFolder, "fuels.asc")
        FBPlookup = os.path.join(self.args.InFolder, "kitral_lookup_table.csv")
        
        # Obtain FBP and Color dictionaries from FBP file, read the ForestGrid file
        FBPDict, ColorsDict = ReadDataPrometheus.Dictionary(FBPlookup)
        GForestN, GForestType, Rows, Cols, AdjCells, CoordCells, CellSide = ReadDataPrometheus.ForestGrid(ForestFile,
                                                                                                          FBPDict)

        # Number of cells
        self._NCells = Rows * Cols
        self._Rows = Rows
        self._Cols = Cols
        self._AdjCells = AdjCells
        self._CoordCells = CoordCells
        self._GForestType = GForestType
        self._GForestN = np.asarray(GForestN).reshape((Rows, Cols))

        # Initialize main cells inputs
        FTypeCells, StatusCells, RealCells, Colors = InitCells(self._NCells, self._FTypes2,
                                                               ColorsDict, GForestType, GForestN)

        self._Colors = Colors
        self._FTypeCells = FTypeCells
        self._StatusCells = StatusCells

    '''
    Generate empty MessageFiles if needed
    '''
    def DummyMsg(self):
        # Messages path and CWD for returning
        MPath = os.path.join(self.args.OutFolder, "Messages")
        if not os.path.exists(MPath):
            os.makedirs(MPath)
        CWD = os.getcwd()
        os.chdir(MPath)

        # Read files
        MessagesFiles = glob.glob('*')
        existingIDs = [int(re.match('MessagesFile(\d+)', MessagesFiles[i]).groups()[0]) for i in range(0, len(MessagesFiles))]

        # Loop for filling with dummy files
        for i in range(1, self.args.nsims + 1):
            if i not in existingIDs:
                np.savetxt(os.path.join(MPath, "MessagesFile" + str(i).zfill(2) + ".csv"), np.asarray([]))

        # Come back to the original directory
        os.chdir(CWD)


    '''
    Generate empty MessageFiles if needed
    '''
    def DummyMsg_Heur(self, OutFolder):
        # Messages path and CWD for returning
        MPath = os.path.join(OutFolder, "Messages")
        CWD = os.getcwd()
        if not os.path.exists(MPath):
            os.makedirs(MPath)
        os.chdir(MPath)

        # Read files
        MessagesFiles = glob.glob('*')
        existingIDs = [int(re.match('MessagesFile(\d+)', MessagesFiles[i]).groups()[0]) for i in range(0, len(MessagesFiles))]

        # Loop for filling with dummy files
        for i in range(1, self.args.nsims + 1):
            if i not in existingIDs:
                np.savetxt(os.path.join(MPath, "MessagesFile" + str(i).zfill(2) + ".csv"), np.asarray([]))

        # Come back to the original directory
        os.chdir(CWD)


    '''
    Generate statistics from Grids
    '''
    def stats(self):
        # Get rows, cols
        DFForest = pd.read_csv(os.path.join(self.args.InFolder, "fuels.asc"),
                               sep=" ", header=None, nrows=2)
        Shape = DFForest[1].values

        # Initialize the Stats object
        StatsPrinter = Statistics(OutFolder=self.args.OutFolder,
                                  StatsFolder="",
                                  MessagesPath=os.path.join(self.args.OutFolder, "Messages"),
                                  Rows=Shape[0],
                                  Cols=Shape[1],
                                  NCells=Shape[0] * Shape[1],
                                  boxPlot=True,
                                  CSVs=True,
                                  statsGeneral=True,
                                  statsHour=True,
                                  histograms=True,
                                  BurntProb=True,
                                  nSims=self.args.nsims,
                                  verbose=self.args.verbose,
                                  GGraph=None,
                                  tCorrected=False,
                                  pdfOutputs=self.args.pdfOutputs)

        # Hourly Stats
        if self.args.grids:
            print("Hourly stats...",flush=True)
            StatsPrinter.HourlyStats()

        # General Stats
        print("General stats...",flush=True)
        StatsPrinter.GeneralStats()

        # Dummy msg if needed
        self.DummyMsg()

        # Get Coordinates and colors
        if self.args.spreadPlots or self.args.plots or self.args.allPlots:
            print("Reading data...",flush=True)
            self.getData()  
            print("Dummy if needed...",flush=True)
            self.DummyMsg()

        # Spread plots
        if self.args.spreadPlots or self.args.allPlots:
            # Fire Spread Graphs
            print("Generating global fire spread evolution...",flush=True)
            totalPlots = 1

            # If multiple sims, plots including freq are useful
            if self.args.nsims > 1:
                totalPlots = 3
            for v in tqdm(range(totalPlots)):
                StatsPrinter.GlobalFireSpreadEvo(self._CoordCells,
                                                 onlyGraph=True,
                                                 version=v)

            # Fire Spread Graphs (individual)
            if self.args.grids:
                print("Generating individual Fire Spread plots...",flush=True)
                for n in tqdm(range(1, self.args.nsims + 1)):
                    StatsPrinter.SimFireSpreadEvo(n, self._CoordCells,
                                                  self._Colors,
                                                  H=None, version=0,
                                                  print_graph=True,
                                                  analysis_degree=False,
                                                  onlyGraph=True)


            # Generate Initial Forest
            print("Generating initial forest plot...",flush=True)
            FBPlookup = os.path.join(self.args.InFolder, "kitral_lookup_table.csv")
            if self.args.HCells is not None: 
                HCarray = np.loadtxt(self.args.HCells, skiprows=1, delimiter=",")[1:].astype(np.int)
                print("HCArray:", HCarray)
                print("GForestN:", self._GForestN)
                self._GForestN = self._GForestN.flatten()
                for i in HCarray:
                    self._GForestN[i-1] = -1
                    #self._GForestN[i // Shape[1] - 1, i - i // Shape[1] * i // Shape[0] - 1] = -1

                self._GForestN = self._GForestN.reshape((Shape[0], Shape[1]))
            StatsPrinter.ForestPlot(FBPlookup, self._GForestN,
                                    self.args.OutFolder, namePlot="InitialForest")


        # Individual plots
        if self.args.plots or self.args.allPlots:
            if self.args.grids:
                # Plotting
                print("Generating fire evolution plots...",flush=True)
                StatsPrinter.plotEvo()

                # Combine them with background
                if self.args.combine:
                    print("Combining Fires with background (initial forest)...",flush=True)
                    StatsPrinter.mergePlot()

            print("Generating detailed individual propagation trees...",flush=True)
            for n in tqdm(range(1, self.args.nsims + 1)):
                for v in range(1,4):
                    StatsPrinter.SimFireSpreadEvoV2(n, self._CoordCells,
                                                    self._Colors,
                                                    H=None, version=v,
                                                    onlyGraph=True)



    '''
    Generate statistics from Grids
    '''
    def stats_Heur(self, OutFolder, HCells=None):
        # Initialize the Stats object
        StatsPrinter = Statistics(OutFolder=OutFolder,
                                  StatsFolder="",
                                  MessagesPath=os.path.join(OutFolder, "Messages"),
                                  Rows=self._Rows,
                                  Cols=self._Cols,
                                  NCells=self._Cols * self._Rows,
                                  boxPlot=True,
                                  CSVs=True,
                                  statsGeneral=True,
                                  statsHour=True,
                                  histograms=True,
                                  BurntProb=True,
                                  nSims=self.args.nsims,
                                  verbose=self.args.verbose,
                                  GGraph=None,
                                  tCorrected=False,
                                  pdfOutputs=self.args.pdfOutputs)

        # Dummy msg if needed
        self.DummyMsg()

        # Hourly Stats
        if self.args.grids:
            print("Hourly stats...",flush=True)
            StatsPrinter.HourlyStats()

        # General Stats
        print("General stats...",flush=True)
        StatsPrinter.GeneralStats()

        # Get Coordinates and colors
        if self.args.spreadPlots or self.args.plots or self.args.allPlots:
            print("Reading data...",flush=True)
            self.getData()  
            print("Dummy if needed...",flush=True)
            self.DummyMsg_Heur(OutFolder)

        # Spread plots
        if self.args.spreadPlots or self.args.allPlots:
            # Fire Spread Graphs
            print("Generating global fire spread evolution...",flush=True)
            totalPlots = 1

            # If multiple sims, plots including freq are useful
            if self.args.nsims > 1:
                totalPlots = 3
            for v in tqdm(range(totalPlots)):
                StatsPrinter.GlobalFireSpreadEvo(self._CoordCells,
                                                 onlyGraph=True,
                                                 version=v)

            # Fire Spread Graphs (individual)
            if self.args.grids:
                print("Generating individual Fire Spread plots...",flush=True)
                for n in tqdm(range(1, self.args.nsims + 1)):
                    StatsPrinter.SimFireSpreadEvo(n, self._CoordCells,
                                                  self._Colors,
                                                  H=None, version=0,
                                                  print_graph=True,
                                                  analysis_degree=False,
                                                  onlyGraph=True)


            # Generate Initial Forest
            print("Generating initial forest plot...")
            FBPlookup = os.path.join(self.args.InFolder, "kitral_lookup_table.csv")
            if HCells is not None: 
                HCarray = np.loadtxt(HCells, skiprows=1, delimiter=",")[1:].astype(np.int)
                self._GForestN = self._GForestN.flatten()
                for i in HCarray:
                    self._GForestN[i-1] = -1

                self._GForestN = self._GForestN.reshape((self._Rows, self._Cols))
            StatsPrinter.ForestPlot(FBPlookup, self._GForestN,
                                    OutFolder, namePlot="InitialForest")


        # Individual plots
        if self.args.plots or self.args.allPlots:
            if self.args.grids:
                # Plotting
                print("Generating fire evolution plots...",flush=True)
                StatsPrinter.plotEvo()

                # Combine them with background
                if self.args.combine:
                    print("Combining Fires with background (initial forest)...",flush=True)
                    StatsPrinter.mergePlot()

            print("Generating detailed individual propagation trees...",flush=True)
            for n in tqdm(range(1, self.args.nsims + 1)):
                for v in range(1,4):
                    StatsPrinter.SimFireSpreadEvoV2(n, self._CoordCells,
                                                    self._Colors,
                                                    H=None, version=v,
                                                    onlyGraph=True)


    '''
    Initialize heuristic object to estimate FPV or other metrics
    '''
    def heur(self, AvailCells=set(), BurntCells=set(), FirebreakCells=set()):
        # Seed
        npr.seed(self.args.seed)

        # Dummy msg if needed
        self.DummyMsg()

        # If no stats, read data
        if self.args.stats is False or \
           (self.args.spreadPlots is False and self.args.plots is False and self.args.allPlots is False):
            print("Reading data...")
            self.getData()

        # Init values for heuristic object
        self._FPVGrids = True
        self._onlyGraphs = False
        self._GenSel = False
        self._GreedySel = True

        # AvailCells (Original at the beginning of the instance)
        self._AvailCells = set([])
        for idx in range(len(self._FTypeCells)):
            # Burnable
            if self._FTypeCells[idx] == 2:
                self._AvailCells.add(idx + 1)

        # Folders
        MessagePath = os.path.join(self.args.OutFolder, "Messages")
        if not os.path.exists(MessagePath):
            os.makedirs(MessagePath)
        OutFolder = os.path.join(self.args.OutFolder, "Heuristic")
        if not os.path.exists(OutFolder):
            os.makedirs(OutFolder)

        # Heur object
        self._HeurObject = Heuristic(version=self.args.heuristic,       # Heuristic ID
                                     MessagePath=MessagePath,           # Path to the messages (FPV and graphs)
                                     InFolder=self.args.InFolder,       # Instance Folder path
                                     OutFolder=OutFolder,               # Output Folder path (for heuristic outputs)
                                     AvailCells=self._AvailCells,       # AvailCells
                                     BurntCells=BurntCells,             # BurntCells
                                     FirebreakCells=FirebreakCells,     # Harvested Cells
                                     AdjCells=self._AdjCells,           # Adjacent cells info
                                     NCells=self._NCells,               # Number of cells inside the forest
                                     Cols=self._Cols,                   # Number of columns inside the forest
                                     Rows=self._Rows,                   # Number of rows inside the forest
                                     Year=1,                            # Current year
                                     FPVGrids=self._FPVGrids,           # Boolean flag: Generate FPV grids/Heatmaps
                                     GeneticSelection=self._GenSel,     # Gen alg for selecting the best connected patch (adjacency)
                                     GreedySelection=self._GreedySel,   # Greedy selection (top to bottom) for adjacency constraints
                                     verbose=self.args.verbose)         # Verbosity level (False = minimum)

        # If no messages, no graph for FPV heurs
        if not os.listdir(MessagePath) and self.env._heuristic >= 7:
            print("No message files: FPV heuristics cannot be used")

        else:
            # Init Graph (FPV)
            if self.args.valueFile is None:
                # All cells are identical (no specific value)
                self._HeurObject.initGraph_FPV(np.full(self._NCells, 1),    # Vol
                                               self.args.ngen,              # Generations
                                               self.args.npop,              # Population
                                               self.args.tSize,             # Tournament
                                               self.args.cxpb,              # CrossOver
                                               self.args.mutpb,             # Mutation
                                               self.args.indpb,             # Individual prob.
                                               self.args.GPTree)            # Global Propagation Tree option
            else:
                # User provides a custom value file with values for each cell
                customValue = np.loadtxt(self.args.valueFile, delimiter=" ", dtype=np.float32)
                customValue = customValue.flatten()
                if len(customValue) != self._NCells:
                    print("[ERROR] Custom value matrix does not match the dimension of the forest, please check it")
                    print("[ERROR] Running with identical weights (1)")
                    customValue = np.full(self._NCells, 1)
                else:
                    print("Using custom value function ( from file", self.args.valueFile, ")")
                self._HeurObject.initGraph_FPV(customValue,                 # Custom value
                                               self.args.ngen,              # Generations
                                               self.args.npop,              # Population
                                               self.args.tSize,             # Tournament
                                               self.args.cxpb,              # CrossOver
                                               self.args.mutpb,             # Mutation
                                               self.args.indpb,             # Individual prob.
                                               self.args.GPTree)            # Global Propagation Tree option

        if self.args.heuristic < 6:
            # Init Graph (BP) - CP: checking best way to split logics
            self._HeurObject.initGraph_BP()


        # Plot
        self._HeurObject.Global_FPVPlot(normalized=True, xticks=50, yticks=50)

        # Heuristics available
        AvailHeuristics = {0: "Random",
                           1: "Random_Adj",
                           2: "Max_Utility",
                           3: "Max_Utility_Adj",
                           4: "Burnt_Probability",
                           5: "Burnt_Probability_Adj",
                           6: "FPV_Palma",
                           7: "FPV_Palma_Adj",
                           8: "DPV_VaR_Volume",
                           9: "DPV_VaR_Volume_Adj",
                           10: "DPV_VaR_Volume_Degree",
                           11: "DPV_VaR_Volume_Degree_Adj",
                           12: "DPV_VaR_Volume_Degree_Time",
                           13: "DPV_VaR_Volume_Degree_Time_Adj",
                           14: "DPV_VaR_Volume_Degree_Time_Layer_decay",
                           15: "DPV_VaR_Volume_Degree_Time_Layer_decay_Adj",
                           18: "BCentrality",
                           19: "BCentrality_Adj"}

        # Heuristic parameters
        if self.args.fdemand:
            DFractions = [-1, 0.001, 0.002, 0.003, 0.004, 0.005,                      # Demand fractions (Finer version)
                          0.01, 0.015, 0.02, 0.025, 0.03, 0.035, 0.04]
        else:
            DFractions = [-1, 0.05, 0.10, 0.15, 0.20, 0.25,                           # Demand fractions
                          0.30, 0.35, 0.4, 0.45, 0.50,
                          #0.55, 0.60, 0.65, 0.7,
                          0.75, 0.80, 0.85, 0.9]

        DUnits = [int(dfr * len(self._AvailCells)) for dfr in DFractions[1:]]  # Demand translated to units (based on available set)
        if self.args.valueFile is not None:
            self._CellUtility = np.loadtxt(self.args.valueFile, delimiter=" ", dtype=np.float32)
            self._CellUtility = self._CellUtility.flatten()
        else:
            print('Reading utility from:'. self.args.valueFile)
            self._CellUtility = np.full(shape=(self._NCells), fill_value=1)        # Cell's utility


        # Run the heuristic
        SelHeur = AvailHeuristics[self.args.heuristic]
        if self.args.GPTree:
            SelHeur = SelHeur + "_GPTree"
        print("------ Running Heuristic:", SelHeur, "------")
        if self.args.verbose:
            print("Available cells (originally):", self._AvailCells)
        print("Total Available cells:", len(self._AvailCells))
        step = 0
        for fr in DFractions:
            # Special case: record the what if no heuristic fire
            if fr == -1:
                if self.args.noEvaluation is False:
                    print("Running the AS-IS forest (no heuristic applied)")
                    csvPath = os.path.join(OutFolder, SelHeur)
                    self.run_Heur(os.path.join(csvPath, "No_Heur_Case"), None)
                else:
                    print("No evaluation is performed (option)")

            else:
                print("\nTreat Fraction " + str(fr) + "%...")
                action, fitness = self._HeurObject.runHeur(self._AvailCells.copy(),      # Available cells
                                                           self._AdjCells,               # Adjacent dictionary
                                                           np.full(self._NCells, 1),     # Volume
                                                           DUnits[step],                 # Demand Units
                                                           self._CellUtility,            # Harvesting Utility
                                                           1)                            # Year (TODO: can be deleted later since we test all ddm.)
                actions = list(action)
                #print("Selected cells:", actions)
                print("Demand satisfied:", len(action) == DUnits[step])
                if len(action) != DUnits[step]:
                    print("Total harvested:", len(action),
                          " Demand:", DUnits[step],
                          " Delta:", DUnits[step] - len(action))
                print("Total fitness (FPV):", fitness)

                # Save the harvested cells
                csvPath = os.path.join(OutFolder, SelHeur)
                if not os.path.exists(csvPath):
                    os.makedirs(csvPath)

                # Create the aux DF for saving the harvested cells in different files depending on the treated fraction %
                np.savetxt(os.path.join(csvPath, SelHeur + "_" +str(fr) + ".csv"),
                           np.asarray([1] + actions).reshape(1, len(actions) + 1).astype(np.int),
                           delimiter=",", fmt="%d", header="Year,HCells", comments='')
                step += 1

                if self.args.noEvaluation is False:
                    # Run the heuristic
                    print("Running the instance with the heuristic...")
                    self.run_Heur(os.path.join(csvPath, "Fraction" + str(fr)),
                                  os.path.join(csvPath, SelHeur + "_" +str(fr) + ".csv"))

                    # Stats
                    print("Generating stats from heuristic...")
                    self.stats_Heur(os.path.join(csvPath, "Fraction" + str(fr)),
                                    os.path.join(csvPath, SelHeur + "_" +str(fr) + ".csv"))
                else:
                    print("No evaluation is performed, TF:", fr)

