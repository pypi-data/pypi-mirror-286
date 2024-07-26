# -*- coding: utf-8 -*-

import cohesity_management_sdk.models_v2.no_sql_protection_group_object_params

class CassandraProtectionGroupParams(object):

    """Implementation of the 'CassandraProtectionGroupParams' model.

    Specifies the parameters for Cassandra Protection Group.

    Attributes:
        objects (list of NoSqlProtectionGroupObjectParams): Specifies the
            objects to be included in the Protection Group.
        concurrency (int): Specifies the maximum number of concurrent IO
            Streams that will be created to exchange data with the cluster.
        bandwidth_mbps (long|int): Specifies the maximum network bandwidth
            that each concurrent IO Stream can use for exchanging data with
            the cluster.
        exclude_object_ids (list of long|int): Specifies the objects to be
            excluded in the Protection Group.
        source_id (long|int): Object ID of the Source on which this protection
            was run .
        source_name (string): Specifies the name of the Source on which this
            protection was run.
        data_centers (list of string): Only the specified data centers will be
            considered while taking backup. The keyspaces having replication
            strategy 'Simple' can be backed up only if all the datacenters for
            the cassandra cluster are specified. For any keyspace having
            replication strategy as 'Network', all the associated data centers
            should be specified.
        is_log_backup (bool): Specifies the type of job for Cassandra. If true,
            only log backup job will be scheduled for the source. This requires
            a policy with log Backup option enabled.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "objects":'objects',
        "concurrency":'concurrency',
        "bandwidth_mbps":'bandwidthMBPS',
        "exclude_object_ids":'excludeObjectIds',
        "source_id":'sourceId',
        "source_name":'sourceName',
        "data_centers":'dataCenters',
        "is_log_backup":'isLogBackup'
    }

    def __init__(self,
                 objects=None,
                 concurrency=None,
                 bandwidth_mbps=None,
                 exclude_object_ids=None,
                 source_id=None,
                 source_name=None,
                 data_centers=None,
                 is_log_backup=None):
        """Constructor for the CassandraProtectionGroupParams class"""

        # Initialize members of the class
        self.objects = objects
        self.concurrency = concurrency
        self.bandwidth_mbps = bandwidth_mbps
        self.exclude_object_ids = exclude_object_ids
        self.source_id = source_id
        self.source_name = source_name
        self.data_centers = data_centers
        self.is_log_backup = is_log_backup


    @classmethod
    def from_dictionary(cls,
                        dictionary):
        """Creates an instance of this model from a dictionary

        Args:
            dictionary (dictionary): A dictionary representation of the object as
            obtained from the deserialization of the server's response. The keys
            MUST match property names in the API description.

        Returns:
            object: An instance of this structure class.

        """
        if dictionary is None:
            return None

        # Extract variables from the dictionary
        objects = None
        if dictionary.get('objects') != None:
            objects = list()
            for structure in dictionary.get('objects'):
                objects.append(cohesity_management_sdk.models_v2.no_sql_protection_group_object_params.NoSqlProtectionGroupObjectParams.from_dictionary(structure))
        concurrency = dictionary.get('concurrency')
        bandwidth_mbps = dictionary.get('bandwidthMBPS')
        exclude_object_ids = dictionary.get('excludeObjectIds')
        source_id = dictionary.get('sourceId')
        source_name = dictionary.get('sourceName')
        data_centers = dictionary.get('dataCenters')
        is_log_backup = dictionary.get('isLogBackup')

        # Return an object of this model
        return cls(objects,
                   concurrency,
                   bandwidth_mbps,
                   exclude_object_ids,
                   source_id,
                   source_name,
                   data_centers,
                   is_log_backup)


