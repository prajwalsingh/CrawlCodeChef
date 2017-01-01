import os
import requests
from bs4 import BeautifulSoup
import  re


class CodeChefCrawler:
    codechefurl = "https://www.codechef.com/users/"
    codechefcon = "https://www.codechef.com/contests"
    codecheflistH = ["ProfilePhoto", "Name", "Country", "Username", "Institution\Organization"]
    codecheflistCH = ["Contest Code", "Contest Name", "Begin Date & Time", "End Date & Time"]
    codecheflist = []
    codechefconC = []
    codechefconF = []

    def crawlCodechefProfile(self, uname):
        try:
            self.codechefurl += uname
            print("")
            source_code = requests.get(self.codechefurl)
            plain_text = source_code.text
            soup = BeautifulSoup(plain_text, "html.parser")
        except:
            print("!Sorry , Unable to fetch information !!!")
            return
        # ---------------- Extract User Profile Image Url --------------------------
        try:
            uimg = soup.find_all("div", "user-thumb-pic")
            userImgData = str(uimg[0]).split("=")
            imgURL = userImgData[3].split(" ")
            finalImgUrl = re.search(r'\"(.*)\"', imgURL[0]).group(1)
            finalImgUrl = "https://www.codechef.com" + finalImgUrl
            self.codecheflist.append(finalImgUrl)
        except:
            print("@Sorry, Unable to fetch codechef profile picture!!")
        # ----------------- Extract User Name --------------------------------------
        try:
            uname = soup.find_all("div", "user-name-box")
            userNameData = str(uname[0]).split("=")
            flag = 0
            finalUserName = ""
            for i in userNameData[1]:
                if i == '<': flag = 0
                if i == '>' or flag == 1:
                    flag = 1
                    finalUserName += i
            finalUserName = re.search(r'>(.*)>', finalUserName).group(1)
            self.codecheflist.append(finalUserName)
        except:
            print("@Sorry, Unable to fetch Codechef User name!!")
        # ------------------ Extract Country Name ------------------------------------
        try:
            ucount = soup.find_all("span", "user-country-name")
            userCountData = str(ucount[0]).split("=")
            flag = 0
            finalContName = ""
            for i in userCountData[2]:
                if i == '<': flag = 0
                if i == '>' or flag == 1:
                    flag = 1
                    finalContName += i
            finalContName = re.search(r'>(.*)>', finalContName).group(1)
            self.codecheflist.append(finalContName)
        except:
            print("@Sorry, Unable to fetch user country on Codechef !!")
        # -------------------- Extract Username and Institution or Organization Name ----------------------------------
        try:
            tables = soup.findAll('table')[2]
            for row in tables.findAll('tr'):
                col = row.findAll('td')
                if col[0].string == 'Username:':
                    self.codecheflist.append(col[1].string)
                elif col[0].string == 'Institution:' or col[0].string == 'Organisation:':
                    self.codecheflist.append(col[1].string)
        except:
            print("@Sorry, Unable to fetch Codechef User Institution!!")
        # --------------------- Extract Problem Information ----------------------------------------------------------
        try:
            tables = soup.find('table', {'id': 'problem_stats'})
            problemList = []
            for row in tables.findAll('tr'):
                col = row.findAll('td')
                for ccol in col:
                    val = ""
                    for item in ccol:
                        problemList.append(item)
                    l = len(problemList) // 2
            for i in range(l):
                self.codecheflistH.append(problemList[i])
                self.codecheflist.append(problemList[i + l])
        except:
            print("@Sorry, Unable to fetch Codechef User Problem Information  !!")
        # ---------------------- Extract rating Information -----------------------------------------------------------
        try:
            tables = soup.find('table', {'class': 'rating-table'})
            store = ""
            # for row in tables.findAll('tr'):
            row = tables.findAll('tr')[1]
            longCon = row.findAll('td')[0].string
            longConrank_G = row.findAll('hx')[0].string
            longConrank_L = row.findAll('hx')[1].string
            row = tables.findAll('tr')[2]
            shortCon = row.findAll('td')[0].string
            shortConrank_G = row.findAll('hx')[0].string
            shortConrank_L = row.findAll('hx')[1].string
            row = tables.findAll('tr')[3]
            lunchCon = row.findAll('td')[0].string
            lunchConrank_G = row.findAll('hx')[0].string
            lunchConrank_L = row.findAll('hx')[1].string
            self.codecheflistH.append(longCon + " Global Rank")
            self.codecheflistH.append(longCon + " Country Rank")
            self.codecheflistH.append(shortCon + " Global Rank")
            self.codecheflistH.append(shortCon + " Country Rank")
            self.codecheflistH.append(lunchCon + " Global Rank")
            self.codecheflistH.append(lunchCon + " Country Rank")
            self.codecheflist.append(longConrank_G)
            self.codecheflist.append(longConrank_L)
            self.codecheflist.append(shortConrank_G)
            self.codecheflist.append(shortConrank_L)
            self.codecheflist.append(lunchConrank_G)
            self.codecheflist.append(lunchConrank_L)
        except:
            print("@Sorry, Unable to fetch Codechef User ratings!!")

    def crawlCodechefContest(self):
        webdata = requests.get(self.codechefcon).text
        soup = BeautifulSoup(webdata, 'html.parser')
        tables = soup.findAll('table', {'class': 'dataTable'})
        # --------------------------------- Extract Current Contest Information -----------------------------------
        try:
            for row in tables[0].findAll('tr')[1:]:
                col = row.findAll('td')
                temp = []
                copy = []
                ind = 0
                samp = []
                for ccol in col:
                    temp.append(ccol.string)
                    samp.append(temp[:][ind])
                    ind += 1
                self.codechefconC.append(samp)
        except:
            print("@Sorry, Unable to fetch Current Contest Details!!")
        # --------------------------------- Extract Future Contest Information -----------------------------------
        try:
            for row in tables[1].findAll('tr')[1:]:
                col = row.findAll('td')
                temp = []
                copy = []
                ind = 0
                samp = []
                for ccol in col:
                    temp.append(ccol.string)
                    samp.append(temp[:][ind])
                    ind += 1
                self.codechefconF.append(samp)
        except:
            print("@Sorry, Unable to fetch Current Contest Details!!")

    def showCodeChefProfile(self):
        cheflist = zip(self.codecheflistH, self.codecheflist)
        ind = 0
        for k, v in cheflist:
            print(k, ":", v)
            # ind += 1
            # if ind == 5: break
        # try:
        #     print("")
        #     print('%-30s %-30s %-30s %-30s %-30s %-30s %-30s %-30s %-30s' %
        #           (self.codecheflistH[5], self.codecheflistH[6], self.codecheflistH[7], self.codecheflistH[8],
        #            self.codecheflistH[9], self.codecheflistH[10], self.codecheflistH[11], self.codecheflistH[12],
        #            self.codecheflistH[13]
        #            )
        #           )
        #     print('%-30s %-30s %-30s %-30s %-30s %-30s %-30s %-30s %-30s' %
        #           (self.codecheflist[5], self.codecheflist[6], self.codecheflist[7], self.codecheflist[8],
        #            self.codecheflist[9], self.codecheflist[10], self.codecheflist[11], self.codecheflist[12],
        #            self.codecheflist[13]
        #            )
        #           )
        #     print("")
        #     print('%-30s %-30s %-30s %-30s %-30s %-30s' %
        #           (self.codecheflistH[14], self.codecheflistH[15], self.codecheflistH[16], self.codecheflistH[17],
        #            self.codecheflistH[18], self.codecheflistH[19]
        #            )
        #           )
        #     print('%-30s %-30s %-30s %-30s %-30s %-30s' %
        #           (self.codecheflist[14], self.codecheflist[15], self.codecheflist[16], self.codecheflist[17],
        #            self.codecheflist[18], self.codecheflist[19]
        #            )
        #           )
        # except:
        #     print("@Sorry, Unable to Format Display Details!!")

    def showCodechefContest(self):
        try:
            print("\nCurrent Contest\n------ -------")
            print("Contest Code" + '%30s' % "Contest Name" + '%30s' % "Start Date/Time" + '%30s' % "End Date/Time")
            for data in self.codechefconC:
                print(data[0] + '%40s' % data[1] + '%30s' % data[2] + '%30s' % data[3])
            print("\nFuture Contest\n------ -------")
            print("Contest Code" + '%30s' % "Contest Name" + '%30s' % "Start Date/Time" + '%30s' % "End Date/Time")
            for data in self.codechefconF:
                print(data[0] + '%40s' % data[1] + '%30s' % data[2] + '%30s' % data[3])
        except:
            print("@Sorry, Unable to Format Display Details!!")


class ChefSolve:
    solveList = []
    error = 1

    def checkSolve(self, uname):
        print("Please Wait Fetching Information Take Less Than A Minute.....")
        url = requests.get("https://www.codechef.com/users/" + uname).text
        soup = BeautifulSoup(url, 'html.parser')
        span = soup.findAll('span')
        ind = 0
        try:
            userBox = soup.find('div', {'class': 'user-name-box'})
            name = userBox.string
            self.error = 0
            for td in span:
                ind += 1
                if ind == 6:
                    self.solveList.append(td.text.split(","))
                    break
        except:
            self.error = -1

    def getList(self):
        return self.solveList[0]

    def getError(self):
        return self.error


class ChefQuestion:
    schoolListQName = []
    schoolListQCode = []
    easyListQName = []
    easyListQCode = []
    mediumListQName = []
    mediumListQCode = []
    hardListQName = []
    hardListQCode = []
    challengeListQName = []
    challengeListQCode = []
    exListQName = []
    exListQCode = []
    uSolve = []

    def chefQuestion(self, place, opt):
        print("Loading Please Wait...\n\n")
        try:
            url = requests.get('https://www.codechef.com/problems/' + place).text
            soup = BeautifulSoup(url, 'html.parser')
            tables = soup.find('table', class_="dataTable")
            rows = tables.findAll('tr')
            for row in rows:
                flag = 0
                col = row.findAll('td')
                for ccol in col:
                    flag += 1
                    if flag == 1:
                        if opt == 1:
                            self.schoolListQName.append(ccol.text.strip())
                        elif opt == 2:
                            self.easyListQName.append(ccol.text.strip())
                        elif opt == 3:
                            self.mediumListQName.append(ccol.text.strip())
                        elif opt == 4:
                            self.hardListQName.append(ccol.text.strip())
                        elif opt == 5:
                            self.challengeListQName.append(ccol.text.strip())
                        elif opt == 6:
                            self.exListQName.append(ccol.text.strip())
                    elif flag == 2:
                        if opt == 1:
                            self.schoolListQCode.append(ccol.text.strip())
                        elif opt == 2:
                            self.easyListQCode.append(ccol.text.strip())
                        elif opt == 3:
                            self.mediumListQCode.append(ccol.text.strip())
                        elif opt == 4:
                            self.hardListQCode.append(ccol.text.strip())
                        elif opt == 5:
                            self.challengeListQCode.append(ccol.text.strip())
                        elif opt == 6:
                            self.exListQCode.append(ccol.text.strip())
                    if flag == 2:
                        break
            return 0

        except:
            input("@Unable to fetch questions sorry for it....Press ENTER key to go back...")
            return -1

    def showChefQuestion(self, listQName, listQCode):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\t\t\tQuestion Table\n\t\t\t-------- -----\n")
            ind = 0
            print("%-3s\t\t%-10s\t\t%-15s\t\t%-30s" % ("SNo", "Solved", "Question Code", "Question Name"))
            print("-" * 90)
            for k in listQCode:
                ind += 1
                if ind>=800:
                    print("There are more than 800 Question in this section Cmd is not able to print all...")
                    break
                if ind in self.uSolve:
                    print("%3d.\t%-7s\t%-15s\t%-40s" % (ind, "#Yes#", k, listQName[ind - 1]))
                else:
                    print("%3d.\t%-7s\t%-15s\t%-40s" % (ind, "No", k, listQName[ind - 1]))
                print("-" * 90)
            try:
                opt = int(input("0: Go Back\t\t-1: Exit\t\tS.No: Go To Question\nenter option>> "))
            except:
                print("Invalid Input")
                continue
            if opt == 0:
                return 0
            elif opt == -1:
                exit()
            elif 1 <= opt <= ind:
                self.openQuestion(listQCode[opt - 1])

    @staticmethod
    def openQuestion(code):
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Loading Question Please Wait....\n")
            url = "https://www.codechef.com/problems/" + code
            box = requests.get(url).text
            soup = BeautifulSoup(box, 'html.parser')
            tables = soup.findAll('div', {'class': 'content'})
            questionList = tables[1]
            for q in questionList:
                try:
                    print(q.text.strip())
                    print("")
                except:
                    pass
            input("Press ENTER key to exit....")
        except:
            print("@Unable To Fetch Question Please Try again....")

    def chefSolveList(self, solveList, qList):
        ind = 1
        freshList = []
        for v in solveList:
            freshList.append(v.strip())
        self.uSolve.clear()
        for v in qList:
            if v in freshList:
                self.uSolve.append(ind)
            ind += 1


uname = input("\t\t\tCrawlChefCode\t\t\t - Prajwal Singh (prajwal_15)\n\t\t\t-------------\n\nEnter codechef user name : ")
chefObj = ChefSolve()
chefObj.checkSolve(uname)
flag = chefObj.getError()
if flag == -1:
    print("@Invalid Username!!!")

else:
    fresh = 0
    qtypeL = [0, 0, 0, 0, 0, 0]
    getList = chefObj.getList()
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n\t\t\tCodechef Command Version\t\t\t - Prajwal Singh (prajwal_15)\n\t\t\t-------- ------- -------")
        if fresh == 0:
            chefcrawl = CodeChefCrawler()
            chefcrawl.crawlCodechefContest()
            chefcrawl.crawlCodechefProfile(uname)
        fresh = 1
        chefcrawl.showCodechefContest()
        print("\n")
        chefcrawl.showCodeChefProfile()
        print("\n\n")
        qType = ""
        try:
            opt = int(input("\t\t\tSearch Problems\n\t\t\t------ --------\n1.Beginner Problems\n2.Easy Problems\n3.Medium Problems\n4.Hard Problems\n5.Challenge Problems\n6.Peer Problems\n7.Refresh All Information (fetch update)\n-1.To Exit\n\nenter option>> "))
        except:
            print("Inavlid Input!!!")
            continue
        if opt == -1:
            exit()
        elif opt == 1:
            qType = "school"
        elif opt == 2:
            qType = "easy"
        elif opt == 3:
            qType = "medium"
        elif opt == 4:
            qType = "hard"
        elif opt == 5:
            qType = "challenge"
        elif opt == 6:
            qType = "extcontest"
        elif opt == 7:
            qtypeL[:] = 0
            fresh = 0
        chefObj = ChefQuestion()
        if qtypeL[opt - 1] == 0:
            flag = chefObj.chefQuestion(qType, opt)
        if flag == 0:
           qtypeL[opt - 1] = 1
        if opt == 1:
            chefObj.chefSolveList(getList, chefObj.schoolListQCode)
            chefObj.showChefQuestion(chefObj.schoolListQName, chefObj.schoolListQCode)
        elif opt == 2:
            chefObj.chefSolveList(getList, chefObj.easyListQCode)
            chefObj.showChefQuestion(chefObj.easyListQName, chefObj.easyListQCode)
        elif opt == 3:
            chefObj.chefSolveList(getList, chefObj.mediumListQCode)
            chefObj.showChefQuestion(chefObj.mediumListQName, chefObj.mediumListQCode)
        elif opt == 4:
            chefObj.chefSolveList(getList, chefObj.hardListQCode)
            chefObj.showChefQuestion(chefObj.hardListQName, chefObj.hardListQCode)
        elif opt == 5:
            chefObj.chefSolveList(getList, chefObj.challengeListQCode)
            chefObj.showChefQuestion(chefObj.challengeListQName, chefObj.challengeListQCode)
        elif opt == 6:
            chefObj.chefSolveList(getList, chefObj.exListQCode)
            chefObj.showChefQuestion(chefObj.exListQName, chefObj.exListQCode)
