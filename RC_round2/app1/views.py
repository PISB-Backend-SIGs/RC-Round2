from curses import termname
from time import strftime
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from django.contrib.auth.models import User
import re
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# Create your views here.
from django.contrib.auth.decorators import login_required
from .utils import *
from .decorators import *
from .models import *
from .decorators import (check_time, only_superuser)
from .runnerUtils import runCode
import json
from .RCGetOp import *
@login_required(login_url='login')
def home(request):
    context={
        "user":request.user
    }
    user = User.objects.get(username=request.user)
    player = Player.objects.get(user=user)
    if request.method == "POST":
        if (player.p_is_started):
            return redirect("questions")
        checkbox = request.POST.get("checked")
        print(checkbox)
        if checkbox == "checked":
            player.p_start_time = timezone.now()
            player.p_is_started = True
            player.save()
            return redirect("questions")
        else:
            messages.error(request, "Checkbox not checked")

    return render(request,"app1/instructions.html",context)

def userLogin(request):
    print("in login")
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username)
        print(password)

        user = authenticate(request, username = username, password = password)
        
        if user is not None:
            try:
                player = Player.objects.get(user=user)
                if not(player.p_is_loged_in):
                    login(request, user)
                    player.p_is_loged_in = True
                    player.save()
                else:
                    messages.error(request, "The participant has already logged in!!")
                    return redirect("login")
            except:
                player=Player(user=user,p_is_loged_in=True)
                player.save()
                login(request, user)            
            return redirect("home")
        else:
            messages.error(request, "Login Failed due to invalid credentials!")
            return redirect("login")
    return render(request, 'app1/newlogin.html')

def userLogout(request):
    logout(request)
    return redirect("login")

def userRegister(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        rep_password = request.POST.get('rep_password')
        email = request.POST.get('email')

        if User.objects.filter(username = username).exists():
            messages.error(request, "User already exists!")
            return redirect("register")
        else:
            if password == rep_password and  len(password)>8: 
                if re.search('[A-Z]', password)!=None and re.search('[0-9]', password)!=None and re.search("^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$", password)!=None:
                    user_registration = User.objects.create_user(username = username, email = email, password = password)
                    user_registration.save()
                    player = Player(user=user_registration)
                    player.save()
                    messages.success(request, "User creation successful! Kindly proceed for login")
                    return redirect("login")
                else:
                    messages.error(request, "Enter valid credentials")
                    return redirect("register")
            else:
                messages.error(request, "User registration failed!")
                return redirect("register")
    return render(request, 'app1/register.html')

@check_time
@login_required(login_url='login')
def questions(request):
    user=User.objects.get(username=request.user)
    team = Team.objects.get(user=user)
    questions = Question.objects.all()
    check_accuracy()
    ques_list=check_solved(team)   #To show user which questions are solved
    end_time = Contest_time.objects.get(id=1)
    var = str(end_time.end_time.astimezone())
    return render(request,"app1/quesHub.html",{"questions":questions,"player":user,"ques_list":ques_list, "end_time":var,"team_score":team.team_score})

@login_required(login_url='login')
def question(request,id):
    context={}
    question = Question.objects.get(q_id=id)
    print("question",question)
    user = User.objects.get(username=request.user)
    player = Player.objects.get(user=user)
    team = Team.objects.get(user__username=request.user)
    print("this is user : ",user,"with team id : ",team)
    # print("team ",team)
    context["question"]=question
    context["player"]=player
    context["team"]=team
    context["isSolved"]=False
    end_time = Contest_time.objects.get(id=1)
    var = str(end_time.end_time.astimezone())
    context["end_time"]=var


    try:
        submission = Submission.objects.filter(team=team,q_id=question,q_status="AC").last()
        # print("subtry",submission[0].s_code)
        print("last accepted submission ",submission)
        # print("subtry",submission[0].s_code)
        context["isSolved"]=True

        context["user_code"]=json.dumps(submission.s_code)

    except:
        try:
            submission = Submission.objects.filter(player=user,q_id=question).last()
            # print(submission)
            context["isSolved"]=True
            context["user_code"]=json.dumps(submission.s_code)
        except:
            context["isSolved"]=False
            context["user_code"]=json.dumps("#Write your code here..")
    try:
        if submission.s_language == "cpp":
            context["code_lang_cpp"]="cpp"
        if submission.s_language == "c":
            context["code_lang_c"]="c"
    except:
        pass
    print("user code  : ",context["user_code"])
    # return render(request,"app1/question.html",context)
    return render(request,"app1/rccoding.html",context)

@login_required(login_url='login')
def question_sub(request,id):
    print("inside question_sub ")
    context={}
    question = Question.objects.get(q_id=id)
    user = User.objects.get(username = request.user)
    team = Team.objects.get(user =user)
    if request.method=="POST":
        print("question_sub inside post")
        user_code = request.POST.get("user_code")
        language = request.POST.get("code_lang")
        btn_status = int(request.POST.get("btn_clicked"))
        
        # print("users code :",user_code,"languageddddddd 0",language,"stat : ",type(btn_status))

        if (btn_status==0):
            print("run clciked")
            user_test_ip = request.POST.get("testip")
            status = runCode(id,user_code,language,btn_status,user_test_ip)
            # print("from utils to show aop",status)
            print("from utils to show op")
            dict = {
                "status":1,
                "subStatus":status,
                "testip":user_test_ip,
                # "testop":status[0],
            }
            return JsonResponse(dict)

        submission = Submission(team=team,player=user,q_id=question,s_code=user_code,s_language=language)
        
        submissionFlag = False
        #it will store one submission of user with answer of all testcases
        status = runCode(id,user_code,language,btn_status,"No")
        if (status["ShortFormOfStatus"].count("AC")==len(status["ShortFormOfStatus"])):
            try:
                if(Submission.objects.filter(team=team,q_id=id,q_status="AC")):
                    submissionFlag = True
                    submission.q_status = "AC"
                    

            except:
                submissionFlag = True
                submission.q_status = "AC"
                marks_reduce = calc_score(Submission.objects.filter(team=team,q_id=id))  #It gives how many marks will be reducing
                team.team_score += (question.q_point - marks_reduce)    #It will store marks for that question in team 
                submission.s_pt = team.team_score
                question.q_point -=1
                question.save()
                

        else:
            submission.q_status = "WA"
        team.team_attempted +=1
        submission.save()
        team.save()
        dict = {
                "status":1,
                "subStatus":status,
                # "testip":user_test_ip,
                # "testop":status[0],
                "submissionFlag":submissionFlag,
            }
        # return redirect(f"/question/{id}")
        return JsonResponse(dict)
        
from django.views.decorators.csrf import csrf_exempt
@login_required(login_url='login')
@csrf_exempt
def getRCipOP(request):
    print("**************************")
    if (request.method=="POST"):
            print("run clciked")
            userTestInput = request.POST.get("user_code")
            qid = request.POST.get("id")
            userOp = getOp(qid,userTestInput)
            # print("from utils to show aop",status)
            print("from utils to show op",userOp)
            dict = {
                "status":1,
                "testop":userOp,
            }
            return JsonResponse(dict)
    else:
        dict={
            "status":0
        }
        return JsonResponse(dict)

# @login_required(login_url='login')
def leaderboard(request):
    context={
        "title":"Result"
    }
    # team1 =Team.objects.all().values()  #to check attributes
    # print(team1)
    team =Team.objects.all().order_by('-team_score','teamTime')
    # print(team)
    user=User.objects.all()
    # print(user.filter(team__id=3)[0].username)
    dict=get_leaderboard(team,user)   #to get list of dictionary containing places of users 
    # team2 =User.objects.filter()

    context["teams"]=dict
    return render(request,"app1/leaderb.html",context)


# from django.contrib.auth.decorators import user_passes_test
# @user_passes_test(lambda u: u.is_superuser)s
@only_superuser
@login_required(login_url='login')
def settingwale(request):
    context={}
    players = Player.objects.all()
    users = User.objects.all()
    context["players"]=players
    context["users"]=users
    return render(request,"app1/settingwale.html",context)


def test(request):
    # if (request.method == "POST"):
    #     return JsonResponse({"status":1})
    # else:
    #     return JsonResponse({"status":0})
    # make_dir("prasad")
    return render(request,"app1/codingPage.html")

@login_required(login_url='login')
def submissions(request):
    # user= User.objects.get(username='testuser1')
    user= User.objects.get(username=request.user)
    print("Ffdd",user)
    submissions = Submission.objects.filter(player=user)
    print(submissions)
    return render(request,"app1/SubPage.html",{'submissions':submissions })

@login_required(login_url='login')
def result(request):
    currteam = Team.objects.get(user=request.user)
    teamResult = Team.objects.all().order_by('team_score').reverse()
    context ={}
    context["currteam"] = currteam

    context["first"] = teamResult[0]
    context["first_name"] = str()
    for x in teamResult[0].user.all() :
        context["first_name"] += (x.username + " ")

    context["second"] = teamResult[1]
    context["second_name"] = str()
    for w in teamResult[1].user.all() :
        context["second_name"] += (w.username + " ")

    context["third"] = teamResult[2]
    context["third_name"] = str()
    for v in teamResult[2].user.all() :
        context["third_name"] += (v.username + " ")

    context["teamResult"] = teamResult[3:6]
    cn = dict()
    for i in range(len(teamResult)) :
        for j in teamResult[i].user.all() :
            print('t:',teamResult[i],j.username)
            cn[j.username] = teamResult[i]
        if currteam == teamResult[i] :
            context["currteam_rank"] = i+1
    context['cn'] = cn
    print(cn)
    return render(request,"app1/result.html",context)

@login_required(login_url='login')
def submission_detail(request):
    if request.method == 'POST':
        team_time = request.POST.get('s_time')
        print(team_time)
        t_time = team_time
        detail = Submission.objects.filter(s_time =team_time).first()
        print(detail)
    return JsonResponse({'hello' : 'hello'})