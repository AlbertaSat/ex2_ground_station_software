from system import SystemValues

f = open("CommandDocs.txt", "w")
system = SystemValues()

f.write('\t\t\t\t-- Ex-Alta 2 Ground Station Commands --\n' +
'Note: arguments and return types are given as numpy types\n\n\n')

for services in system.SERVICES:
    print(services)
    subservice = system.SERVICES[services]['subservice']
    for subName in subservice.keys():
        f.write(services + '.' + subName + ':\n')

        sub = subservice[subName]
        inoutInfo = sub['inoutInfo']

        args = 'None' if inoutInfo['args'] is None else ', '.join(map(str, inoutInfo['args']))
        returns = 'None' if inoutInfo['returns'] is None else repr(inoutInfo['returns'])
        info = 'None' if not 'what' in sub else sub['what']
        f.write(
        '\t\tAbout: ' + info + '\n'
        '\t\tArguments: [' + args + ']\n' +
        '\t\treturn values: ' + returns + '\n'
        '\t\tport: ' + str(system.SERVICES[services]['port']) +
        '\t\tsubport: ' + str(sub['subPort']) + '\n\n\n')
