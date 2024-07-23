# Vtat
A simple ACL system<br>
[Pypi - Vtat](https://pypi.org/project/vtat/)<br>
[Other Vtats](https://github.com/askofback)
# VTAT(ENGLISH)
## JSON EXAMPLE
```json
{
"groups": {
  "users": [
    "group:other",
    "user:vtat"
  ],
  "other": [
    "user:other"
  ],
}
}
```
## IMPORT
```python
import vtat
```
OR
```python
from vtat import *
```
## FUNCTIONS
### addGroup(json_array, group)
In `json_array` add group, `group`
And return json_array.
### removeGroup(json_array, group)
It remove `group` in `json_array`
and return json_array.
### addObject(json_array, group, name)
In `json_array` add object, `name` in group, `group`
And return json_array
and Object name must be `group:(group name)` or `user:(user name)`.
### eraseObject(json_array, group, name)
It delete `name` in `group` in `json_array`
and return json_array.
and Object name must be `group:(group name)` or `user:(user name)`.
### userExists(json_array, group, user)
It is return `True` or `False`
If in `json_array` in `group` exist `user`,
It return `True`.
If not in `json_array` in `group` exist `user`,
It return `False`.
But Don't use it.(Instead of use `meet()`)
and Uesr must be `group:(group name)` or `user:(user name)`.
### groupExists(json_array, group)
It is return `True` or `False`
If in `json_array` exist `group`,
It return `True`.
If not in `json_array` exist `group`,
It return `False`.
### meet(json_array, group, name)
It return `True` or `False`
If in json_array exist name in group (It works even if there are users in subgroups within the group.)
It return `True`
If not in json_array exist name in group (It works even if there are users in subgroups within the group.)
It return `False`
And name must be `group:(group name)` or `user:(user name)`.
### removeObject(json_array, name)
It delete `name` in all.
And name must be `group:(group name)` or `user:(user name)`.
### replaceObject(json_array, old_name, new_name)
It replace from `old_name` to `new_name` in all groups.
And old_name and new_name must be `group:(group name)` or `user:(user name)`.
### renameGroup(json_array, old_name, new_name)
It rename group from old_name to new_name
### renameObject(json_array, group, old_name, new_name)
It replace from `old_name` to `new_name` in `group` in `json_array`.
And old_name and new_name must be `group:(group name)` or `user:(user name)`.
### (BETA) listGroups(json_array)
It return all groups in `json_array`
### (BETA) listObjects(json_array)
It return all objects in `json_array`
### (BETA) listObjectsOfGroup(json_array, group)
It return objects in `group` in `json_array`
### (BETA) getGroupsOfObject(json_array, name)
It return included `name` all groups.
### (BETA) objectIsInAnyGroup(json_array, name)
It return included `name` any groups.
### (BETA) getSubgroups(json_array, group)
It return subgroups in group.