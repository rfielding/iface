public interface ApiA {
    /*ApiA module implements this*/
    interface In {
        void setZ(ApiB ApiBArg);
        F doSomeF(X XArg);
        G doSomeG(Y YArg);
        void setB(ApiB ApiBArg);
    }
    interface Precondition {
        bool Pre_setZ();
        bool Pre_doSomeF();
        bool Pre_doSomeG();
        bool Pre_setB();
    }
    interface Connect {
        bool setListener(ApiA.Listen.Move lsn, bool isOn);
        bool setListener(ApiA.Listen.Send lsn, bool isOn);
        bool setListener(ApiA.Listen.Enter lsn, bool isOn);
        bool setListener(ApiA.Listen.Exit lsn, bool isOn);
    }
    /*ApiA state machine observers implements this*/
    interface Listen {
        interface Move {
            void Move_wasCrazy(ApiA snd);
            void Move_respondForK(ApiA snd);
            void Move_wrapUp(ApiA snd);
        }
        interface Send {
            void Send_doNotify(ApiA snd,ApiA rcv,Z ZArg);
            void Send_doSomeK(ApiA snd,ApiB rcv,X XArg);
        }
        interface Enter {
            void Enter_constructing(ApiA snd);
            void Enter_destroyed(ApiA snd);
            void Enter_init(ApiA snd);
            void Enter_wentcrazy(ApiA snd);
            void Enter_responded(ApiA snd);
            void Enter_constructed(ApiA snd);
        }
        interface Exit {
            void Exit_constructing(ApiA snd);
            void Exit_destroyed(ApiA snd);
            void Exit_init(ApiA snd);
            void Exit_wentcrazy(ApiA snd);
            void Exit_responded(ApiA snd);
            void Exit_constructed(ApiA snd);
        }
    }
}
public interface ApiB {
    /*ApiB module implements this*/
    interface In {
        K doSomeK(X XArg);
    }
    interface Precondition {
        bool Pre_doSomeK();
    }
    interface Connect {
        bool setListener(ApiB.Listen.Move lsn, bool isOn);
        bool setListener(ApiB.Listen.Send lsn, bool isOn);
        bool setListener(ApiB.Listen.Enter lsn, bool isOn);
        bool setListener(ApiB.Listen.Exit lsn, bool isOn);
    }
    /*ApiB state machine observers implements this*/
    interface Listen {
        interface Move {
            void Move_initializing(ApiB snd);
            void Move_wrapUp(ApiB snd);
        }
        interface Send {
            void Send_doNotify(ApiB snd,ApiA rcv,Z ZArg);
            void Send_setB(ApiB snd,ApiA rcv,ApiB ApiBArg);
        }
        interface Enter {
            void Enter_destroyed(ApiB snd);
            void Enter_init(ApiB snd);
            void Enter_constructed(ApiB snd);
        }
        interface Exit {
            void Exit_destroyed(ApiB snd);
            void Exit_init(ApiB snd);
            void Exit_constructed(ApiB snd);
        }
    }
}
public interface ApiC {
    /*ApiC module implements this*/
    interface In {
    }
    interface Precondition {
    }
    interface Connect {
        bool setListener(ApiC.Listen.Move lsn, bool isOn);
        bool setListener(ApiC.Listen.Send lsn, bool isOn);
        bool setListener(ApiC.Listen.Enter lsn, bool isOn);
        bool setListener(ApiC.Listen.Exit lsn, bool isOn);
    }
    /*ApiC state machine observers implements this*/
    interface Listen {
        interface Move {
            void Move_initializing(ApiC snd);
            void Move_emitF(ApiC snd);
            void Move_emitG(ApiC snd);
            void Move_wrapUp(ApiC snd);
        }
        interface Send {
            void Send_doNotify(ApiC snd,ApiA rcv,Z ZArg);
            void Send_doSomeF(ApiC snd,ApiA rcv,X XArg);
            void Send_doSomeG(ApiC snd,ApiA rcv,Y YArg);
        }
        interface Enter {
            void Enter_destroyed(ApiC snd);
            void Enter_init(ApiC snd);
            void Enter_constructed(ApiC snd);
        }
        interface Exit {
            void Exit_destroyed(ApiC snd);
            void Exit_init(ApiC snd);
            void Exit_constructed(ApiC snd);
        }
    }
}
