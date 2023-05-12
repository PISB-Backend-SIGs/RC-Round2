import os
import subprocess
import signal,resource


# codeRunnerPath = os.path.abspath("testsubprocess")
# codeRunnerPath="Clash_RC_2/Code_Runner"

#It will give current file path 
#And our other files are in same folder
FilePath = os.path.dirname(__file__)

#File in which users code is present
PythonFile = f"{FilePath}/code.py"
CppFile = f"{FilePath}/code.cpp"
CFile = f"{FilePath}/code.c"

ip_file_path = open(f'{FilePath}/input.txt','r')

CONTAINER_NAME="container0"

ErrorCodes={
  "AC": 0, 
  "WA": 1, 
  "MLE":2, 
  "TLE":3, 
  "CE": 4, 
  "RE": 5, 
}

ceErrors = [ "SyntaxError:","NameError:","TypeError:","ImportError:","IndentationError:","LogicError:"]
reErrors = ["ZeroDivisionError:","IndexError:","KeyError:","AttributeError:","ValueError:","RuntimeError","StopIteration","RecursionError","OSError"]
#"MemoryError"

# Timeout Signal
#--------------------------------------------------------------------------
TimeoutLimit = 5
def set_time_limit(time_limit):
    def signal_handler(signum, frame):
        raise TimeoutError("Time Limit Exceeded")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(TimeoutLimit)

MemoryLimit = 256*1024*1024
def set_memory_limit():
    resource.setrlimit(resource.RLIMIT_CPU, (TimeoutLimit, TimeoutLimit))
    resource.setrlimit(resource.RLIMIT_AS, (MemoryLimit, MemoryLimit))


def execute_python_code():
    try:
        process = subprocess.Popen(f"docker exec {CONTAINER_NAME} sh -c 'timeout 1s python3 src/code.py < src/input.txt'",stdout=subprocess.PIPE, stderr=subprocess.PIPE,preexec_fn=set_time_limit(TimeoutLimit),shell=True)
            
        # # wait for the command to finish and get the stdout and stderr
        stdout, stderr = process.communicate()
        print("-------------------------------------------------------------------------------")

        ListOfReturn =stderr.decode().strip().split()
        print("H:",ListOfReturn, "returncode",process.returncode)
        # check for any errors in stderr
        if process.returncode != 0:
            process.kill()
            if process.returncode==137:
                CopyReturnCode(stderr, ErrorCodes["MLE"])
                #return MLE
            elif any(error in ListOfReturn for error in ceErrors):
                CopyReturnCode(stderr,ErrorCodes["CE"])
                print("CE")
                # return "CE"
            elif any(error in ListOfReturn for error in reErrors):
                CopyReturnCode(stderr,ErrorCodes["RE"])
                print("RE")
                # return "RE"
            elif "MemoryError" in ListOfReturn:
                CopyReturnCode(stderr,ErrorCodes["MLE"])
                print("MLE")
                # return "MLE"
            else:
                CopyReturnCode(stderr,ErrorCodes["TLE"])
                print("TLE")
                # return "WA"
        else:
            if (process.returncode == 0):
                CopyOpFile(stdout,ErrorCodes["AC"])
                print("AC")
                # return "AC"
            else:
                CopyReturnCode(stderr,ErrorCodes["WA"])
                print("WA")
                # return "WA"    
    except TimeoutError:
        # handle timeout error
        process.kill()
        stdout, stderr = process.communicate()
        CopyOpFile(stdout,stderr)

        # stderr = process.stderr.read()
        ListOfReturn =stderr.decode().strip().split()
        # s[s.index("File")] = "ddddd"
        # print("index ",ListOfReturn)
        # print("inside 1timeout ",str(stderr.decode()).split())
        if ("MemoryError" in ListOfReturn):
            CopyReturnCode(stderr,ErrorCodes["MLE"])
            print("MLE")
            # return "MLE"
        else:
            CopyReturnCode(stderr,ErrorCodes["TLE"])
            print("TLE")
            # return "TLE"

def CopyReturnCode(stderr,rCode):
    err=open(f'{FilePath}/error.txt','w+')
    rcode=open(f'{FilePath}/returncode.txt','w+')
    print("errrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")
    # print(err,"  fdsf  ",rcode)
    err.write(stderr.decode().strip())
    rcode.write(str(rCode))

def CopyOpFile(stdout,rCode):
    out=open(f'{FilePath}/output.txt','w+')
    rcode=open(f'{FilePath}/returncode.txt','w+')

    out.write(stdout.decode().strip())
    rcode.write(str(rCode))
    # rCode.write(rCode)

# def RunByLang(lang):
#     if (lang == "python"):
#         process = subprocess.Popen(['python3', f'{PythonFile}'],stdin=ip_file_path,stdout=subprocess.PIPE, stderr=subprocess.PIPE,preexec_fn=set_memory_limit)
#         return process
#     elif (lang == "cpp"):
#         args = ['g++', '-o', f'{FilePath}/code', CppFile] # compile the file and generate an output executable
#         process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE,preexec_fn=set_memory_limit)
#         print("llllllllllllllllllllllllllllllllllll")
#         # print(process.returncode)
#         output, error = process.communicate() # get the output and error messages
#         # print(output,error)
#         if not error:
#             executable = f'{FilePath}/./code'
#             process = subprocess.Popen(executable, stdin=ip_file_path,stdout=subprocess.PIPE, stderr=subprocess.PIPE,preexec_fn=set_memory_limit,shell=False)
#             output, error = process.communicate()
#             print("llllllllllllllllllllllllllllllllllll")
#             # print(process.returncode)
#             return process
#         else:
#             return process
    
# test the function with a sample command


def execute_cpp_code():
    # args = ['docker','exec','g++', '-o', f'{FilePath}/code', CppFile] # compile the file and generate an output executable

    process = subprocess.Popen(f"docker exec {CONTAINER_NAME} sh -c 'timeout 1s g++ src/code.cpp'", stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
    output, error = process.communicate()
    # error = process.stderr
    print(process.returncode)
    print("executable file ",error)

    if process.returncode==124:
        CopyReturnCode(error,ErrorCodes["TLE"])
        print("Time Limit Exceeded")
    elif error:
        CopyReturnCode(error,ErrorCodes["CE"])
        print("Compile Error:")
        # print(error.decode('utf-8'))
    else:
        executable = f'{FilePath}/./code'
        try:
            process = subprocess.Popen(f"docker exec {CONTAINER_NAME} sh -c 'timeout 1s ./a.out < src/input.txt'", stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)

            out, err = process.communicate(timeout=1) # timeout after 5 seconds
            # print("try block err : ",err.decode().split())
            print("try block err : ")
        except subprocess.TimeoutExpired:
            process.kill()    # terminate the process if it exceeds the timeout
            CopyReturnCode(err,ErrorCodes["TLE"])
            print("Time Limit Exceeded")
            exit()
        except subprocess.CalledProcessError:
            CopyReturnCode(err,ErrorCodes["MLE"])
            print("inside 3rd except : ")

        if err:
            CopyReturnCode(err,ErrorCodes["RE"])
            print("Runtime Error1:")
            # print(err.decode('utf-8'))
        elif process.returncode != 0:
            CopyReturnCode(err,ErrorCodes["TLE"])
            print("Runtime Error2: TLE ")
            # print(out.decode('utf-8'))
        else:
            print("outtttttttttttt ",out)
            CopyOpFile(out,ErrorCodes["AC"])
            print("AC CPP")
            # print(out.decode('utf-8'))




def execute_c_code():
    #g++ src/main.c && /src/./a.out
    #docker exec container2 sh -c 'python3 src/code.py < src/input.txt'
    # args = ['docker','exec',f'{CONTAINER_NAME}','gcc', '-o', f'{FilePath}/ccode', CFile] # compile the file and generate an output executable

    process = subprocess.Popen(f"docker exec {CONTAINER_NAME} sh -c 'timeout 1s gcc src/code.c'", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate(timeout=1)
    # error = process.stderr
    print("executable file ",error)

    print("return code ->",process.returncode)
    if process.returncode==124:
        CopyReturnCode(error,ErrorCodes["TLE"])
        print("Time Limit Exceeded")
    elif error:
        CopyReturnCode(error,ErrorCodes["CE"])
        print("Compile Error:")
        # print(error.decode('utf-8'))
    else:
        # executable = f'{FilePath}/./ccode'
        err=b''
        try:
            process = subprocess.Popen(f"docker exec {CONTAINER_NAME} sh -c 'timeout 1s ./a.out < src/input.txt'", stdin=ip_file_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
            # print(process.returncode)

            out, err = process.communicate(timeout=1) # timeout after 5 seconds
            # print("try block err : ",err.decode().split())
            print("try block err : ")
        except subprocess.TimeoutExpired:
            process.kill()    # terminate the process if it exceeds the timeout
            CopyReturnCode(err,ErrorCodes["TLE"])
            print("Time Limit Exceeded")
            exit()
        except subprocess.CalledProcessError:
            CopyReturnCode(err,ErrorCodes["MLE"])
            print("inside 3rd except : ")

        if err:
            CopyReturnCode(err,ErrorCodes["RE"])
            print("Runtime Error1:")
            # print(err.decode('utf-8'))
        elif process.returncode != 0:
            CopyReturnCode(err,ErrorCodes["TLE"])
            print("Runtime Error2: TLE ")
            # print(out.decode('utf-8'))
        else:
            print("outtttttttttttt ",out)
            CopyOpFile(out,ErrorCodes["AC"])
            print("AC CPP")
            # print(out.decode('utf-8'))


# def cpp(time_limit,memory_limit):
#     a=subprocess.run('g++ code.cpp -o cpp.out',shell=True,stderr=er,text=True)
#     rc.write(str(a.returncode))
#     if(a.returncode==0):
#         a=subprocess.run('./cpp.out <input.txt>output.txt',shell=True,stderr=er,preexec_fn=set_limit_resource(False,time_limit,memory_limit),text=True)
#         rc.write(str(a.returncode))
#     rc.close()
#     er.close()
execute_python_code()