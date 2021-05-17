import time
import shlex
import getopt
import sys
import signal
import requests
from krtc import KerberosTicket
from subprocess import check_call

# bsub -q psfehhiprioq -o logs/log-\%J.out -n 16 mpirun python mfxlv7018.py -r 13

queue = 'psfehhiprioq' # 'psnehhiprioq' #'psfehhiprioq'
nproc = 4
nnode = 4
exec_file = 'make_smalldata.py'
experiment = 'cxix46119'

def get_current_run():
    krbheaders = KerberosTicket('HTTP@pswww.slac.stanford.edu').getAuthHeaders()
    url = 'https://pswww.slac.stanford.edu/ws-kerb/lgbk/lgbk/%s/ws/current_run' %experiment
    respone = requests.get(url, headers=krbheaders)
    if respone.status_code != 200:
        print('Error in request %d' % respone.status_code)
    return respone.json()['value']['num']


def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

current_run = get_current_run()
print('Start looking for new runs')
print('current run is: ',current_run)

def main(argv):
    #parse args
    Length = None
    run_num = None
    try:
        opts, args = getopt.getopt(argv,"hr:L:",["run=","Length="])
    except getopt.GetoptError:
        print('usage: ')
        print('<script> -r <run number> or <script> --run= <run number>')
        print('<script> -L <num shots> or <script> --Length= <num shots>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('Oops.  You entered a script argument wrong.  Usage: ')
            print('<script> -r <run number> or <script> --run= <run number>')
            print('<script> -L <num shots> or <script> --Length= <num shots>')
            sys.exit()
        elif opt in ("-r", "--run"):
            run_num = int(arg)
        elif opt in ("-L", "--Length"):
            Length = int(arg)
          
    if run_num is None:
        run_num = get_current_run()
    
    current_run = run_num
    signal.signal(signal.SIGINT, signal_handler)
    while True:
        next_run = get_current_run()
        if next_run > current_run:
            print(f'New run {next_run} at {time.ctime()}')
            cmd_str = f"sbatch -p {queue} -N {nnode} -n {nproc} --wrap=\"mpirun python {exec_file} -r {current_run}\""
            print('executing cmd: ',cmd_str,' !')
            check_call(shlex.split(cmd_str))
            current_run += 1
        time.sleep(60.0)
        
if __name__ == "__main__":
    main(sys.argv[1:])
