### GBK PYTHON SNIPPETS 101 ###


### FIRST STEP ###


print "Hello World!"


### USING VARIABLE ###


name = 'Attila'
print ('Hello ' + name + '!')


### CREATE A NODE ###
## Functions: createNode, setValue ##


nuke.createNode("Blur")

nuke.createNode("Tracker4")

nuke.createNode("Blocky")


nuke.createNode("Blur")['size'].setValue(80)


m = nuke.createNode("Blur")
m['channels'].setValue("rgb")
m['size'].setValue(50)
m['mix'].setValue(.5)
m['label'].setValue("Size: [value size]\nChannels: [value channels]\nMix: [value mix]")


nuke.nodes.Blur()


nuke.nodes.Blur(mix=.5,size=10)


### GETTING KNOB VALUE ###
## Functions: toNode, value, getValue, knob ###


nuke.toNode('Blur1')["channels"].value()

nuke.toNode('Blur1').knob("channels").value()

nuke.toNode('Blur1')["filter"].getValue()


### SETTING KNOB VALUE ###
## Functions: setValue ##


nuke.toNode('Blur1')["size"].setValue(3)


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
    i["size"].setExpression('Blur1.size')


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


### Run on any selected nodes ###
## Functions: selectedNodes ##


nodes = nuke.selectedNodes()
for node in nodes:
    try:
        node.knob("size").setValue(5)
    except Exception:
        pass


### Run on all nodes in a script ###
## Functions: allNodes ##


nodes = nuke.allNodes()
for node in nodes:
    try:
        node.knob("size").setValue(20)
    except Exception:
        pass


### Run an all specified Classes ###


nodes = nuke.allNodes('Merge2')
for node in nodes:
    node.knob("mix").setValue(.5)


### Run an selected specified Classes ###


nodes = nuke.selectedNodes('Merge2')
for node in nodes:
    try:
        node.knob("mix").setValue(.8)
    except Exception:
        pass


### Run on all multiple Classes ###


nodes_classes = ["Read", "PostageStamp", "Constant", "ColorBars", "CheckerBoard2", "ColorWheel"]

for node in nuke.allNodes(group=nuke.root()):
    if node.Class() in nodes_classes:
        try:
            node["postage_stamp"].setValue(True)
        except Exception:
            pass


### Run on selected multiple Classes ###


nuke.root().begin()

nodes_classes = ["Read", "PostageStamp", "Constant", "ColorBars", "CheckerBoard2", "ColorWheel"]

for node in nuke.selectedNodes():
    if node.Class() in nodes_classes:
        try:
            node["postage_stamp"].setValue(True)
        except Exception:
            pass
nuke.root().end()


### Path for your nuke folder ###


nuke.pluginPath()

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
"""
