"""
Vypracovanie ulohy - tvorba molekul vody
Je potrebna implementacia znovupouzitelnej bariery
inicializovanej na hodnotu 3 (2 atomy vodika,
1 atom kyslika). Bariera nam zabezpeci to,
aby sa pockali tieto tri atomy a zamadzili tak
tvorbe dalsej molekuly, kym sa nezlucia aktualne
tri atomy. Taktiez sa pouzil binarny semafor.
Binarny preto, lebo chceme aby ine vlakno uvolnilo
chod kritickej oblasti. V pripade pouzitia mutexu
by jedno vlakno, ktore zamklo oblast muselo tuto
oblast aj odokmnut, co je pre tento problem
nepouzitelne.
"""
from fei.ppds import Semaphore, Mutex, Thread, Event, print
from random import randint
from time import sleep


class Barrier:

    def __init__(self, N):
        self.N = N
        self.mutex = Mutex()
        self.counter = 0
        self.semaphore = Semaphore(0)

    def wait(self):
        self.mutex.lock()
        self.counter += 1
        if self.counter == self.N:
            self.counter = 0
            self.semaphore.signal(self.N)
        self.mutex.unlock()
        self.semaphore.wait()


class Molecule:
    def __init__(self):
        # binarny semafor
        self.mutex = Semaphore(1)
        self.oxygenQueue = Semaphore(0)
        self.hydrogenQueue = Semaphore(0)
        self.oxygen = 0
        self.hydrogen = 0
        self.barrier = Barrier(3)

    def oxygenFunc(self):
            # zamadzenie pristupu do KO
            self.mutex.wait()
            self.oxygen += 1
            """
            Ak je este nedostatocny pocet vodikov
            tak chod dalej a uvolni pridanie
            sa dalsiemu kysliku
            """
            if self.hydrogen < 2:
                self.mutex.signal()
            else:
                self.oxygen -= 1
                self.hydrogen -= 2
                # odobera sa kyslik z "fronty"
                self.oxygenQueue.signal()
                # odoberaju sa 2 vodiky z "fronty"
                self.hydrogenQueue.signal(2)

            # Pridava sa jeden kyslik do "fronty"
            self.oxygenQueue.wait()
            print("oxygen do zlucenia")

            # zlucovanie
            self.bond()

            """
            bariera, kde sa caka na dobehnutie
            vsetkych 3 atomov po zluceni, aby
            sa mohli ist dalsie atomy zlucovat
            """
            self.barrier.wait()
            self.mutex.signal()

    def hydrogenFunc(self):
        # zamadzenie pristupu do KO
        self.mutex.wait()
        self.hydrogen += 1

        """
        Ak je nedostatocny pocet kyslikov alebo vodikov
        tak uvolni pridanie sa dalsiemu vodiku a chood
        dalej
        """
        if self.hydrogen < 2 or self.oxygen < 1:
            self.mutex.signal()
        else:
            self.oxygen -= 1
            self.hydrogen -= 2
            # odobera sa kyslik z "fronty"
            self.oxygenQueue.signal()
            # odoberaju sa 2 vodiky z "fronty"
            self.hydrogenQueue.signal(2)

        # Pridava sa vodik do zlucenia
        self.hydrogenQueue.wait()
        print("Hydrogen do zlucenia")

        # zlucovanie
        self.bond()

        """
        bariera, kde sa caka na dobehnutie
        vsetkych 3 atomov po zluceni, aby
        sa mohli ist dalsie atomy zlucovat
        """
        self.barrier.wait()

    def bond(self):
        # prevedenie zlucovania
        sleep(randint(5, 15)/10)
        print("Zlucenie buniek")


def init_and_run():

    threads = list()
    molecule = Molecule()

    # neustale sa tvoriace vlakna vodikov a kyslikov
    while True:
        threads.append(Thread(molecule.oxygenFunc))
        threads.append(Thread(molecule.hydrogenFunc))

    # for t in threads:
    #    t.join()

if __name__ == "__main__":
    init_and_run()
