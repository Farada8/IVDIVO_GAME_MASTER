#!/usr/bin/env python3

class State:
    def __init__(self,revision=1):
        self.revision=revision
        self.data={}
    def write(self,base_revision,key,value):
        if base_revision!=self.revision:
            return 'STALE_WRITE_BLOCKED'
        self.data[key]=value
        self.revision+=1
        return 'COMMITTED'

def run():
    state=State()
    a=state.revision
    b=state.revision
    assert state.write(a,'frontier','A')=='COMMITTED'
    assert state.write(b,'frontier','B')=='STALE_WRITE_BLOCKED'
    independent=State()
    rev=independent.revision
    assert independent.write(rev,'branch_A','done')=='COMMITTED'
    rev=independent.revision
    assert independent.write(rev,'branch_B','done')=='COMMITTED'
    assert independent.data=={'branch_A':'done','branch_B':'done'}
    print('C01_STALE_WRITE PASS')
    print('C02_INDEPENDENT_BRANCH PASS')

if __name__=='__main__':
    run()
