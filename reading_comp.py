import json
import enum

# PRACTICE SET 1: Easy

#  based on this passage.
# /*
# passage
#  need to remove line nums 5,10,15
# */
# /*
# Description
# */

# question
# Explanation
# question
# Explanation

#  based on this passage
#  ?? page num

# PRACTICE SET 2: Medium

class ReadingCompPassageModel:
    def __init__(self, questionNums = [], pagenum = -1, difficulty=""):
        self.lines = [],
        self.difficulty = difficulty
        self.questionNumbers = [],
        self.description="",
        self.pagenum = pagenum
    
    def getJson(self):
        data = {}
        data["lines"] = self.lines
        data["difficulty"] = self.difficulty
        data["questionNumbers"] = self.questionNumbers
        data["description"] = self.description
        data["page_num"] = self.pagenum
        return data


class ReadingCompQuestionModel:
    def __init__(self, questionNumber = -1, pagenum = -1, difficulty= ""):
        self.questionText = ""
        self.difficulty = difficulty
        self.questionNumber = questionNumber
        self.answerOptions  = []
        self.correctAnswer = -1
        self.explanationText = ""
        self.pagenum = pagenum
   
    
    def getJson(self):
        data = {}
        data["questionNumber"] = self.questionNumber
        data["questionText"] = self.questionText
        data["difficulty"] = self.difficulty
        data["answerOptions"] = self.answerOptions
        data["correctAnswer"] = self.correctAnswer
        data["explanationText"] = self.explanationText    
        data["page_num"] = self.pagenum
        return data
        #print(data)

    
    def addAnswer(self, ans, optionnum = 5):
        ans = ans.strip()
        ans = ans.strip("\n")

        if len(ans) !=0:
            if optionnum > len(self.answerOptions)-1:
                self.answerOptions.append(ans)
            else:
                self.answerOptions[optionnum] += " " +ans
    


f = open("Educational Testing Service - Official GRE Verbal Reasoning Practice Questions-McGraw-Hill (2014)-pages-48-69.txt", 'rt', encoding="utf-8")

pageStart = 36
qstart = 0
# start and end of set 1, then start and end of set 2
questionnum = 1
currentpage = 36
questions = []
 # need to change these to enums and switch funct
class CurrentSection(enum.Enum): 
    answers = 1
    passage = 2
    question = 3
    description = 4
    explanation = 5
    start = 6


currentSection = CurrentSection.start
ansNum = 0
qchoiceNum = 0

passages = []
questions = []

answerchoices = ["A", "B", "C", "D", "E"]
difficultyLevel = ["Easy", "Medium", "Hard", "Prob", "Prob"]
currentDifficulty = -1
# S

for line in f:
    line = line.strip()
    if line == str(currentpage):
        currentpage+=1
        pass
    elif "PRACTICE SET" in line:
        currentDifficulty+=1
        questionnum=1
        pass
    elif "based on this passage" in line:

        passageQs = []
        if "Questions" in line:
            l = line.split(" ")
            for i in range(int(l[1]), int(l[3])):
                passageQs.append(i)
        elif "Question" in line:
            passageQs.append(int(line.split(" ")[1]))
        p = ReadingCompPassageModel(passageQs, currentpage, difficultyLevel[currentDifficulty])
        p.lines = []
        passages.append(p)
        currentSection = CurrentSection.passage
        pass
    elif currentSection == CurrentSection.passage:
        if line == "Description":
            currentSection = CurrentSection.description
            passages[-1].description = ""
            pass
        elif str(questionnum) in line.split(" ")[0]:
            q = ReadingCompQuestionModel(questionnum, currentpage, difficultyLevel[currentDifficulty])
            q.questionText += line.strip(str(questionnum)+". ")
            questions.append(q)
            qchoiceNum+=1
            currentSection = CurrentSection.question
        else:
            passages[-1].lines.append(line)
            pass
        pass
    
    elif currentSection == CurrentSection.description:
        if str(questionnum) in line.split(" ")[0]:
            q = ReadingCompQuestionModel(questionnum, currentpage, difficultyLevel[currentDifficulty])
            q.questionText += line.strip(str(questionnum)+". ")
            questions.append(q)
            qchoiceNum+=1
            currentSection = CurrentSection.question
        else:
            passages[-1].description+=line
        pass
    elif currentSection == CurrentSection.question:
        if "A " in line:
            questionnum+=1
            currentSection = CurrentSection.answers
            questions[-1].addAnswer(line.strip("A "), qchoiceNum)
        else:
            questions[-1].questionText+=line
        pass
    elif currentSection == CurrentSection.answers:
        if (qchoiceNum+1)<len(answerchoices) and (answerchoices[qchoiceNum+1]+" ") in line:
            qchoiceNum+=1
            questions[-1].addAnswer(line.strip(answerchoices[qchoiceNum]+" "), qchoiceNum)
        elif "Explanation" in line:
            currentSection = CurrentSection.explanation
            qchoiceNum=0
        else:
            questions[-1].addAnswer(line, qchoiceNum)
        pass
    elif currentSection == CurrentSection.explanation:
        if str(questionnum) in line.split(" ")[0]:
            q = ReadingCompQuestionModel(questionnum, currentpage, difficultyLevel[currentDifficulty])
            q.questionText += line.strip(str(questionnum)+". ")
            questions.append(q)
            qchoiceNum+=1
            currentSection = CurrentSection.question
        else:
            questions[-1].explanationText+=line

        pass
    

    

print(len(questions))
data = {}
data["questions"]=[]
data["passages"] = []

for q in questions:
   data["questions"].append(q.getJson())
for p in passages:
   data["passages"].append(p.getJson())
 

with open('rdata.json', 'w') as outfile:  
    json.dump(data, outfile)