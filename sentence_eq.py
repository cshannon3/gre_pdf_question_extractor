import json
import enum

class SentEqQuestionModel:
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
    


f = open("Educational Testing Service - Official GRE Verbal Reasoning Practice Questions-McGraw-Hill (2014)senteq.txt", 'rt', encoding="utf-8")

pageStart = 89
qstart = 0
# start and end of set 1, then start and end of set 2
questionnum = 1
currentpage = 89
questions = []
 # need to change these to enums and switch funct
class CurrentSection(enum.Enum): 
    answers = 1
    question = 3
    explanation = 5
    start = 6


currentSection = CurrentSection.start
ansNum = 0
qchoiceNum = 0
blanks = 1

questions = []

answerchoices = ["A", "B", "C", "D", "E", "F"]

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
    elif str(questionnum) in line.split(" ")[0]:
        q = SentEqQuestionModel(questionnum, currentpage, difficultyLevel[currentDifficulty])
        q.questionText += line.strip(str(questionnum)+". ")
        questions.append(q)
        qchoiceNum+=1
        currentSection = CurrentSection.question
   
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
        questions[-1].explanationText+=line
    

    

print(len(questions))
data = {}
data["questions"]=[]


for q in questions:
   data["questions"].append(q.getJson())


with open('sent_eq_data.json', 'w') as outfile:  
    json.dump(data, outfile)