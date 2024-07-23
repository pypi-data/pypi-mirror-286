import io
import json
import locale
import os
import subprocess
import threading
import time
import traceback
from datetime import datetime

from ascript.ios.developer import ws

run_process = None


def read_from_stream(stream, t):
    while True:
        line = stream.readline()
        line = line.replace("\n", "").replace("\r\n", "").replace("\r", "")
        if line:
            msg = {"msg": line, "type": t, "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            print(json.dumps(msg))
            ws.send_message(json.dumps(msg))
        else:
            break


def run_worker(cmds, module_space):
    global run_process

    if run_process is not None:
        run_process.kill()
        print("wait...kill")

    print("enter")

    env = os.environ.copy()
    env['PYTHONUNBUFFERED'] = '1'
    env['PYTHONIOENCODING'] = 'utf-8'

    # print("env----",env)

    print(locale.getdefaultlocale())
    # os.environ["PYTHONIOENCODING"] = 'gb2312'

    # run_process = subprocess.Popen(cmds, cwd=module_space, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env,
    #                                encoding='utf-8', universal_newlines=True, text=True, errors='ignore')

    run_process = subprocess.Popen(cmds, cwd=module_space, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env,
                                   encoding='utf-8', universal_newlines=True, text=True, errors='ignore')

    ws.send_message("启动成功")
    try:

        stdout_thread = threading.Thread(target=read_from_stream, args=(run_process.stdout, 'i'))
        stderr_thread = threading.Thread(target=read_from_stream, args=(run_process.stderr, 'e'))
        stdout_thread.start()
        stderr_thread.start()
        run_process.wait()

        stdout_thread.join()
        stderr_thread.join()

        # while True:
        #     print("read-start")
        #     for line in io.TextIOWrapper(run_process.stdout, encoding='utf-8'):
        #         # msgstr = line.strip()
        #         line = line.replace("\n", "").replace("\r\n", "").replace("\r", "")
        #         msg = {"msg": line, "type": "i", "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        #         print(json.dumps(msg))
        #         ws.send_message(json.dumps(msg))
        #
        #     for line in io.TextIOWrapper(run_process.stderr, encoding='utf-8'):
        #         line = line.replace("\n", "").replace("\r\n", "").replace("\r", "")
        #         msg = {"msg": line, "type": "e", "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        #         print(line)
        #         ws.send_message(json.dumps(msg))
        #
        #     if run_process.poll() is None:
        #         break

    except Exception as e:
        print(e)
        traceback.print_exc()
        pass
    finally:
        print("运行结束-")
        msg = {"msg": "运行结束", "type": "e", "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        ws.send_message(json.dumps(msg))
        run_process = None

    # while run_process.poll() is None:
    #     line = run_process.stdout.readline()
    #     if line:
    #         print(line)
    #         time.sleep(0.01)
    #
    #     for line in run_process.stdout:
    #         print(line)
    #
    #     err = run_process.stderr.read()
    #     if err:
    #         print(err)


def run_script(cmd, module_space):
    threading.Thread(target=run_worker, args=(cmd, module_space)).start()
