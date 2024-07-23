import json

def addGroup(json_array, group):
    if json_array == '':
        json_array = '{}'
    data = json.loads(json_array)
    if 'groups' not in data:
        data['groups'] = {}
    if group in data['groups']:
        print('Error: Group, ' + group + ' name already exists.')
    else:
        data['groups'][group] = []
    return json.dumps(data, indent=4)

def removeGroup(json_array, group):
    if json_array == '':
        json_array = '{}'
    data = json.loads(json_array)
    if 'groups' not in data:
        data['groups'] = {}
    if group in data['groups']:
        del data['groups'][group]
    else:
        print('Error: Not found group, ' + group)
    return json.dumps(data, indent=4)

def addObject(json_array, group, user):
    if json_array == '':
        json_array = '{}'
    data = json.loads(json_array)
    if 'groups' not in data:
        print('Error: Not found groups')
    else:
        if group not in data['groups']:
            print('Error: Not found group, ' + group)
        else:
            if user not in data['groups'][group]:
                data['groups'][group].append(user)
            else:
                print('Error: Object, ' + user + ' already exists.')
    return json.dumps(data, indent=4)

def eraseObject(json_array, group, user):
    if json_array == '':
        json_array = '{}'
    data = json.loads(json_array)
    if 'groups' not in data:
        print('Error: Not found groups')
    else:
        if group not in data['groups']:
            print('Error: Not found group, ' + group)
        else:
            if user not in data['groups'][group]:
                print('Error: Not found object, ' + user)
            else:
                data['groups'][group].remove(user)
    return json.dumps(data, indent=4)

def userExists(json_array, group, user):
    exists = False
    if json_array == '':
        json_array = '{}'
    data = json.loads(json_array)
    if 'groups' not in data:
        print('Error: Not found groups')
        exists = False
    else:
        if group not in data['groups']:
            print('Error: Not found group, ' + group)
            exists = False
        else:
            if user not in data['groups'][group]:
                exists = False
            else:
                exists = True
    return exists

def groupExists(json_array, group):
    exists = False
    if json_array == '':
        json_array = '{}'
    data = json.loads(json_array)
    if 'groups' not in data:
        print('Error: Not found groups')
        exists = False
    else:
        if group not in data['groups']:
            exists = False
        else:
            exists = True
    return exists

def meet(json_array, group, object_name):
    if json_array == '':
        json_array = '{}'
    try:
        data = json.loads(json_array)
    except json.JSONDecodeError:
        return False
    if 'groups' not in data:
        print('Error: Not found groups')
        return False

    def find_object_in_group(group, obj, visited=None):
        if visited is None:
            visited = set()
        if group in visited:
            return False
        visited.add(group)
        if group in data['groups']:
            if obj in data['groups'][group]:
                return True
            for member in data['groups'][group]:
                if member.startswith('group:'):
                    subgroup = member.split(':')[1]
                    if find_object_in_group(subgroup, obj, visited):
                        return True
                elif member.startswith('user:'):
                    continue
        return False

    if not groupExists(json_array, group):
        print('Error: Not found group, ' + group)
        return False
    if object_name.startswith('user:') or object_name.startswith('group:'):
        return find_object_in_group(group, object_name)
    else:
        print('Error: Invalid object format ' + object_name)
        return False

def replaceObject(json_array, old_name, new_name):
    if json_array == '':
        json_array = '{}'
    data = json.loads(json_array)
    if 'groups' not in data:
        print('Error: Not found groups')
        return json.dumps(data, indent=4)
    for group, users in data['groups'].items():
        for i in range(len(users)):
            if users[i] == old_name:
                users[i] = new_name
    return json.dumps(data, indent=4)

def removeObject(json_array, user):
    if json_array == '':
        json_array = '{}'
    data = json.loads(json_array)
    if 'groups' not in data:
        print('Error: Not found groups')
        return json.dumps(data, indent=4)
    for group, users in data['groups'].items():
        if user in users:
            users.remove(user)
    return json.dumps(data, indent=4)

def renameGroup(json_array, old_name, new_name):
    if json_array == '':
        json_array = '{}'
    data = json.loads(json_array)
    if 'groups' not in data:
        print('Error: Not found groups')
        return json.dumps(data, indent=4)
    if old_name not in data['groups']:
        print('Error: Not found group, ' + old_name)
        return json.dumps(data, indent=4)
    if new_name in data['groups']:
        print('Error: Group, ' + new_name + ' name already exists.')
        return json.dumps(data, indent=4)
    data['groups'][new_name] = data['groups'].pop(old_name)
    return json.dumps(data, indent=4)

def renameObject(json_array, group, old_name, new_name):
    json_array = eraseObject(json_array, group, old_name)
    json_array = addObject(json_array, group, new_name)
    return json_array

def listGroups(json_array):
    # List all groups
    return list(json_array["group"].keys())

def listObjects(json_array):
    # List all users in all groups
    users = set()
    for members in json_array["group"].values():
        for member in members:
            if member.startswith("user:"):
                users.add(member)
    return list(users)

def listObjectsOfGroup(json_array, group):
    # List all users in a specific group
    if group in json_array["group"]:
        return [member for member in json_array["group"][group] if member.startswith("user:")]
    return 

def objectIsInAnyGroup(json_array, name):
    for members in json_array["group"].values():
        if name in members:
            return True
    return False

def getGroupsOfObject(json_array, name):
    groups = []
    for group, members in json_array["group"].items():
        if name in members:
            groups.append(group)
    return groups

def getSubgroups(json_array, group):
    if group not in json_array["group"]:
        return []
    return [member.split(":")[1] for member in json_array["group"][group] if member.startswith("group:")]

