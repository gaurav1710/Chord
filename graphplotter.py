__author__ = 'gaurav'

from datacollector import DataCollector
import matplotlib.pyplot as plotter


class GraphPlotter:

    dc = DataCollector()
    #PLOT FOR AVERAGE NUMBER OF MESSAGES IN NODE INSERTION VS NUMBER OF NODES
    def plotForInserts(self):
        plotter.plot(self.dc.n, self.dc.avg_insert_messages, color='b', linewidth=2.0)
        plotter.ylabel("Average Number of Messages(Node Arrival)")
        plotter.xlabel("Number of Nodes(N)")
        plotter.show()

    #PLOT FOR AVERAGE NUMBER OF MESSAGES IN NODE DELETION VS NUMBER OF NODES
    def plotForDeletes(self):
        plotter.plot(self.dc.n, self.dc.avg_delete_messages, color='r', linewidth=2.0)
        plotter.ylabel("Average Number of Messages(Node Departure)")
        plotter.xlabel("Number of Nodes(N)")
        plotter.show()

    #PLOT FOR AVERAGE NUMBER OF MESSAGES IN KEY LOOKUP VS NUMBER OF NODES
    def plotForLookups(self):
        plotter.plot(self.dc.n, self.dc.avg_lookup_messages, color='g', linewidth=2.0)
        plotter.ylabel("Average Number of Messages(Key Lookup)")
        plotter.xlabel("Number of Nodes(N)")
        plotter.show()

    #PLOT FOR GLOBAL FINGER TABLE HIT RATIO
    def plotForFingerTableEfficacy(self):
        plotter.plot(self.dc.n, self.dc.finger_table_hitratio, color='g', linewidth=2.0)
        plotter.ylabel("Finger Table Hit Ratio")
        plotter.xlabel("Number of Nodes(N)")
        plotter.show()
