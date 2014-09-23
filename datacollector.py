__author__ = 'gaurav'

from stats import Stats
#Parameter data collector
class DataCollector:
    #Total number of messages in lookups for ith experiment
    total_lookup_messages = []

    #Total number of lookups for ith experiment
    total_lookups = []

    avg_lookup_messages = []

    #Total number of messages in inserts for ith experiment
    total_insert_messages = []

    #Total number of inserts for ith experiment
    total_inserts = []

    avg_insert_messages = []

    #Total number of messages in deletes for ith experiment
    total_delete_messages = []

    #Total number of deletes for ith experiment
    total_deletes = []

    avg_delete_messages = []

    #Finger table stats for ith experiment
    finger_table_hits = []
    finger_table_misses = []
    finger_table_hitratio = []

    #N
    n = []

    def collect(self, N):
        stats = Stats()
        self.total_lookup_messages.append(stats.total_lookup_messages)

        self.total_lookups.append(stats.total_lookups)

        self.avg_lookup_messages.append(float(stats.total_lookup_messages)/float(stats.total_lookups))

        self.total_insert_messages.append(stats.total_insert_messages)

        self.total_inserts.append(stats.total_inserts)

        self.avg_insert_messages.append(float(stats.total_insert_messages)/float(stats.total_inserts))

        self.total_delete_messages.append(stats.total_delete_messages)

        self.total_deletes.append(stats.total_deletes)

        self.avg_delete_messages.append(float(stats.total_delete_messages)/float(stats.total_deletes))

        self.finger_table_hits.append(stats.finger_table_hits)

        self.finger_table_misses.append(stats.finger_table_misses)

        self.finger_table_hitratio.append(float(stats.finger_table_hits)/float(stats.finger_table_hits + stats.finger_table_misses))

        self.n.append(N)