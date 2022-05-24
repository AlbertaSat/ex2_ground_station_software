
from groundStation.groundStation import groundStation
from groundStation.ftp import ftp, ftp_options
from groundStation.system import SystemValues

if __name__ == '__main__':
    opts = ftp_options()
    opts2 = opts.getOptions()
    csp = ftp(opts2)
    csp.start_transfer()