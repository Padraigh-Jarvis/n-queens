# -*- coding: utf-8 -*-
"""
Created on Sat Nov 25 22:04:33 2017

@author: Padraigh Jarvis
"""
import math
import timeit
import numpy as np

def assignment3(n):
    #Creates a n size array that represents our problem domain
    #Each position in the array represents a columns and the number represents a row
    
    start = timeit.default_timer()
    randomRestartHillClimber(n)
    stop=timeit.default_timer()
    print("Hill climber time taken:",stop-start , "seconds taken\n")
    
    start = timeit.default_timer()
    randomRestartSimulatedAnnealing(n)
    stop=timeit.default_timer()
    print("Simulated Annealing time taken:",stop-start , "seconds taken")
 
 
def randomBoard(n):
    board=[]
    for _ in  range(n): # create n random numbers beween 0 and n-1    
        board.append(np.random.randint(0,n-1))
    return board

def randomRestartSimulatedAnnealing(n):
    currentBestBoard=[]
    currentBestThreat=n
    totalAnnealingMoves=0
    for _ in range(500):
        #Create a high temperature. The higher the temp the more likly it is to  
        #explore less good neighbours
        temperature = 500
        coolingRate=0.9
        #Create a random board and get the number of threats on it
        currentBoard=randomBoard(n)
        #when temperature goes below 1 it reaches a freezing point so we will stop
        while temperature>1:
            #Get neigbours for the current state
            neighbours=generateNeighbourState(currentBoard)
            
            for neighbour in neighbours:
                #If the neighbour has less threats then take it as the new current board
                if numOfThreatenedQueens(neighbour)<numOfThreatenedQueens(currentBoard):
                    currentBoard=list(neighbour)
                    totalAnnealingMoves=totalAnnealingMoves+1
                    
                #Else we need to lookinto taking a worse option
                else:
                    #Generate a random number between 0 and 1  
                    randomNum=np.random.random()
                    #Generate the probability of moving to a worse state
                    #The higher the temperature and the lower the diffrence 
                    #beween the neighbour threat and the current threat the 
                    #more likly we are to take the move 
                    probabilityOfMove=math.exp(-(numOfThreatenedQueens(neighbour)-numOfThreatenedQueens(currentBoard))/temperature)

                    #Compare the randomNum to the probablity to move, if random 
                    #num is lower then we take the move
        
                    if randomNum<probabilityOfMove:
                        currentBoard=list(neighbour)
                        totalAnnealingMoves=totalAnnealingMoves+1
                if numOfThreatenedQueens(currentBoard)==0:
                    break
            #Reduce the current temperature by the cooling rate variable so we 
            #can eventually escape and make it less likly to take a bad move
                
                
            temperature = temperature*coolingRate        
 
        #Check if the best board of the loop is better then the current best
        if numOfThreatenedQueens(currentBoard)<currentBestThreat:
            currentBestBoard=list(currentBoard)
            currentBestThreat=numOfThreatenedQueens(currentBoard)

        if currentBestThreat==0:#If the current threat is 0 when we have found a solution!
            break
        
    print("Random Restart Simulated Annealing \nBest solution found:",currentBestBoard,
          "with",currentBestThreat,"threats\nIt took",totalAnnealingMoves,"moves to find this solution")    
    
def randomRestartHillClimber(n):
    currentBestSolution=[]
    currentBestThreats=n
    totalHillMoves=0
    #Random restart 500 times 
    for _ in range(500):
        #Generate a random chess board
        currentBoard=randomBoard(n)
        
        while True:
            #Boolean vairable to check if we have moved this loop, if we have not then 
            #There is no neighbour better then our current board
            moved=False
            #Get a array of arrays for the neighbour states
            neighbours=generateNeighbourState(currentBoard)
            #Itterat through the array
            for neighbour in neighbours:
                #If the threat count of the neighbour is less then our own then
                #it is better and we should move to it
                if numOfThreatenedQueens(neighbour)<numOfThreatenedQueens(currentBoard):
                    currentBoard=neighbour
                    totalHillMoves=totalHillMoves+1
                    moved=True
            #If the current board has no threats then we have found an optimal solution and we can finish
            #(this will occur when we move to a neighbour with a threat value of 0)
            if numOfThreatenedQueens(currentBoard) == 0 :
                break
            #If we have checked all our neighbours and not moved then our board 
            #is the best for this loop and we can leave
            if moved!=True:
                break
            #If nether of these conditions are met then the while loop will go again, 
            #with the new neighbours board acting as our current board.
            #This will continue until one of the above conditions are met
            
        #Check if the solution we got in the loop is better then our overall one from the random start
        #If it is make that the overall best current solutio
        if numOfThreatenedQueens(currentBoard)<currentBestThreats:
            currentBestThreats=numOfThreatenedQueens(currentBoard)
            currentBestSolution=list(currentBoard)
            #if the threats from the new board is 0 then we can go ahead and 
            #leave since we've found an optimal solutuion
            if currentBestThreats ==0:
                break
            
            
     
    print("Random Restart Hill Climber\nBest solution found:",currentBestSolution,
          "with",currentBestThreats,"threats\nIt took",totalHillMoves,"moves to find this solution")    
    
def generateNeighbourState(board):
    neighbours=[]
    for c,r in enumerate(board):
    
        #Each neighbour should be the same as board with only 1 queen moved
        #Note neighbour = board does not work as it will pass by refrence not value
        neighbour=list(board)
        
        #Make a neighbour state that has the value of 1 queen changed to a value between 0 and n-1
        #But not the value it had originaly
        for x in range(0,len(board)):
            if x != r :
                neighbour[c]=x
                neighbours.append(neighbour)
                neighbour=list(board)
    return neighbours
    
#Heuristic/Fitness Code
def numOfThreatenedQueens(board):
    
    threatenedQueens=0
    for column,row in enumerate(board): #We need to use enumerate to get the column of the queen
        
        #Check if each individual queen is threatened    
        if isQueenThreatened(board,column,row):
            threatenedQueens=threatenedQueens+1
   
    #Returns heuristic of how many queens are being threatened, max number is n        
    return threatenedQueens

def isQueenThreatened(board,queenColumn,queenRow):
    queenOnRow=0
    queenOnLeftDiag=0
    queenOnRightDiag=0
    
    for column,row in enumerate(board): #We need to use enumerate to get the column of the queen
        #Check row for queens 
        if row == queenRow:
            queenOnRow=queenOnRow+1
        #If more then 1 queen in row then there is a threat
        if queenOnRow>1:    
            return True    
        
        #Check left diagonal for queens    
        if (column-queenColumn) == (row-queenRow): 
            queenOnLeftDiag=queenOnLeftDiag+1        
        #If more then 1 queen on left diagonal then there is a threat
        if queenOnLeftDiag>1:
            return True
        
        #Check right diagonal for queens
        if (queenColumn-column) == -(queenRow-row): 
            queenOnRightDiag=queenOnRightDiag+1
        #If more then 1 qeen on right diagonal then there is a threat
        if queenOnRightDiag>1:
            return True
    #If no return has triggered till this point then there is no threat for this queen    
    return False  



if __name__ == '__main__':
    np.random.seed(2017)
    n = 8
    assignment3(n)
    
