__author__ = 'gaurav'

class Stats:
    #Total number of messages in lookups
    total_lookup_messages = 0

    #Total number of lookups
    total_lookups = 0

    #Total number of messages in inserts
    total_insert_messages = 0

    #Total number of inserts
    total_inserts = 0

    #Total number of messages in deletes
    total_delete_messages = 0

    #Total number of deletes
    total_deletes = 0

    #Finger table stats
    finger_table_hits = 0
    finger_table_misses = 0

    def print_stats(self):
        print "*********************STATISTICS**************************"

        print "::LOOKUP OPERATION STATS::"
        print "Total Lookups:"+str(self.total_lookups)
        print "Total Number of Messages in Lookups:"+str(self.total_lookup_messages)
        print "Average Number of Messages Per Lookup:"+str(float(self.total_lookup_messages)/float(self.total_lookups))
        print "*********************************************************"

        print "\n::INSERT OPERATION STATS::"
        print "Total Inserts:"+str(self.total_inserts)
        print "Total Number of Messages in Inserts:"+str(self.total_insert_messages)
        print "Average Number of Messages Per Insert:"+str(float(self.total_insert_messages)/float(self.total_inserts))
        print "*********************************************************"

        print "\n::DELETE OPERATION STATS::"
        print "Total Delete:"+str(self.total_deletes)
        print "Total Number of Messages in Deletes:"+str(self.total_delete_messages)
        print "Average Number of Messages Per Delete:"+str(float(self.total_delete_messages)/float(self.total_deletes))
        print "*********************************************************"

        print "\n::FINGER TABLE EFFICACY::"
        print "Total Number of Finger Table accesses:"+str(self.finger_table_hits+self.finger_table_misses)
        print "Finger Table Hits:"+str(self.finger_table_hits)
        print "Finger Table Misses:"+str(self.finger_table_misses)
        print "Finger Table Hit Ratio:"+str(float(self.finger_table_hits)/float(self.finger_table_hits + self.finger_table_misses))
        print "*********************************************************"

        print "END"