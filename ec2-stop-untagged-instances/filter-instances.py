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
TAGNAME = relay.get(D.Tag_Name1)
TAGVALUE = relay.get(D.Tag_Value1)

to_stop = []
to_keep = []
to_keep_notag = []

instances = relay.get(D.instances)
for instance in instances:
#    try:
#        if instance['Tags']is None: 
#            to_keep_notag.append(instance['InstanceId'])
        for tag in instance['Tags']:
            if tag['Key'] == TAGNAME:
                if tag['Value'] == TAGVALUE:
                    to_stop.append(instance['InstanceId'])
#        else:
#            to_keep.append(instance['InstanceId'])
#    except Exception as e:
#            print('\nEC2 instance {0} not considered for termination because of a processing error: {1}'.format(instance['InstanceId'], e))

#print('\n\nFound {} instances with no tags, check these instances:'.format(len(to_keep_notag)))
#print(*[instance_id for instance_id in to_keep_notag], sep = "\n") 

#print('\nFound {} instances without the tag ' + TAGNAME + ' = ' + TAGVALUE + ' to keep:'.format(len(to_keep)))
#print(*[instance_id for instance_id in to_keep], sep = "\n") 

print('\nFound {0} instances with the tag ' + TAGNAME + ' = ' + TAGVALUE + ' to stop:'.format(len(to_stop)))
print(*[instance_id for instance_id in to_stop], sep = "\n") 

relay.outputs.set('instanceIDs', to_stop)
