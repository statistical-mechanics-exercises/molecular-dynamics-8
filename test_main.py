import unittest
from main import *

class UnitTests(unittest.TestCase) :
    def test_conserved(self) : 
        fighand=plt.gca()
        figdat = fighand.get_lines()[0].get_xydata()
        times, this_con = zip(*figdat)
        for i in range(1,len(this_con) ) :
            self.assertTrue( np.abs( this_con[i-1]-this_con[i] )<1E-2, "The conserved quantity is not conserved" )
            
    def test_kinetic(self) :
        for i in range(10) :
            vel = np.zeros([7,2])
            myeng = 0
            for j in range(7) : 
                vel[j,0], vel[j,1] = np.random.normal(), np.random.normal()
                myeng = myeng + vel[j,0]*vel[j,0] / 2 + vel[j,1]*vel[j,1] / 2
            self.assertTrue( np.abs( kinetic(vel) - myeng )<1E-6, "The kinetic energy is computed incorrectly" )
            
    def test_forces(self) : 
        pp = pos
        base_p, base_f = potential(pp)
        for i in range(7) :
            for j in range(2) :
               pp[i][j] = pp[i][j] + 1E-8
               new_p, crap = potential(pp)
               numder = (new_p-base_p)/1E-8
               self.assertTrue( np.abs(numder + base_f[i][j])<1e-4, "Forces and potential are not consistent" )
               pp[i][j] = pp[i][j] - 1E-8
