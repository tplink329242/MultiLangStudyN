#!/usr/bin/python

import os
import sys, getopt
import time
from progressbar import ProgressBar

from lib.System import System
from lib.Process_Data import Process_Data
from lib.Collect_RepoStats import Collect_RepoStats
from lib.Github_API import Github_API

from lib.Language_Stats import Language_Stats
from lib.Collect_LangStats import Collect_LangStats
from lib.Collect_DiscripStats import Collect_DiscripStats
from lib.Collect_ComboTopicStats import Collect_ComboTopicStats

from lib.Collect_Association import Collect_Association
from lib.Collect_CmmtLogs import Collect_Issues
from lib.Collect_CmmtLogs import Collect_CmmtLogs
from lib.Collect_Nbr import Collect_Nbr
from lib.Collect_NbrAPI import Collect_NbrAPI
from lib.Collect_NbrSingleLang import Collect_NbrSingleLang
from lib.LangApiSniffer import LangApiSniffer
from lib.CloneRepo import CloneRepo
from lib.Sample import Sample
from lib.Collect_SpearMan import Collect_SpearMan
from lib.Sumreadme import Sumreadme



def Daemonize(pid_file=None):
    pid = os.fork()
    if pid:
        sys.exit(0)
 
    #os.chdir('/')
    os.umask(0)
    os.setsid()

    _pid = os.fork()
    if _pid:
        sys.exit(0)
 
    sys.stdout.flush()
    sys.stderr.flush()
 
    with open('/dev/null') as read_null, open('/dev/null', 'w') as write_null:
        os.dup2(read_null.fileno(), sys.stdin.fileno())
        os.dup2(write_null.fileno(), sys.stdout.fileno())
        os.dup2(write_null.fileno(), sys.stderr.fileno())
 
    if pid_file:
        with open(pid_file, 'w+') as f:
            f.write(str(os.getpid()))
        atexit.register(os.remove, pid_file)


def TimeTag (Tag):
    localtime = time.asctime( time.localtime(time.time()) )
    print ("%s : %s" %(Tag, localtime))
 

# collect from github
def CollectRepo(year=0):
    TimeTag(">>>>>>>>>>>> [%d]Collect repositories fom github..." %year)
    # Retrieves repo data from Github by page
    origin_repo = Github_API()

    if (year == 0):
        origin_repo.collect_repositories()
    else:
        origin_repo.collect_repositories_by_year (year)
    
    return origin_repo.list_of_repositories

def UpdateRepo():
    TimeTag(">>>>>>>>>>>> [%d]Update repositories fom github...")
    # Retrieves repo data from Github by page
    Ga = Github_API()
    Ga.update_repolist()


# repo stats
def RepoStats(original_repo_list=None):
    num_language = 10
    TimeTag(">>>>>>>>>>>> Statistic on repositories...")
    if (original_repo_list == None):
        original_repo_list = Process_Data.load_data(file_path=System.getdir_collect(), file_name='Repository_List')

        #open language file
        languageFile = open("Top_50_languages.txt","r")

        list_language = []

        #load data
        for i in range(0, num_language):
            strLanguage = languageFile.readline()
            strLanguage = strLanguage.strip()
            list_language.append(strLanguage)

        #filter data here
        for org_repo in reversed(original_repo_list):
            org_repo['language_dictionary']

            language_keys = reversed(list(org_repo['language_dictionary'].keys()))
            for key in language_keys:
                num_language_count = 0

                for listValues in list_language:

                    if key == listValues:
                        break
                    else:
                        num_language_count = num_language_count + 1

                if num_language_count >= 50:
                    del((org_repo['language_dictionary'])[key])
            
            if len(org_repo['language_dictionary']) <2:
                original_repo_list.remove(org_repo)
                

    languageFile.close()


    repository_data = Collect_RepoStats()
    repository_data.process_data(original_repo_list)
    repository_data.save_data()

# language stats
def LangStats(repo_stats=None):
    TimeTag(">>>>>>>>>>>> Statistic on languages...")
    file_path=System.getdir_stat()
    if (repo_stats == None):
        repo_stats = Process_Data.load_data(file_path=file_path, file_name='Repository_Stats')
        repo_stats = Process_Data.dict_to_list(repo_stats)
        
    research_data = Collect_LangStats() 
    research_data.process_data(list_of_repos=repo_stats)
    research_data.save_data()

# discription stats
def DiscripStats(repo_stats=None):
    TimeTag(">>>>>>>>>>>> Statistic on discriptions...")
    file_path=System.getdir_stat()
    if (repo_stats == None):
        repo_stats = Process_Data.load_data(file_path=file_path, file_name='Repository_Stats')
        repo_stats = Process_Data.dict_to_list(repo_stats)
    
    research_data = Collect_DiscripStats()
    research_data.process_data(list_of_repos=repo_stats)
    research_data.save_data()    

# relation between language combination and topic stats
def RelComboTopics(descrip_stats=None):
    TimeTag(">>>>>>>>>>>> Statistic on combinations and topics...")
    file_path=System.getdir_stat()
    if (descrip_stats == None):
        descrip_stats = Process_Data.load_data(file_path=file_path, file_name='Description_Stats')
        descrip_stats = Process_Data.dict_to_list(descrip_stats)
        
    research_data = Collect_ComboTopicStats()
    research_data.process_data (list_of_repos=descrip_stats)
    research_data.save_data()

# Association
def Association(correlation_stat=None):
    TimeTag(">>>>>>>>>>>> Statistic on Association...")
    file_path=System.getdir_stat()
    if (correlation_stat == None):
        correlation_stat = Process_Data.load_data(file_path=file_path, file_name='Correlation_Data')
        correlation_stat = Process_Data.dict_to_list(correlation_stat)
        
    research_data = Collect_Association()
    research_data.process_data (list_of_repos=correlation_stat)
    research_data.save_data()

# Commits log analysis
def CommitLog(StartNo=0, EndNo=65535, repo_stats=None):
    TimeTag(">>>>>>>>>>>> Statistic on CommitLog...")
    file_path=System.getdir_stat()
    if (repo_stats == None):
        repo_stats = Process_Data.load_data(file_path=file_path, file_name='Repository_Stats')
        repo_stats = Process_Data.dict_to_list(repo_stats)
        
    research_data = Collect_CmmtLogs(StartNo, EndNo) 
    research_data.process_data(list_of_repos=repo_stats)
    research_data.save_data()

# Commits log NBR analysis
def CommitLogNbr(repo_no, repo_stats=None):
    TimeTag(">>>>>>>>>>>> Statistic on CommitLogNbr...")
    file_path=System.getdir_stat()
    if (repo_stats == None):
        repo_stats = Process_Data.load_data(file_path=file_path, file_name='Repository_Stats')
        repo_stats = Process_Data.dict_to_list(repo_stats)
        
    research_data = Collect_Nbr(repo_no) 
    research_data.process_data(list_of_repos=repo_stats)
    research_data.save_data()

    research_data = Collect_NbrAPI(repo_no) 
    research_data.process_data(list_of_repos=repo_stats)
    research_data.save_data()

    research_data = Collect_NbrSingleLang (repo_no)
    research_data.process_data(list_of_repos=repo_stats)
    research_data.save_data()


# Language API sniffer
def LangSniffer(StartNo, EndNo, FileName):
    TimeTag(">>>>>>>>>>>> Statistic LangAPISniffer...")
    file_path=System.getdir_stat()
    repo_stats = Process_Data.load_data(file_path=file_path, file_name='Repository_Stats')
    repo_stats = Process_Data.dict_to_list(repo_stats)
        
    research_data = LangApiSniffer(StartNo, EndNo, FileName) 
    research_data.process_data(list_of_repos=repo_stats)
    research_data.save_data()

def CloneRepos (startNo=0, endNo=65535):
    CR = CloneRepo ("Repository_List.csv", startNo, endNo)
    CR.Clone ()

def CollectSamples (Stat=False):
    if Stat == False:
        Cs = Sample (50, 500)
        Cs.ValidSmapling ()
    else:
        Cs = Sample (2, 100)
        Cs.StatSampling ()

def CollectIssues (StartNo=0, EndNo=65535, repo_stats=None):
    TimeTag(">>>>>>>>>>>> Statistic on Issues...")
    file_path=System.getdir_stat()
    if (repo_stats == None):
        repo_stats = Process_Data.load_data(file_path=file_path, file_name='Repository_Stats')
        repo_stats = Process_Data.dict_to_list(repo_stats)
        
    research_data = Collect_Issues(StartNo, EndNo) 
    research_data.process_data(list_of_repos=repo_stats)
    research_data.save_data()

def CollectSpearman ():
    Sm = Collect_SpearMan ()

def CollectSumReadMe (StartNo=0, EndNo=65535):
    TimeTag(">>>>>>>>>>>> Statistic on SumReadMe...")
    file_path=System.getdir_stat()
    repo_stats = Process_Data.load_data(file_path=file_path, file_name='Repository_Stats')
    repo_stats = Process_Data.dict_to_list(repo_stats)
        
    research_data = Sumreadme(StartNo, EndNo) 
    research_data.process_data(list_of_repos=repo_stats)
    research_data.save_data()


def StatAll ():
    original_repo_list = Process_Data.load_data(file_path=System.getdir_collect(), file_name='Repository_List')
    RepoStats(original_repo_list)

    repo_stats = Process_Data.load_data(file_path=System.getdir_stat (), file_name='Repository_Stats')
    repo_stats = Process_Data.dict_to_list(repo_stats)        
    LangStats(repo_stats)
    DiscripStats(repo_stats)
                
    RelComboTopics(None)
    Association(None)

def main(argv):
    step = ''
    by_year  = False
    year_val = 0
    repo_no  = 0
    IsDaemon = False
    FileName = ""
    StartNo  = 0
    EndNo    = 65535
   
    # get step
    try:
        opts, args = getopt.getopt(argv,"dhs:y:n:f:b:e:",["step=", "year=", "no="])
    except getopt.GetoptError:
        print ("./collect.py -s <step_name>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ("collect.py -s <step_name>");
            sys.exit()
        elif opt in ("-s", "--step"):
            step = arg;
        elif opt in ("-n", "--no"):
            repo_no = int(arg);
        elif opt in ("-y", "--year"):
            by_year = True;
            year_val = int(arg)
            print ("by_year = %d, year_val = %d" %(by_year, year_val))
        elif opt in ("-d", "--daemon"):
            IsDaemon = True;
        elif opt in ("-f", "--filename"):
            FileName = arg;
        elif opt in ("-b", "--beginno"):
            StartNo = int(arg);
        elif opt in ("-e", "--endno"):
            EndNo = int(arg);

    if IsDaemon:
        Daemonize ()

    print(step)
    
    if (step == "all"):
        if (by_year == True):
            for year in range (System.START_YEAR, System.END_YEAR+1, 1):
                if (year_val != 0 and year_val != year):
                    continue
                print ("\nYear-%d" %year, end="")
                System.setdir (str(year), str(year))
                StatAll()
        else:
            StatAll ()
    elif (step == "update"):
        UpdateRepo ()
    elif (step == "collect"):
        if (by_year == True):
            for year in range (System.START_YEAR, System.END_YEAR+1, 1):
                if (year_val != 0 and year_val != year):
                    continue
                print ("\nYear-%d" %year, end="")
                System.setdir (str(year), str(year))
                CollectRepo(year)
        else:
            CollectRepo()
                
    elif (step == "repostats"):
        if (by_year == True):
            for year in range (System.START_YEAR, System.END_YEAR+1, 1):
                if (year_val != 0 and year_val != year):
                    continue
                print ("\nYear-%d" %year, end="")
                System.setdir (str(year), str(year))
                RepoStats(None)
        else:
            RepoStats(None)
    elif (step == "langstats"):
        if (by_year == True):
            for year in range (System.START_YEAR, System.END_YEAR+1, 1):
                if (year_val != 0 and year_val != year):
                    continue
                print ("\nYear-%d" %year, end="")
                System.setdir (str(year), str(year))
                LangStats(None)
        else:
            LangStats(None)
    elif (step == "discripstats"):
        if (by_year == True):
            for year in range (System.START_YEAR, System.END_YEAR+1, 1):
                if (year_val != 0 and year_val != year):
                    continue
                print ("\nYear-%d" %year, end="")
                System.setdir (str(year), str(year))
                DiscripStats(None)
        else:
            DiscripStats(None)
    elif (step == "topics"):
        if (by_year == True):
            for year in range (System.START_YEAR, System.END_YEAR+1, 1):
                if (year_val != 0 and year_val != year):
                    continue
                print ("\nYear-%d" %year, end="")
                System.setdir (str(year), str(year))
                RelComboTopics(None)
        else:
            RelComboTopics(None)
    elif (step == "asso"):
        if (by_year == True):
            for year in range (System.START_YEAR, System.END_YEAR+1, 1):
                if (year_val != 0 and year_val != year):
                    continue
                print ("\nYear-%d" %year, end="")
                System.setdir (str(year), str(year))
                Association(None)
        else:
            Association(None)
    elif (step == "cmmts"):
        CommitLog (StartNo, EndNo)
    elif (step == "issue"):
        CollectIssues (StartNo, EndNo)
    elif (step == "nbr"):
        CommitLogNbr (repo_no)
    elif (step == "apisniffer"):
        LangSniffer (StartNo, EndNo, FileName)
    elif (step == "clone"):
        CloneRepos (StartNo, EndNo)
    elif (step == "sample"):
        CollectSamples ()
    elif (step == "statsample"):
        CollectSamples (True)
    elif (step == "spearman"):
        CollectSpearman ()
    elif (step == "readme"):
        CollectSumReadMe ()
    else:
        print ("collect.py -s <all/collect/repostats/langstats/discripstats/topics/asso/cmmts/nbr/apisniffer/clone>") 

    TimeTag (">>>>>>>>>>>> End")

if __name__ == "__main__":
    main(sys.argv[1:])
