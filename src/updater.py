
from groundStation.groundStation import groundStation
from groundStation.updater import updater, update_options
from groundStation.system import SystemValues

if __name__ == '__main__':
    opts = update_options()
    opts2 = opts.getOptions()
    print(opts2)
    csp = updater(opts2)
    if (csp.send_update() == True):
        print("Update sent successfully")
    else:
        print("Update Failed")