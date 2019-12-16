#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Module to solve BattleShip problems from the Logic Problems game.
'''

# System libraries for the initial phase.
import sys
import os
import argparse
import datetime
import time
import math

# Application libraries.
import modGetGame




def write(sText : str):
    ''' write the text to the output without a linefeed. '''
    print(sText, end='')
    oFile = open('results.txt', 'a')
    oFile.write(sText)
    oFile.close()



def writeLine(sText: str):
    ''' write the text to the output and add a linefeed. '''
    print(sText)
    oFile = open('results.txt', 'a')
    oFile.write(sText)
    oFile.write("\n")
    oFile.close()



def displayLine(numPositions, line):
    ''' Function to display a horizontal line in a Battleship problem '''
    mask = 1
    for pos in range(0, numPositions):
        if line & mask == mask:
            write(u"\u2588")
        else:
            write(u"\u00B7")
        mask *= 2



def countSolids(line):
    ''' Returns the number of solids in the specified line position. '''
    binaryLine = '{0:b}'.format(line)
    count = 0
    for pos in range (0, len(binaryLine)):
        if binaryLine[pos] == '1':
            count += 1
    return count



def getLongestShip(line):
    ''' Returns the size of the longest ship on the line. '''
    binaryLine = '{0:b}'.format(line)
    maximumShip = 0
    current = 0
    for pos in range (0, len(binaryLine)):
        if binaryLine[pos] == '1':
            current += 1
            if current > maximumShip:
                maximumShip = current
        else:
            current = 0
    return maximumShip



def countShipsOnLine(line, ships):
    ''' Counts the number and size of ships on the line. '''
    binaryLine = '{0:b}'.format(line)
    current = 0
    for pos in range (0, len(binaryLine)):
        if binaryLine[pos] == '1':
            current += 1
        else:
            if current > 1:
                ships[current] += 1
            current = 0
    if current > 1:
        ships[current] += 1
    return True



def getPossibleLines(numPositions, numSolid, maxShip, mask, negativeMask):
    ''' Returns the set of possible lines that have the specified number of solid positions. '''
    # print('getPossibleLines({}, {}, {}, {}, {})'.format(numPositions, numSolid, maxShip, mask, negativeMask))
    listResult = []
    maximumLines = (2 ** numPositions) - 1
    for pos in range(0, maximumLines):
        if countSolids(pos) == numSolid:
            if pos & mask == mask:
                if (~pos) & negativeMask == negativeMask:
                    if getLongestShip(pos) <= maxShip:
                        listResult.append(pos)
    return listResult



def isAnyThreadRunning(threads):
    ''' Returns True if any of the specified threads are running. '''
    isRunning = False
    for thread in threads:
        if thread.poll() is None:
            isRunning = True
    return isRunning



class Battleships():
    ''' Class to represent a game of Battleships. '''



    def __init__(self, grid, maxShip, label, args):
        ''''
        Class Constructor.

        :ivar int grid: Specifies the grid size for the game of battleships.
        :ivar int maxShip: Specifies the size of the largest battleship.  Expected 4 or 5.
        :ivar string label: Specifies a label for the problem.
        '''
        self.grid = grid
        self.maxShip = maxShip
        self.horizontal = []
        self.vertical = []
        self.mask = []
        self.negativeMask = []
        self.line = []
        self.check_ships = True
        self.start_search = 0
        self.finish_search = 100
        self.indent = 2
        self.label = label
        self.isTranspose = False
        self.solve_game = True
        for row in range(0, self.grid):
            self.horizontal.append(1)
            self.vertical.append(1)
            self.line.append(0)
            self.mask.append(0)
            self.negativeMask.append(0)
        if args != None:
            self.ApplyParameters(args)



    def VerticalLine(self, nIndex):
        ''' Calculates the score for the vertical line. '''
        mask = 2 ** nIndex
        line = 0
        for row in range(self.grid):
            if self.line[row] & mask == mask:
                line = line + 2**row
        return line



    def isShip(self, x, y):
        ''' Returns true if the specified position is ship in the current position. '''
        # Allow questions outside the grid.  The answer is false.
        if x < 0 or x >= self.grid or y < 0 or y >= self.grid:
            return False

        # Search on the board.
        mask = 2 ** x
        return self.line[y] & mask == mask



    def getShips(self):
        ''' Returns the number and size of the ships. '''
        ships = []
        for shipSize in range(0, self.maxShip + 1):
            ships.append(0)
        for row in range(0, self.grid):
            countShipsOnLine(self.line[row], ships)
            countShipsOnLine(self.VerticalLine(row), ships)
        shipsOne = self.total_ships
        for shipSize in range(0, self.maxShip+1):
            shipsOne -= shipSize * ships[shipSize]
        ships[1] = shipsOne

        return ships



    def write(self):
        ''' Print the current game position. '''
        # Get the number and size of ships.
        ships = self.getShips()

        # Display the game position.
        print('\033[K', end='')
        write(u"\u250F")
        for y in range(0, self.grid):
            write(u"\u2501")
        write(u"\u2513")
        if self.isTranspose:
            write('\033[40`')
            write(u"\u250F")
            for y in range(0, self.grid):
                write(u"\u2501")
            write(u"\u2513")
        writeLine('')

        for row in range(0, self.grid):
            print('\033[K', end='')
            write(u"\u2503")
            displayLine(self.grid, self.line[row])
            write(u"\u2503")
            write('{}'.format(self.horizontal[row]))

            if row <= self.maxShip and row >= 1:
                write('  {} x {} '.format(ships[row], row))
                for nSize in range(0, row):
                    write(u"\u2588")

            if self.isTranspose:
                write('\033[40`')
                write(u"\u2503")
                mask = 2**row
                for pos in range(0, self.grid):
                    if self.line[pos] & mask == mask:
                        write(u"\u2588")
                    else:
                        write(u"\u00B7")
                write(u"\u2503")
            writeLine('')

            # print(self.horizontal[row], end='')
            # print('{}, {}'.format(self.line[row], self.VerticalLine(row)))

        print('\033[K', end='')
        write(u"\u2517")
        for y in range(0, self.grid):
            write(u"\u2501")
        write(u"\u251B")
        if self.isTranspose:
            write('\033[40`')
            write(u"\u2517")
            for y in range(0, self.grid):
                write(u"\u2501")
            write(u"\u251B")
        writeLine('')

        print('\033[K', end='')
        write(' ')
        for row in range(0, self.grid):
            write('{}'.format(self.vertical[row]))
        writeLine('')

        #for x in range(0, self.grid):
        #    for y in range(0, self.grid):
        #        if self.isShip(x, y):
        #            print('({},{}) '.format(x, y), end='')
        #print()



    def isValidSolution(self):
        ''' Returns true if the current position is valid solution to the problem. '''

        for row in range(0, self.grid):
            line = self.VerticalLine(row)

            # Check that the vertical lines match the conditions
            if countSolids(line) != self.vertical[row]:
                return False

            # Check the length of the battle ships.
            if getLongestShip(line) > self.maxShip:
                return False

        # Check the ships are not touching.
        for x in range(0, self.grid):
            for y in range(0, self.grid):
                if self.isShip(x, y):
                    # Check the diaoctals.
                    if self.isShip(x-1, y-1):
                        return False
                    if self.isShip(x+1, y-1):
                        return False
                    if self.isShip(x-1, y+1):
                        return False
                    if self.isShip(x+1, y+1):
                        return False

        # Optionally check for the correct number of ships.
        if self.check_ships:
            ships = self.getShips()
            if ships[1] != 4:
                return False
            if ships[2] != 3:
                return False
            if ships[3] != 2:
                return False
            if ships[4] != 1:
                return False

        # Looks good!!
        return True



    def CheckTouching(self):
        ''' Report the touching status of the solution. '''
        for x in range(0, self.grid):
            for y in range(0, self.grid):
                if self.isShip(x, y):
                    # Check the diaoctals.
                    if self.isShip(x-1, y-1):
                        print('Touching at ({},{}) and ({},{})'.format(x, y, x-1, y-1))
                    if self.isShip(x+1, y-1):
                        print('Touching at ({},{}) and ({},{})'.format(x, y, x+1, y-1))
                    if self.isShip(x-1, y+1):
                        print('Touching at ({},{}) and ({},{})'.format(x, y, x-1, y+1))
                    if self.isShip(x+1, y+1):
                        print('Touching at ({},{}) and ({},{})'.format(x, y, x+1, y+1))



    def GetNumPossible(self, nLevel):
        nAnswer = 1
        for index in range(nLevel, self.grid):
            nAnswer = nAnswer * len(self.posibilities[index])
        return nAnswer



    def Search(self, nLevel):
        ''' Search for a solution at the specified level. '''
        percentage = 100 * self.count / self.number
        if percentage < self.start_search:
            nStep = self.GetNumPossible(nLevel)
            # print('Level = {} Step = {}'.format(nLevel, nStep))
            step_percentage = 100 * ( self.count + nStep ) / self.number
            # print('\tPercentage = {}'.format(step_percentage))
            if step_percentage < self.start_search:
                self.count = self.count + nStep
                return
            else:
                pass
                #print('GO')
        if percentage <= self.finish_search:
            for Possible in self.posibilities[nLevel]:
                self.line[nLevel] = Possible
                if nLevel == self.grid - 1:
                    if percentage >= self.start_search: # and percentage <= self.finish_search:
                        if self.isValidSolution():
                            writeLine('\033[K{}'.format(datetime.datetime.now()))
                            self.write()
                    self.count = self.count + 1
                    # Display the progress on this thread.
                    # if self.count % 100000 == 0:
                    if self.count % 10000000 == 0:
                        # These write an extra space into the next progress box.
                        elapsed_time = time.time() - self.start_time
                        completed = (percentage - self.start_search) / (self.finish_search - self.start_search)
                        total_time = elapsed_time / completed
                        estimated_time = 30 + (1 - completed) * total_time
                        if self.indent > 0:
                            print('\033[{}C{:>7.3f} '.format(self.indent, percentage))
                            print('\033[{}C {:03.0f}:{:02.0f} '.format(self.indent, estimated_time // 3600, estimated_time % 3600 // 60))
                            print('\033[{}C {:03.0f}:{:02.0f} '.format(self.indent, elapsed_time // 3600, elapsed_time % 3600 // 60))
                            print('\033[{}C {:03.0f}:{:02.0f} '.format(self.indent, total_time // 3600, total_time % 3600 // 60), end='\r\033[3A', flush=True)
                        else:
                            print('{:>7.3f} '.format(percentage))
                            print(' {:03.0f}:{:02.0f} '.format(estimated_time // 3600, estimated_time % 3600 // 60))
                            print(' {:03.0f}:{:02.0f} '.format(elapsed_time // 3600, elapsed_time % 3600 // 60))
                            print(' {:03.0f}:{:02.0f} '.format(total_time // 3600, total_time % 3600 // 60), end='\r\033[3A', flush=True)
                else:
                    self.Search(nLevel+1)



    def ShowInitialPosition(self):
        ''' Returns true if the inital position should be shown. '''
        # if self.start_search == 0: # and self.finish_search == 100:
        #    return True
        return False



    def Solve(self):
        ''' Solve the game of battleships '''
        self.start_time = time.time()
        self.count = 0
        self.number = 1
        self.posibilities = []
        nTotalShipsHorizontal = 0
        nTotalShipsVertical = 0
        if self.ShowInitialPosition():
            writeLine(self.label)
            write(u"\u250F")
            for y in range(0, self.grid):
                write(u"\u2501")
            writeLine(u"\u2513")
        for x in range(0, self.grid):
            if self.ShowInitialPosition():
                write(u"\u2503")
                for y in range(0, self.grid):
                    mask = 2 ** y
                    if self.mask[x] & mask == mask:
                        write(u"\u2588")
                    elif self.negativeMask[x] & mask == mask:
                        write(u"\u00B7")
                    else:
                        write(' ')
                write(u"\u2503")
            # print('{} {} {}'.format(self.horizontal[x], self.mask[x], self.negativeMask[x]))
            possibleLines = getPossibleLines(self.grid, self.horizontal[x], self.maxShip, self.mask[x], self.negativeMask[x])
            self.posibilities.append(possibleLines)
            self.number = self.number * len(possibleLines)
            if self.ShowInitialPosition():
                writeLine('{}    There are {} possible lines.'.format(self.horizontal[x], len(possibleLines)))

            nTotalShipsHorizontal = nTotalShipsHorizontal + self.horizontal[x]
            nTotalShipsVertical = nTotalShipsVertical + self.vertical[x]

        if self.ShowInitialPosition():
            write(u"\u2517")
            for y in range(0, self.grid):
                write(u"\u2501")
            writeLine(u"\u251B")

            write(' ')
            for row in range(0, self.grid):
                write('{}'.format(self.vertical[row]))
            writeLine('')

            writeLine('Search space is {:,}'.format(self.number))

        if nTotalShipsHorizontal == nTotalShipsVertical:
            self.total_ships = nTotalShipsHorizontal
            if self.number > 0:
                if self.solve_game:
                    self.Search(0)
                    # These write an extra space into the next progress box.
                    if self.indent > 0:
                        print('\033[{}C ------ '.format(self.indent), end='\r', flush=True)
                    else:
                        print(' ------ ', end='\r', flush=True)

            # print('Search Space  {:,}'.format(self.number))
            # print('Actual Search {:,}'.format(self.count))
        else:
            print('Total ships horizontal != ships vertical. {} != {}'.format(nTotalShipsHorizontal, nTotalShipsVertical))
        # print('Finished')



    def ApplyParameters(self, args):
        ''' Apply the parameters to the game object. '''
        if args.start != None:
            self.start_search = float(args.start)
        if args.finish != None:
            self.finish_search = float(args.finish)
        if args.indent != None:
            self.indent = int(args.indent)
        if args.threads != None:
            self.solve_game = False
        if args.transpose:
            self.isTranspose = True



    def Transpose(self):
        ''' Switch the game on it's side. '''
        for x in range(0, self.grid):
            temporary = self.horizontal[x]
            self.horizontal[x] = self.vertical[x]
            self.vertical[x] = temporary

        transposedMask = []
        mask = 1
        for x in range(0, self.grid):
            add = 1
            work = 0
            for y in range(0, self.grid):
                # print('{} {}'.format(self.mask[y], mask))
                if self.mask[y] & mask == mask:
                    work |= add
                add *= 2
            transposedMask.append(work)
            mask *= 2

        for x in range(0, self.grid):
            self.mask[x] = transposedMask[x]


        transposedMask = []
        mask = 1
        for x in range(0, self.grid):
            add = 1
            work = 0
            for y in range(0, self.grid):
                # print('{} {}'.format(self.mask[y], mask))
                if self.negativeMask[y] & mask == mask:
                    work |= add
                add *= 2
            transposedMask.append(work)
            mask *= 2

        for x in range(0, self.grid):
            self.negativeMask[x] = transposedMask[x]



def main():
    # Process the command line arguments.
    # This might end the program (--help).
    argParse = argparse.ArgumentParser(prog='battleships', description='Solver for Battleships.')
    argParse.add_argument('-g', '--game', help='The index of the game to solve.', action='store')
    argParse.add_argument('-s', '--start', help='The starting percentage.', action='store')
    argParse.add_argument('-f', '--finish', help='The finish percentage.', action='store')
    argParse.add_argument('-i', '--indent', help='The indent for the progress percentage.', action='store')
    argParse.add_argument('-t', '--threads', help='Split the program into threads.', action='store')
    argParse.add_argument('-p', '--transpose', help='Switch the problem 90 degrees.', action='store_true')
    argParse.add_argument('-r', '--remain', help='Display estimated time remaining not progress.', action='store_true')
    argParse.add_argument('-v', '--verbose', help='Increase the output level.', action='store_true')

    args = argParse.parse_args()

    # Display the parameters.
    if args.verbose:
        print(sys.argv)

    # Reset the output file.
    if args.threads == None:
        oFile = open('results.txt', 'w')
        oFile.close()
    else:
        nThreads = int(args.threads)
        if nThreads > 1:
            oFile = open('results.txt', 'w')
            oFile.close()

    # Indentify the game to solve.
    bShowGame = False
    nGame = 0
    if args.game != None:
        try:
            nGame = int(args.game)
        except:
            pass
    while nGame == 0:
        bShowGame = True
        print('Please enter the game number.')
        nGame = input()
        try:
            nGame = int(nGame)
        except:
            print('I do not understand')
            nGame = 0
    # print('Game = {}'.format(nGame))

    game = modGetGame.getGame(nGame, args)

    if game.isTranspose:
        game.Transpose()

    if args.threads == None:
        bShowGame = True
    else:
        nThreads = int(args.threads)
        if nThreads > 1:
            bShowGame = True

    if bShowGame:
        writeLine(game.label)
        write(u"\u250F")
        for y in range(0, game.grid):
            write(u"\u2501")
        writeLine(u"\u2513")
        nNumber = 1
        for x in range(0, game.grid):
            possibleLines = getPossibleLines(game.grid, game.horizontal[x], game.maxShip, game.mask[x], game.negativeMask[x])
            nNumber *= len(possibleLines)

            write(u"\u2503")
            for y in range(0, game.grid):
                mask = 2 ** y
                if game.mask[x] & mask == mask:
                    write(u"\u2588")
                elif game.negativeMask[x] & mask == mask:
                    write(u"\u00B7")
                else:
                    write(' ')
            write(u"\u2503")
            writeLine('{}     {:4n} {:4n}    There are {} possible lines.'.format(game.horizontal[x], game.mask[x], game.negativeMask[x], len(possibleLines)))

        write(u"\u2517")
        for y in range(0, game.grid):
            write(u"\u2501")
        writeLine(u"\u251B")

        write(' ')
        for row in range(0, game.grid):
            write('{}'.format(game.vertical[row]))
        writeLine('')

        writeLine('Search space is {:,}.  log = {:0.2f}'.format(nNumber, math.log10(nNumber)))

    if args.threads != None:
        nThreads = int(args.threads)
        if nThreads <= 1:
            # Give the other threads time to output initial status.
            time.sleep(1)

            # print('args.threads = {}.'.format(nThreads))
            # Solve the specified game.
            game.Solve()
        else:
            # print('args.threads = {}.'.format(nThreads))
            import subprocess
            nSplit = nThreads
            if nSplit > 20:
                nSplit = 20
            elif nSplit < 2:
                nSplit = 2

            fAmount = float((game.finish_search - game.start_search) / nSplit)
            fStart = game.start_search
            nIndent = 0
            threads = []
            for nIndex in range(0, nSplit-1):
                if args.verbose:
                    print('Thread({}) --game={} --start={} --finish={} --indent={} --threads={}'.format(nIndex, nGame, fStart, fStart + fAmount, nIndent, 1))
                oCommand = [__file__, '--game', '{}'.format(nGame) , '--start', '{}'.format(fStart), '--finish', '{}'.format(fStart + fAmount), '--indent', '{}'.format(nIndent), '--threads', '1']
                if game.isTranspose:
                    oCommand.append('-p')
                if args.verbose:
                    oCommand.append('-v')
                threads.append(subprocess.Popen(oCommand))
                fStart = fStart + fAmount
                nIndent = nIndent + 7
            if game.finish_search >= 100:
                if args.verbose:
                    print('Thread({}) --game={} --start={} --indent={} --threads={}'.format(nSplit-1, nGame, fStart, nIndent, 1))
                oCommand = [__file__, '--game', '{}'.format(nGame), '--start', '{}'.format(fStart), '--indent', '{}'.format(nIndent), '--threads', '1']
                if game.isTranspose:
                    oCommand.append('-p')
                if args.verbose:
                    oCommand.append('-v')
                threads.append(subprocess.Popen(oCommand))
            else:
                if args.verbose:
                    print('Thread({}) --game={} --start={} --finish={} --indent={} --threads={}'.format(nSplit-1, nGame, fStart, game.finish_search, nIndent, 1))
                oCommand = [__file__, '--game', '{}'.format(nGame), '--start', '{}'.format(fStart), '--finish', '{}'.format(game.finish_search), '--indent', '{}'.format(nIndent), '--threads', '1']
                if game.isTranspose:
                    oCommand.append('-p')
                if args.verbose:
                    oCommand.append('-v')
                threads.append(subprocess.Popen(oCommand))

            while isAnyThreadRunning(threads):
                time.sleep(10)
            print()
            print()
            print()
            print()
            print('\033[KFinished.')

        # Exit this script.
        # quit()



if __name__ == '__main__':
    main()
