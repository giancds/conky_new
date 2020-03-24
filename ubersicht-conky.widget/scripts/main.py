#!/usr/bin/env python
import datetime
import platform
import os
import time
import calendar
import datetime

import psutil

DOT = '.'
GB = 1e+9
UPTIME = psutil.boot_time()

ICON_CAL = '<img name="hdicon" src="ubersicht-conky.widget/icons/calendar.svg" width="18" height="18"/>'
ICON_CPU = '<img name="hdicon" src="ubersicht-conky.widget/icons/cpu.svg" width="15" height="15"/>'
ICON_DOWN = '<img name="hdicon" src="ubersicht-conky.widget/icons/download.svg" width="15" height="15"/>'
ICON_HD = '<img name="hdicon" src="ubersicht-conky.widget/icons/hard-disk.svg" width="15" height="15"/>'
ICON_PIN = '<img name="hdicon" src="ubersicht-conky.widget/icons/pin.svg" width="15" height="15"/>'
ICON_PROC = '<img name="hdicon" src="ubersicht-conky.widget/icons/server.svg" width="15" height="15"/>'
ICON_RAM = '<img name="hdicon" src="ubersicht-conky.widget/icons/ram.svg" width="15" height="15"/>'
ICON_UP = '<img name="hdicon" src="ubersicht-conky.widget/icons/upload.svg" width="15" height="15"/>'
ICON_SYS = '<img name="hdicon" src="ubersicht-conky.widget/icons/monitor.svg" width="15" height="15"/>'


def get_system_info():
    system = platform.system()
    release = platform.release()
    uptime = get_uptime()
    cpuload = get_cpu_load()
    ramload = get_ram_load()
    procs = get_processes_load()
    # procs = "EMPTY_PANEL"
    string = """
        <div id='system_info' class='row font-weight-bold'>
            System&nbsp;<font style='font-size:8px'>{0:.^75s}</font>
        </div>

        <div class='row'>
            <div class='col-1 text-left'>
                {1}
            </div>
            <div id='kernel-info' class='col-4 text-left'>
                Kernel:
            </div>
            <div id='kernel-info' class='col-6 text-right'>
                {2} {3}
            </div>
        </div>
        <div id='system_info' class='row'>
            <div class='col-1 text-left'>

            </div>
            <div id='uptime' class='col-4 text-left'>
                Uptime:
            </div>
            <div id='uptime-info' class='col-6 text-right'>
            {4}
            </div>
        </div>
        {5}
        {6}
        {7}
    """.format(DOT, ICON_SYS, system, release, uptime, cpuload, ramload, procs)
    return string


def get_uptime():
    uptime_total_seconds = time.time() - UPTIME
    uptime_days = int(uptime_total_seconds / 24 / 60 / 60)
    uptime_hours = int(uptime_total_seconds / 60 / 60 % 24)
    uptime_minutes = int(uptime_total_seconds / 60 % 60)
    return "{}d {}h {}m".format(uptime_days, uptime_hours, uptime_minutes)


def get_cpu_load():
    cpuload = psutil.cpu_percent(percpu=True)
    string = ""
    for c, cpu in enumerate(cpuload):
        string += """
        <div class='row align-items-center'>

            <div class='col-1'>
                {0}
            </div>

            <div class='col-5 text-left'>
                CPU{1}:&nbsp;<b>{2}%</b>
            </div>

            <div class='col-5 text-right'>
                <div class="progress" style="height: 4px; background: #212526 !important; ">
                    <div class="progress-bar" role="progressbar" style="width: {3}%; background: #51751E;" aria-valuenow="{4}" aria-valuemin="0" aria-valuemax="100"></div>
                </div>
            </div>

        </div>
    """.format(ICON_CPU if c == 0 else '', c + 1, cpu, int(cpu), int(cpu))

    return string


def get_ram_load():
    memory = psutil.virtual_memory()
    mempct = memory.percent
    memtotal = memory.total
    memavail = memory.available
    memused = memtotal - memavail
    string = """
        <div class='row'>

            <div class='col-1'>
                {}
            </div>

            <div class='col-4'>
                RAM:&nbsp;<b>{:.0f}%</b>
            </div>

        </div>

        <div class='row'>

            <div class='col-1'>
            </div>

            <div class='col-5 text-right'>
                F:&nbsp;<b>{:.2f}GiB</b>
            </div>

            <div class='col-5 text-right'>
                U:&nbsp;<b>{:.2f}GiB</b>
            </div>

        </div>

    """.format(ICON_RAM, mempct, memavail / 1e+9, memused / 1e+9)
    return string


def get_processes_load():
    # proclist = sh.ps("-Acro comm,pcpu,pmem").split("\n")
    # proclist = os.popen('ps -Acro comm,pcpu,pmem | head -n 11').read().split("\n")
    # top = [proclist[i].split() for i in range(1, 11)]
    procs = []
    for p in psutil.process_iter(
            attrs=['memory_percent', 'cpu_percent', 'name']):
        with p.oneshot():
            p.dict = p.as_dict(['memory_percent', 'cpu_percent', 'name'])
            procs.append(p)
    top = [(p.info['name'], p.info['cpu_percent'], p.info['memory_percent'])
           for p in sorted(psutil.process_iter(
               attrs=['name', 'cpu_percent', 'memory_percent']),
                           reverse=True,
                           key=lambda p: p.info['cpu_percent']
                           if p.info['cpu_percent'] is not None else 0.0)
           if p.info['cpu_percent'] is not None][0:11]
    string = """
      <div class='row'>

        <div class='col-1'>
            {}
        </div>

        <div class='col-5 font-weight-bold'>
          Processes
        </div>

        <div class='col-2 text-center font-weight-bold'>
          CPU
        </div>

        <div class='col-2 font-weight-bold'>
          Ram
        </div>

      </div>
    """.format(ICON_PROC)
    for proc in top:
        if proc[0] != "Python":
            string += """
            <div class='row'>

                <div class='col-1'>

                </div>

              <div class='col-5'>
                &nbsp;&nbsp;{:.9s}
              </div>

              <div class='col-2 text-center'>
                {:.4}
              </div>

              <div class='col-2 text-center'>
                {:.4}
              </div>

            </div>
      """.format(proc[0], str(proc[1]), str(proc[2]))
    return string


def get_time_info():
    calendar.setfirstweekday(calendar.SUNDAY)
    now = datetime.datetime.now()
    string = """
    <div class='row font-weight-bold'>
        Date&nbsp;<font style='font-size:8px'>{0:.^82s}</font>
    </div>
    """.format(DOT)

    now = datetime.datetime.today()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    cal = calendar.month(int(year), int(month))
    cal = cal.replace(' ', '&nbsp;&nbsp;')
    cal = cal.replace('\n', '<br/>')
    cal = cal.replace(day, "<b><font style='font-size:11px; color: #51751E;'>{0}</font></b>".format(day))
    string += """
    <div class='row align-items-center'>

        <div class='col-3 text-right '>

        </div>

        <div class='col-3 '>
            <font style='font-size:48px'>{0:%d}</font>
        </div>

        <div class='col-4 '>
            <font style='font-size:10px'>{0:%b} {0:%Y}</font>
            <br/>{0:%A}</br>{0:%H}:{0:%M}
        </div>

    </div>

    <div class='row'>
        <div class='col-2'>
            {1}
        </div>
        <div class='col'>
            {2}
        </div>
    </div>


  """.format(now, ICON_CAL, cal)
    return string


def get_hd_info():
    disks = [
        disk for disk in psutil.disk_partitions()
        if disk.mountpoint != "/private/var/vm"
    ]
    # disks = psutil.disk_partitions()
    string = """
        <div class='row font-weight-bold'>
            HD&nbsp;<font style='font-size:8px'>{0:.^85s}</font>
        </div>
        """.format(DOT)
    for disk in disks:
        if disk.mountpoint != "/":
            diskname = disk.mountpoint.split("/")[-1]
        else:
            diskname = disk.mountpoint
        usage = psutil.disk_usage(disk.mountpoint)
        string += """
        <div class='row'>

            <div class='col-1 pr-2'>
                {}
            </div>

          <div class='col-8 text-left'>
            {}: <b>{:.1f}%</b>
          </div>

        </div>

        <div class='row'>

            <div class='col-1'>
            </div>

          <div class='col-5 text-left'>
            F:<b>{:.1f} GiB </b>
          </div>

          <div class='col-5 text-right'>
            U:<b>{:.1f} GiB</b>
          </div>

        </div>
    """.format(ICON_HD, diskname, 100.0 - usage.percent, usage.free / GB,
               usage.used / GB)
    return string


def get_network_info():
    addrs = psutil.net_if_addrs()
    string = """
    <div class='row font-weight-bold text-left'>
        Network&nbsp;<font style='font-size:8px'>{0:.^75s}</font>
    </div>

    """.format(DOT)
    net_counters = psutil.net_io_counters()
    bytes_sent_old = bytes2human(net_counters.bytes_sent)
    bytes_recv_old = bytes2human(net_counters.bytes_recv)
    time.sleep(0.05)
    net_counters_new = psutil.net_io_counters()
    bytes_sent_new = bytes2human(net_counters_new.bytes_sent -
                                 net_counters.bytes_sent)
    bytes_recv_new = bytes2human(net_counters_new.bytes_recv -
                                 net_counters.bytes_recv)
    string += """
        <div class='row pb-1'>

            <div class='col-1'>
                {}
            </div>

            <div class='col-5 text-left'>
                Up: <b>{} {}</b>
            </div>


            <div class='col-5 text-right'>
                Total: <b>{:.1f} {}</b>
            </div>

        </div>

        <div class='row pb-1'>

            <div class='col-1'>
                {}
            </div>

            <div class='col-5  text-left'>
                Down: <b>{} {}</b>
            </div>

            <div class='col-5 text-right'>
                Total: <b>{:.1f} {}</b>
            </div>

        </div>

    """.format(ICON_UP, int(bytes_sent_new[0]), bytes_sent_new[1], bytes_sent_old[0],
               bytes_sent_old[1], ICON_DOWN, int(bytes_recv_new[0]),
               bytes_recv_new[1], bytes_recv_old[0], bytes_recv_old[1])

    string += """ <div class='row'> """
    for key in addrs:
        address = addrs[key]
        if address[0].broadcast is not None:
            string += """
                <div class='col-1'>
                    {0}
                </div>

                <div class='col-4'>
                    Local IP:
                </div>

                <div class='col-6 text-right'>
                    {1}
                </div>

            """.format(ICON_PIN, address[0].broadcast)
    string += '</div>'
    return string


def bytes2human(n):
    # From sample script for psutils
    """
    >>> bytes2human(10000)
    '9.8 K'
    >>> bytes2human(100001221)
    '95.4 M'
   """
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return value, s
    return n, 'B'


def get_info():
    hd_info = get_hd_info()
    system_info = get_system_info()
    time_info = get_time_info()
    network_info = get_network_info()
    # TODO: separar as colunas em divs de rows
    string = """
    <div class='container'>
        {0}
    </div>
    <div class='container'>
        {1}
    </div>
    <div class='container'>
        {2}
    </div>
    <div class='container'>
        {3}
    </div>


  """.format(system_info, time_info, hd_info, network_info)
    return string


if __name__ == "__main__":
    _ = get_info()
    print(get_info())