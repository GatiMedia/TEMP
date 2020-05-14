
### GBK PYTHON SNIPPETS 101 ###


### FIRST STEP ###


print ("Hello World!")


### USING VARIABLE ###


name = 'Attila'
print ('Hello ' + name + '!')

name = 'Attila'
print("Hello %s!" % name)

name = 'Attila'
print("Hello {}!".format(name))


### CREATE A NODE ###
## Functions: createNode, setValue ##


nuke.createNode("Blur")

# Can check node's Class with the `i` hotkey
nuke.createNode("Tracker4")

# Can call nodes that are removed from GUI
nuke.createNode("Blocky")

# Set a value
nuke.createNode("Blur")['size'].setValue(80)

# Set multiple values using a variable
m = nuke.createNode("Blur")
m['channels'].setValue("rgb")
m['size'].setValue(50)
m['mix'].setValue(.5)
m['label'].setValue("Size: [value size]\nChannels: [value channels]\nMix: [value mix]")

# Creating node for scripting
nuke.nodes.Blur()

nuke.nodes.Blur(mix=.5,size=10)


### GETTING KNOB VALUE ###
## Functions: toNode, value, getValue, knob ###


# Calling knobs as list items
nuke.toNode('Blur1')["channels"].value()

# Calling knobs with a function
nuke.toNode('Blur1').knob("channels").value()

nuke.toNode('Blur1')["filter"].getValue()


### SETTING KNOB VALUE ###
## Functions: setValue ##

# Setting single value
nuke.toNode('Blur1')["size"].setValue(10)

# Setting multiple values
b = nuke.toNode('Blur1')
b["size"].setValue(20)
b["mix"].setValue(.8)
b["filter"].setValue(0)
b["channels"].setValue("rgb")



### SETTING EXPRESSION VALUE ###
## Functions: setExpression ##

nuke.toNode('Blur1')["size"].setExpression('Blur2.size * 2')

nuke.toNode('Transform1')["filter"].setExpression("Transform2.filter")


### REMOVE ANIMATION / EXPRESSION ###
## Functions: clearAnimated ##


nuke.toNode('Transform1')["filter"].clearAnimated()


### CREATE MULTIPLE NODES WITH `FOR LOOP` ###
## Functions: range ##


for i in range(15):
    i = nuke.createNode("Blur")
    i["channels"].setValue('rgb')
    i["size"].setExpression('Blur1.size')\


### CONNECT MULTIPLE NODES TO A SINGLE NODE ###
## Functions: selectedNodes, setInput ##

t = nuke.toNode('Transform1')

nodes = nuke.selectedNodes()
for i in nodes:
    i.setInput(0, t)
    i.setInput(1, None)


### FORMATTING VALUES ###


# Interger - int(x)

x = 12.8
print type(x)
x = int(x)
print type(x)
print x

# Float - float(x)

x = 12
print type(x)
x = float(x)
print type(x)
print x

# String - str(x)

x = 12.5
print type(x)
x = str(x)
print type(x)
print x


### RUN ON ANY SELECTED NODES ###
## Functions: selectedNodes ##


nodes = nuke.selectedNodes()
for node in nodes:
    try:
        node.knob("size").setValue(5)
    except Exception:
        pass


### RUN ON ALL NODES IN A SCRIPT ###
## Functions: allNodes ##


nodes = nuke.allNodes()
for node in nodes:
    try:
        node.knob("size").setValue(20)
    except Exception:
        pass


### RUN AN ALL SPECIFIED CLASSES ###


nodes = nuke.allNodes('Merge2')
for node in nodes:
    node.knob("mix").setValue(.5)


### RUN AN SELECTED SPECIFIED CLASSES ###


nodes = nuke.selectedNodes('Merge2')
for node in nodes:
    try:
        node.knob("mix").setValue(.8)
    except Exception:
        pass


### RUN ON ALL MULTIPLE CLASSES ###


nodes_classes = ["Read", "PostageStamp", "Constant", "ColorBars", "CheckerBoard2", "ColorWheel"]

for node in nuke.allNodes(group=nuke.root()):
    if node.Class() in nodes_classes:
        try:
            node["postage_stamp"].setValue(True)
        except Exception:
            pass


### RUN ON SELECTED MULTIPLE CLASSES ###


nuke.root().begin()

nodes_classes = ["Read", "PostageStamp", "Constant", "ColorBars", "CheckerBoard2", "ColorWheel"]

for node in nuke.selectedNodes():
    if node.Class() in nodes_classes:
        try:
            node["postage_stamp"].setValue(True)
        except Exception:
            pass
nuke.root().end()


### PATH FOR YOUR NUKE FOLDER ###


nuke.pluginPath()


### PERFORMANCE TIMER ###

#start
nuke.startPerformanceTimers()

#reset
nuke.resetPerformanceTimers()

#stop
nuke.stopPerformanceTimers()


# https://learn.foundry.com/nuke/developers/90/pythondevguide/performance.html

### NOTES ###

# For checkboxes the value can be True or False that equals to 1 or 0

# For dropdown menu values can be the name of the option or the serial number of the option starting with 0 from the top

# To find the Class of the node select it and press `i` over the NodeGraph

"""
Useful links
Foundry learn:
https://learn.foundry.com/nuke/developers/120/pythondevguide/index.html
Nuke API:
https://learn.foundry.com/nuke/developers/120/pythonreference/
Andrea Geremia Python tips:
http://www.andreageremia.it/tutorial_python_tcl.html
"""
