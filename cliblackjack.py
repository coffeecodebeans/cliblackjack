import random
import curses
import time
cards = {"2H": 2, "3H": 3, "4H": 4, "5H": 5, "6H": 6, "7H": 7, "8H": 8, "9H": 9, "10H": 10, "2C": 2, "3C": 3, "4C": 4, "5C": 5, "6C": 6, "7C": 7, "8C": 8, "9C": 9, "10C": 10, "2D": 2, "3D": 3, "4D": 4, "5D": 5, "6D": 6, "7D": 7, "8D": 8, "9D": 9, "10D": 10,
         "2S": 2, "3S": 3, "4S": 4, "5S": 5, "6S": 6, "7S": 7, "8S": 8, "9S": 9, "10S": 10, "JH": 10, "QH": 10, "KH": 10, "JC": 10, "QC": 10, "KC": 10, "JD": 10, "QD": 10, "KD": 10, "JS": 10, "QS": 10, "KS": 10, "AJ": (1, 11), "AQ": (1, 11), "AK": (1, 11)}


def obtain_score(cards_list):
    score = 0
    for i in cards_list:
        if 'A' not in i:
            score += cards[i]
        elif 'A' in i:
            if score + 11 <= 21:
                score += 11
            elif score + 11 > 21:
                score += 1
    return score




def main(stdscr):
    curses.curs_set(0)
    while 1:
        stdscr.clear()
        l = [x for x in cards]
        random.shuffle(l)
        player = [l.pop(),l.pop()]
        dealer = [l.pop(), l.pop()]
        h,w = stdscr.getmaxyx()
        curses.init_pair(1,curses.COLOR_RED,curses.COLOR_BLACK)
        curses.init_pair(2,curses.COLOR_GREEN,curses.COLOR_BLACK)
        for i in range(0,h):
            stdscr.clear()
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(i,w//2,"Blackjack",curses.A_BLINK)
            stdscr.attroff(curses.color_pair(1))
            time.sleep(.1)
            stdscr.refresh()
        stdscr.clear()
        stdscr.attron(curses.color_pair(1))
        stdscr.addstr(h//2,w//2 - len("Black Jack")//2,"BLACK JACK",curses.A_BLINK)
        stdscr.attroff(curses.color_pair(1))
        stdscr.addstr(h//2+1,w//2 - len("Press Enter to continue")//2,"Press Enter to continue")
        stdscr.refresh()
        time.sleep(1)
        while 1:
            key = stdscr.getch()
            if key == curses.KEY_ENTER or key in [10,13]:
                break

        while 1:
            stdscr.clear()
            h, w = stdscr.getmaxyx()
            flag = 0
            y = h // 4
            x = w//2 - len("Dealer")//2
            stdscr.addstr(y, x, "Dealer", curses.COLOR_RED)
            for idx, car in enumerate(dealer):
                if idx == 0:
                    stdscr.addstr(y+1, x, '#')
                else:
                    stdscr.addstr(y+1, x, car)
                x += 5
            y1 = h // 2 + h // 4
            x1 = w//2-len("Player")//2
            stdscr.addstr(y1, x1, "Player : " + str(obtain_score(player)), curses.COLOR_GREEN)

            for idx, car in enumerate(player):

                stdscr.addstr(y1+1, x1, car)
                x1 += 5
            if obtain_score(player) == 21:
                stdscr.attron(curses.color_pair(2))
                stdscr.addstr(h//2, w//2-len("BLACK JACK")//2,"BLACK JACK", curses.A_BLINK)
                stdscr.attroff(curses.color_pair(2))
                break
            stdscr.addstr(h//2,0, "Press UP KEY FOR HIT")
            stdscr.addstr(h//2+1, 0, "Press DOWN KEY FOR STAND")
            stdscr.refresh()
            key = stdscr.getch()
            time.sleep(2)
            if key == curses.KEY_UP:
                car = l.pop()
                player.append(car)
                if obtain_score(player) > 21:
                    stdscr.addstr(y1+1, x1, car)
                    stdscr.addstr(h//2, w//2 - len("You are busted") //2, "You are BUSTED", curses.A_BLINK)
                    stdscr.addstr(h//2 + 1, w//2 - len("NEW GAME RESUMING IN THREE SECONDS") //2, "NEW GAME RESUMING IN THREE SECONDS", curses.A_BLINK)
                    stdscr.refresh()
                    time.sleep(3)
                    break
                else:
                    stdscr.addstr(y1+1, x1, car)
                    x1 += 3
                    continue
            if key == curses.KEY_DOWN:
                # stand
                stdscr.clear()
                player_score = obtain_score(player)
                dealer_score = obtain_score(dealer)
                if dealer_score < 17:
                    while dealer_score < 17:
                        dealer.append(l.pop())
                        dealer_score += obtain_score(dealer)
                h , w = stdscr.getmaxyx()
                y = h // 4
                x = w//2 - len("Dealer")//2
                stdscr.addstr(y, x, "Dealer :  " + str(obtain_score(dealer)), curses.COLOR_RED)
                for idx,car in enumerate(dealer):
                    stdscr.addstr(y+1, x, car)
                    x += 5
                y1 = h // 4 + h // 2
                x1 = w//2 - len("Player")//2
                stdscr.addstr(y1, x1, "Player   :  " +str(obtain_score(player)) , curses.COLOR_GREEN)
                x1 = x1 - len(player)
                for idx, car in enumerate(player):
                    stdscr.addstr(y1+1, x1, car)
                    x1 += 5
                if player_score > 21 and player_score < dealer_score:
                    stdscr.attron(curses.color_pair(1))
                    stdscr.addstr(h//2, w//2 - len("Dealer Wins")//2,
                                  "DEALER WINS", curses.A_BLINK)
                    stdscr.attroff(curses.color_pair(1))
                elif player_score == dealer_score:
                    stdscr.attron(curses.color_pair(1))
                    stdscr.addstr(h//2, w//2 - len("PUSH")//2,
                                  "PUSH", curses.A_BLINK)
                    stdscr.attroff(curses.color_pair(1))
                elif (dealer_score > 21 and player_score < 21):
                    stdscr.attron(curses.color_pair(2))
                    stdscr.addstr(h//2, w//2 - len("PLAYER WINS")//2,
                                  "PLAYER WINS", curses.A_BLINK)
                    stdscr.attron(curses.color_pair(2))
                elif (player_score > dealer_score and player_score < 21):
                    stdscr.attron(curses.color_pair(2))
                    stdscr.addstr(h//2, w//2 - len("PLAYER WINS")//2,
                                  "PLAYER WINS", curses.A_BLINK)
                    stdscr.attron(curses.color_pair(2))
                stdscr.refresh()
                flag  = 1
                time.sleep(10)
                break

    curses.curs_set(1)
curses.wrapper(main)
