#!/usr/bin/env python

# File: filter-instances.py 
# Description: This is an example script that you can author or modify that retrieves 
#              a list of instances from the Relay Interface (in the form of parameters)
#              and filters the instances that are the tag 'created by' 'Deimos'. It then sets the output
#              variable `instanceIDs` to the list of instances that have this tag. 
# Inputs:
#   - created_by - tag indicating the owner of the instance
#   - instances - List of instances to evaluate 
# Outputs:
#   - instanceIDs - list of instance IDs to stop in the next step

from relay_sdk import Interface, Dynamic as D

relay = Interface()

# Tag names (user-configurable)
CREATEDBY = relay.get(D.CreatedBy)
TAGNAME = relay.get(D.TagName)

to_stop = []
to_keep = []

instances = filter(lambda i: i['State']['Name'] == 'running', relay.get(D.instances))
for instance in instances:
    try:
        if instance['Tags']is None: 
            to_keep.append(instance['InstanceId'])
        else:
            for tag in instance['Tags']:
                if tag['Key'] == TAGNAME and tag['Value'] == CREATEDBY:
                    to_keep.append(instance['InstanceId'])
    except Exception as e:
            print('\nEC2 instance {0} not considered for termination because of a processing error: {1}'.format(instance['InstanceId'], e))

print('\nFound {0} instances without the tag createdby = ' + CREATEDBY + ' to keep:'.format(len(to_keep)))
print(*[instance_id for instance_id in to_keep], sep = "\n") 

print('\nFound {0} instances with the tag created_by = ' + CREATEDBY + ' to stop:'.format(len(to_stop)))
print(*[instance_id for instance_id in to_stop], sep = "\n") 

relay.outputs.set('instanceIDs', to_stop)
