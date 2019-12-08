import json
import enum
## first download pdf from libgen
## second split pdf with https://smallpdf.com/split-pdf, saving only explanations for each question type
## Third use k2pdfopt application located in downloards to convert 2column pdfs to 1
##  Forth use pdftotext.exe -layout examplepdf.pdf to get a text file of the questions
## Fifth clean the data, look for repeating parts, page headers etc
## finally can use this program to extract question info into models
## next use pymongo to load questions to mongodb

## Then the hard part of creating value with the question bank

## TODO figure out how to create and link pictures of each question to models so
## can use those for actual ui


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



class TextCompQuestionModel:
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
    


f = open("data/Educational Testing Service - Official GRE Verbal Reasoning Practice Questions-McGraw-Hill (2014)text_comp.txt", 'rt', encoding="utf-8")

pageStart = 36
qstart = 0
# start and end of set 1, then start and end of set 2
questionnum = 1
currentpage = 36
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

answerchoices = ["A", "B", "C", "D", "E"]
answerCBlanks = [["A", "B", "C"], ["D", "E", "F"], ["G", "H", "I"]]
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
        q = TextCompQuestionModel(questionnum, currentpage, difficultyLevel[currentDifficulty])
        q.questionText += line.strip(str(questionnum)+". ")
        questions.append(q)
        qchoiceNum+=1
        currentSection = CurrentSection.question
   
    elif currentSection == CurrentSection.question:
        if "Blank" in line:
            blanks = line.count("Blank")

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


with open('text_comp_data.json', 'w') as outfile:  
    json.dump(data, outfile)